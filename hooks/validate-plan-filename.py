#!/usr/bin/env python3
"""
PostToolUse hook: enforce plan-mode.md §4 (verb-target kebab-case filenames).

Fires on every Write/Edit. Ignores anything outside the configured plans
directory (reads `plansDirectory` from ~/.claude/settings.json, falls back
to `docs/plans`) and plans whose frontmatter carries `status: completed`.
On a violation: writes a rename message to stderr and exits 2 so Claude
receives it as actionable feedback (PostToolUse exit-2 contract).
On a pass: exits 0 silently.
"""

import json
import os
import re
import sys

_SETTINGS_PATH = os.path.join(os.path.expanduser("~"), ".claude", "settings.json")
_FALLBACK_PLANS_DIR = "docs/plans"

IMPERATIVE_VERBS = {
    "add", "fix", "update", "refactor", "create", "remove", "delete",
    "implement", "migrate", "rename", "move", "document", "enforce",
    "validate", "build", "setup", "set", "configure", "wire", "port",
    "extract", "split", "merge", "replace", "introduce", "support",
    "enable", "disable", "improve", "optimize", "harden", "scaffold",
    "generate", "convert",
    # common imperative verbs not in original seed
    "install", "switch", "require", "extend", "restrict", "register",
    "deprecate", "deploy", "release", "test", "run", "sync", "patch",
    "upgrade", "downgrade", "wrap", "expose", "load", "bootstrap",
}

GENERIC_NAMES = {"plan", "untitled", "draft", "temp", "notes", "todo", "new-plan"}

# Second-token stop-words signal prompt-echo phrasing (e.g. "update-the-...")
STOP_WORDS_2ND = {"the", "a", "an", "this", "that", "my", "some", "please", "to", "of", "for", "want"}

_KEBAB_RE = re.compile(r"^[a-z0-9]+(-[a-z0-9]+)*$")
_HEX_AGENT_RE = re.compile(r"-agent-[0-9a-f]{6,}$")
_HEX_SUFFIX_RE = re.compile(r"-[0-9a-f]{8,}$")
_DATE_SUFFIX_RE = re.compile(r"-\d{4}-\d{2}-\d{2}$")


def classify_filename(stem):
    """
    Return (ok: bool, reason: str).
    ok=True  → filename is valid verb-target kebab-case.
    ok=False → reason describes the first failing check.
    """
    if not _KEBAB_RE.fullmatch(stem):
        return False, "not strict kebab-case (only lowercase letters, digits, hyphens allowed)"
    if _HEX_AGENT_RE.search(stem) or _HEX_SUFFIX_RE.search(stem):
        return False, "contains a harness-generated hex suffix — strip it"
    if _DATE_SUFFIX_RE.search(stem):
        return False, "trailing date belongs in frontmatter `created:`, not the filename"
    if stem in GENERIC_NAMES:
        return False, f"'{stem}' is a generic placeholder name"
    tokens = stem.split("-")
    if tokens[0] not in IMPERATIVE_VERBS:
        return False, (
            f"first word '{tokens[0]}' is not an imperative verb "
            f"— start with e.g. add-, fix-, refactor-"
        )
    if len(tokens) >= 2 and tokens[1] in STOP_WORDS_2ND:
        return False, (
            f"second word '{tokens[1]}' is a stop-word "
            f"— looks like a prompt-echo (e.g. 'update-the-...' → 'update-plan-mode')"
        )
    return True, ""


def _get_plans_dir():
    """Read plansDirectory from settings.json; normalize and fall back to 'docs/plans'."""
    try:
        with open(_SETTINGS_PATH, encoding="utf-8") as fh:
            settings = json.load(fh)
        val = (settings.get("plansDirectory") or "").strip()
        if val:
            if os.path.isabs(val):
                return val.rstrip("/")
            # Relative path: strip leading ./ and trailing /
            return val.lstrip("./").strip("/") or _FALLBACK_PLANS_DIR
    except (OSError, json.JSONDecodeError, ValueError):
        pass
    return _FALLBACK_PLANS_DIR


def _is_plan_path(path, plans_dir):
    """Return True if path is a .md file inside plans_dir."""
    normalized = path.replace(os.sep, "/")
    if os.path.isabs(plans_dir):
        return normalized.startswith(plans_dir + "/")
    return f"/{plans_dir}/" in normalized


def _is_completed(path):
    """Return True if the file has `status: completed` in its YAML frontmatter."""
    try:
        with open(path, encoding="utf-8") as fh:
            lines = fh.read().splitlines()
    except OSError:
        return False
    if not lines or lines[0].strip() != "---":
        return False
    for line in lines[1:]:
        if line.strip() == "---":
            break
        if re.match(r"^\s*status:\s*completed\s*$", line):
            return True
    return False


def main():
    try:
        data = json.load(sys.stdin)
    except (json.JSONDecodeError, ValueError):
        sys.exit(0)

    path = (data.get("tool_input") or {}).get("file_path", "")
    if not path or not path.endswith(".md"):
        sys.exit(0)

    plans_dir = _get_plans_dir()
    if not _is_plan_path(path, plans_dir):
        sys.exit(0)

    if _is_completed(path):
        sys.exit(0)

    stem = os.path.basename(path)[: -len(".md")]
    ok, reason = classify_filename(stem)
    if ok:
        sys.exit(0)

    msg = (
        f"\n[plan-filename] '{os.path.basename(path)}' violates plan-mode.md §4 "
        f"(verb-target kebab-case).\n"
        f"Reason: {reason}.\n"
        f"Rename to an imperative verb-target name before committing, "
        f"e.g. 'add-dark-mode-toggle', 'fix-login-redirect'.\n"
        f"Derive the name from the plan's # H1 title and Objective section.\n"
    )
    sys.stderr.write(msg)
    sys.exit(2)


if __name__ == "__main__":
    main()
