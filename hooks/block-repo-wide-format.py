#!/usr/bin/env python3
"""PreToolUse/Bash hook: block formatters whose blast radius is the whole repo.

Enforces the `## Formatting & Scope` rule in CLAUDE.md. Exit 2 blocks the
command and feeds stderr back to Claude.

Self-check: python3 block-repo-wide-format.py --selftest
"""

import json
import re
import sys

# (pattern, label). The bare-dot patterns match `.`, `./`, `..`, and quoted
# forms, but NOT a real path — `--write src/app.ts` must pass through.
PATTERNS = [
    (r"\b(npm|pnpm|yarn|bun)\s+run\s+fix:all\b", "npm run fix:all"),
    (r"\b(prettier|biome)\b[^|;&]*--write\s+[\"']?\.{1,2}/?[\"']?(\s|$)", "prettier --write ."),
    (r"\b(eslint|biome)\b[^|;&]*--fix\s+[\"']?\.{1,2}/?[\"']?(\s|$)", "eslint --fix ."),
]

MESSAGE = (
    "Blocked: `{label}` reformats files you did not touch.\n"
    "Format only what you changed: npx prettier --write <files>\n"
    "If a repo-wide run is genuinely needed, ask the user first."
)


def blocked(command):
    """Return the label of the first repo-wide pattern matched, else None."""
    for pattern, label in PATTERNS:
        if re.search(pattern, command):
            return label
    return None


def selftest():
    for cmd in [
        "npm run fix:all",
        "pnpm run fix:all --silent",
        "prettier --write .",
        "npx prettier --write ./",
        'prettier --write "."',
        "eslint --fix .",
    ]:
        assert blocked(cmd), f"should block: {cmd}"
    for cmd in [
        "npm run fix",
        "npm run test",
        "prettier --write src/app.ts",
        "npx prettier --write  src/app.ts",
        "prettier --check .",
        "eslint --fix src/",
        "git log --oneline",
    ]:
        assert not blocked(cmd), f"should allow: {cmd}"
    print("selftest ok")


if __name__ == "__main__":
    if "--selftest" in sys.argv:
        selftest()
        sys.exit(0)

    try:
        command = json.load(sys.stdin).get("tool_input", {}).get("command", "")
    except (json.JSONDecodeError, AttributeError, ValueError):
        sys.exit(0)

    label = blocked(command)
    if label:
        print(MESSAGE.format(label=label), file=sys.stderr)
        sys.exit(2)
