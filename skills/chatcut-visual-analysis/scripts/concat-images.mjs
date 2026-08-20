#!/usr/bin/env node

import { existsSync, mkdirSync, mkdtempSync, rmSync } from "node:fs";
import { basename, dirname, extname, join, resolve } from "node:path";
import { spawnSync } from "node:child_process";

const parsed = parseArgs(process.argv.slice(2));
const outputPath = resolve(parsed.output);
const outputExtension = extname(outputPath).toLowerCase();

if (![".jpg", ".jpeg", ".png", ".webp"].includes(outputExtension)) {
  fail("--output must end in .jpg, .jpeg, .png, or .webp");
}
if (parsed.inputs.length === 0 || parsed.inputs.length > 25) {
  fail("Pass between 1 and 25 input images");
}
if (parsed.captions.length && parsed.captions.length !== parsed.inputs.length) {
  fail("Pass exactly one --caption per input image, or omit captions entirely");
}

const inputs = parsed.inputs.map((input) => resolve(input));
for (const input of inputs) {
  if (!existsSync(input)) fail(`Input image does not exist: ${input}`);
}

mkdirSync(dirname(outputPath), { recursive: true });
const temporaryDirectory = mkdtempSync(
  join(dirname(outputPath), ".concat-images-"),
);
const imageMagick = resolveImageMagick();

try {
  const prepared = inputs.map((input, index) => {
    const preparedPath = join(temporaryDirectory, `${index}.png`);
    const args = imageMagick.prefix.concat([
      input,
      ...(parsed.crop ? ["-crop", parsed.crop, "+repage"] : []),
      "-auto-orient",
      "-resize",
      `${parsed.tileWidth}x${parsed.tileWidth}>`,
      preparedPath,
    ]);
    run(imageMagick.command, args, `prepare ${input}`);
    return preparedPath;
  });

  const captions = parsed.captions.length
    ? parsed.captions
    : inputs.map((input) => basename(input));
  const columns = parsed.columns ?? Math.ceil(Math.sqrt(inputs.length));
  const montageArgs = imageMagick.montagePrefix.concat([
    ...prepared.flatMap((input, index) => ["-label", captions[index], input]),
    "-tile",
    `${columns}x`,
    "-geometry",
    `+${parsed.gap}+${parsed.gap}`,
    "-background",
    "#111111",
    "-fill",
    "#ffffff",
    "-stroke",
    "none",
    "-pointsize",
    "24",
    outputPath,
  ]);
  run(imageMagick.command, montageArgs, "compose contact sheet");

  process.stdout.write(
    `${JSON.stringify(
      {
        columns,
        crop: parsed.crop ?? null,
        inputs: inputs.map((input, index) => ({
          caption: captions[index],
          path: input,
        })),
        outputPath,
        rows: Math.ceil(inputs.length / columns),
      },
      null,
      2,
    )}\n`,
  );
} finally {
  rmSync(temporaryDirectory, { force: true, recursive: true });
}

function parseArgs(args) {
  const result = {
    captions: [],
    columns: undefined,
    crop: undefined,
    gap: 16,
    inputs: [],
    output: undefined,
    tileWidth: 720,
  };
  for (let index = 0; index < args.length; index += 1) {
    const arg = args[index];
    if (arg === "--caption")
      result.captions.push(requiredValue(args, ++index, arg));
    else if (arg === "--columns")
      result.columns = boundedInteger(
        requiredValue(args, ++index, arg),
        arg,
        1,
        9,
      );
    else if (arg === "--crop") result.crop = requiredValue(args, ++index, arg);
    else if (arg === "--gap")
      result.gap = boundedInteger(
        requiredValue(args, ++index, arg),
        arg,
        0,
        100,
      );
    else if (arg === "--output")
      result.output = requiredValue(args, ++index, arg);
    else if (arg === "--tile-width")
      result.tileWidth = boundedInteger(
        requiredValue(args, ++index, arg),
        arg,
        100,
        2000,
      );
    else if (arg === "--help" || arg === "-h") usage(0);
    else if (arg.startsWith("-")) fail(`Unknown option: ${arg}`);
    else result.inputs.push(arg);
  }
  if (!result.output) fail("--output is required");
  if (result.crop && !/^\d+x\d+\+\d+\+\d+$/.test(result.crop)) {
    fail("--crop must use WIDTHxHEIGHT+X+Y pixel geometry");
  }
  return result;
}

function resolveImageMagick() {
  if (commandExists("magick")) {
    return { command: "magick", montagePrefix: ["montage"], prefix: [] };
  }
  if (commandExists("convert") && commandExists("montage")) {
    return { command: "convert", montagePrefix: [], prefix: [] };
  }
  fail("ImageMagick is unavailable; expected magick or convert + montage");
}

function commandExists(command) {
  return (
    spawnSync("sh", ["-c", `command -v ${command}`], {
      stdio: "ignore",
    }).status === 0
  );
}

function run(command, args, step) {
  const executable =
    step === "compose contact sheet" && command === "convert"
      ? "montage"
      : command;
  const result = spawnSync(executable, args, { encoding: "utf8" });
  if (result.status !== 0) {
    fail(
      `${step} failed: ${(result.stderr || result.stdout || "unknown error").trim()}`,
    );
  }
}

function requiredValue(args, index, option) {
  const value = args[index];
  if (!value) fail(`${option} requires a value`);
  return value;
}

function boundedInteger(value, option, minimum, maximum) {
  const parsed = Number(value);
  if (!Number.isInteger(parsed) || parsed < minimum || parsed > maximum) {
    fail(`${option} must be an integer from ${minimum} to ${maximum}`);
  }
  return parsed;
}

function fail(message) {
  process.stderr.write(`concat-images: ${message}\n`);
  process.exit(1);
}

function usage(exitCode) {
  process.stdout.write(
    "Usage: concat-images.mjs --output <image> [--columns N] [--crop WxH+X+Y] [--caption text ...] <images...>\n",
  );
  process.exit(exitCode);
}
