#!/usr/bin/env python3
"""
Tests for validate-plan-filename.py.
Run: python3 ~/.claude/hooks/test_validate_plan_filename.py
Exits 0 on all-pass, 1 on any failure.
"""

import importlib.util
import json
import os
import subprocess
import sys
import tempfile

# ── load the hook module (filename contains hyphens → importlib required) ────
_HOOK_DIR = os.path.dirname(os.path.abspath(__file__))
_HOOK_SCRIPT = os.path.join(_HOOK_DIR, "validate-plan-filename.py")

_spec = importlib.util.spec_from_file_location("validate_plan_filename", _HOOK_SCRIPT)
_mod = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(_mod)
classify_filename = _mod.classify_filename
get_plans_dir = _mod._get_plans_dir
is_plan_path = _mod._is_plan_path

# ── helpers ───────────────────────────────────────────────────────────────────
_failures = []


def check(label, got, expected):
    if got != expected:
        _failures.append(f"  FAIL [{label}]: got {got!r}, want {expected!r}")
    else:
        print(f"  pass  {label}")


def run_hook(file_path):
    """Run the hook script via subprocess. Returns (returncode, stderr)."""
    payload = json.dumps({"tool_input": {"file_path": file_path}})
    result = subprocess.run(
        [sys.executable, _HOOK_SCRIPT],
        input=payload,
        capture_output=True,
        text=True,
    )
    return result.returncode, result.stderr


# ── unit: _get_plans_dir ─────────────────────────────────────────────────────
print("\n── Unit: _get_plans_dir() ───────────────────────────────────────────────")

_orig_settings_path = _mod._SETTINGS_PATH

with tempfile.TemporaryDirectory() as _cfg_tmp:
    _fake_settings = os.path.join(_cfg_tmp, "settings.json")

    # Custom relative path → normalized (strip ./ and trailing /)
    with open(_fake_settings, "w") as fh:
        json.dump({"plansDirectory": "./custom/plans/"}, fh)
    _mod._SETTINGS_PATH = _fake_settings
    check("custom relative './custom/plans/'", get_plans_dir(), "custom/plans")

    # No plansDirectory key → fallback
    with open(_fake_settings, "w") as fh:
        json.dump({"model": "opus"}, fh)
    check("missing key → fallback", get_plans_dir(), "docs/plans")

    # Empty string → fallback
    with open(_fake_settings, "w") as fh:
        json.dump({"plansDirectory": ""}, fh)
    check("empty string → fallback", get_plans_dir(), "docs/plans")

    # Absolute path → kept as-is (trailing slash stripped)
    with open(_fake_settings, "w") as fh:
        json.dump({"plansDirectory": "/Users/me/myproject/plans/"}, fh)
    check("absolute path → strip trailing /", get_plans_dir(), "/Users/me/myproject/plans")

    # Non-existent settings file → fallback
    _mod._SETTINGS_PATH = os.path.join(_cfg_tmp, "nonexistent.json")
    check("missing settings.json → fallback", get_plans_dir(), "docs/plans")

    _mod._SETTINGS_PATH = _orig_settings_path  # restore

# Real settings.json → should return "docs/plans" (plansDirectory: "./docs/plans")
check("real settings.json → 'docs/plans'", get_plans_dir(), "docs/plans")

# ── unit: _is_plan_path ───────────────────────────────────────────────────────
print("\n── Unit: _is_plan_path() ────────────────────────────────────────────────")

check("relative: match",   is_plan_path("/proj/docs/plans/add-foo.md", "docs/plans"), True)
check("relative: no match", is_plan_path("/proj/src/add-foo.md", "docs/plans"), False)
check("relative: custom",  is_plan_path("/proj/custom/plans/add-foo.md", "custom/plans"), True)
check("absolute: match",   is_plan_path("/abs/plans/add-foo.md", "/abs/plans"), True)
check("absolute: no match", is_plan_path("/other/plans/add-foo.md", "/abs/plans"), False)

# ── unit: classify_filename ───────────────────────────────────────────────────
print("\n── Unit: classify_filename() ────────────────────────────────────────────")

# Real violators from ~/.claude/docs/plans/
_INVALID = [
    ("for-some-reason-or-modular-bubble",                     "prompt-echo prefix"),
    ("claude-md-please-optimize-this-cosmic-ullman",          "noun-led (claude)"),
    ("claude-plugin-install-playwright-claude-delegated-flurry", "noun-led (claude)"),
    ("converting-the-plan-distributed-dahl",                  "gerund not verb"),
    ("i-want-rules-plan-mode-md-to-magical-allen",            "noun-led (i)"),
    # Real violators from ~/.claude/rules/docs/plans/
    ("plan-mode-md-add-a-step-2026-05-22",                    "trailing date"),
    ("update-the-plan-mode-md-to-2026-05-22",                 "trailing date + stop-word"),
    # Harness hex suffix
    ("something-agent-aa2bbf33da4ee6cb1",                     "hex suffix"),
    # Generic placeholders
    ("plan",                                                  "generic"),
    ("draft",                                                 "generic"),
    ("untitled",                                              "generic"),
]

_VALID = [
    "create-social-post-skill",
    "add-dark-mode-toggle",
    "fix-login-redirect",
    "refactor-auth-module",
    "enforce-plan-filenames",
    "add-plan-filename-hook",
    # backfilled plan names (also exercises newly-added verbs)
    "optimize-global-claude-md",
    "install-playwright-plugin",
    "switch-plan-mode-to-html-output",
    "add-clarify-align-steps-to-plan-mode",
    "require-meaningful-plan-filenames",
    "require-per-step-verification",
    "add-repo-name-frontmatter",
]

for stem, comment in _INVALID:
    ok, reason = classify_filename(stem)
    check(f"INVALID '{stem}' ({comment})", ok, False)

for stem in _VALID:
    ok, reason = classify_filename(stem)
    check(f"VALID   '{stem}'", ok, True)

# ── integration: hook exit codes ──────────────────────────────────────────────
print("\n── Integration: hook subprocess exit codes ──────────────────────────────")

with tempfile.TemporaryDirectory() as tmp:
    plans_dir = os.path.join(tmp, "docs", "plans")
    os.makedirs(plans_dir)

    # Bad name → exit 2, stderr references plan-mode.md §4
    bad_file = os.path.join(plans_dir, "i-want-a-thing.md")
    with open(bad_file, "w") as fh:
        fh.write("# Plan: I want a thing\n\n## Context\ntest\n")
    rc, err = run_hook(bad_file)
    check("bad name → exit 2", rc, 2)
    check("bad name → stderr has 'plan-mode.md §4'", "plan-mode.md §4" in err, True)

    # Good name → exit 0
    good_file = os.path.join(plans_dir, "add-dark-mode-toggle.md")
    with open(good_file, "w") as fh:
        fh.write("# Plan: Add dark-mode toggle\n\n## Context\ntest\n")
    rc, err = run_hook(good_file)
    check("good name → exit 0", rc, 0)

    # status: completed → exit 0 even with a bad name
    completed_file = os.path.join(plans_dir, "i-want-bad-name.md")
    with open(completed_file, "w") as fh:
        fh.write("---\nstatus: completed\ntype: feature\ncreated: 2026-01-01\n---\n# Plan\ntest\n")
    rc, err = run_hook(completed_file)
    check("completed plan, bad name → exit 0 (skipped)", rc, 0)

    # Path not under docs/plans/ → exit 0
    other_file = os.path.join(tmp, "i-want-this.md")
    with open(other_file, "w") as fh:
        fh.write("# Not a plan\n")
    rc, err = run_hook(other_file)
    check("non-plan path → exit 0", rc, 0)

    # Non-.md extension → exit 0
    txt_file = os.path.join(plans_dir, "some-file.txt")
    with open(txt_file, "w") as fh:
        fh.write("text\n")
    rc, err = run_hook(txt_file)
    check("non-md extension → exit 0", rc, 0)

# ── summary ───────────────────────────────────────────────────────────────────
total = 6 + 5 + len(_INVALID) + len(_VALID) + 5
print()
if _failures:
    print(f"FAILED  ({len(_failures)} of {total} tests):")
    for f in _failures:
        print(f)
    sys.exit(1)
else:
    print(f"ALL {total} TESTS PASSED")
    sys.exit(0)
