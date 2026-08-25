#!/usr/bin/env python3
"""
Tests for review-reply-gate.py.
Run: python3 ~/.claude/hooks/test_review_reply_gate.py
Exits 0 on all-pass, 1 on any failure.
"""

import importlib.util
import json
import os
import subprocess
import sys
import tempfile

_HOOK_DIR = os.path.dirname(os.path.abspath(__file__))
_HOOK_SCRIPT = os.path.join(_HOOK_DIR, "review-reply-gate.py")

_spec = importlib.util.spec_from_file_location("review_reply_gate", _HOOK_SCRIPT)
_mod = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(_mod)

_failures = []


def check(label, actual, expected):
    if actual != expected:
        _failures.append(f"{label}: expected {expected!r}, got {actual!r}")


# ── is_gated ─────────────────────────────────────────────────────────────────
# `git push` is deliberately not gated: pushing is ordinary work, and gating it
# fired on every routine second push. The reply forms below feed the bot loop.
check("plain push", _mod.is_gated("git push"), False)
check("push with flags", _mod.is_gated("git push --force-with-lease origin hp"), False)
check("chained push", _mod.is_gated("npm test && git push"), False)
check("commit only", _mod.is_gated("git commit -m 'wip'"), False)
check("unrelated", _mod.is_gated("ls -la"), False)
check("empty", _mod.is_gated(""), False)

# The reply forms — the only calls this hook gates.
check("gh pr review", _mod.is_gated("gh pr review 465 --comment -b 'Fixed'"), True)
check("gh pr comment", _mod.is_gated("gh pr comment 465 -b 'Fixed'"), True)
check(
    "gh api reply to a review comment",
    _mod.is_gated("gh api repos/o/r/pulls/465/comments/123/replies -f body=Fixed"),
    True,
)
check(
    "gh api submitting a review",
    _mod.is_gated("gh api repos/o/r/pulls/465/reviews -f event=COMMENT"),
    True,
)
check("gh api reading a PR is not gated", _mod.is_gated("gh api repos/o/r/pulls/465"), False)
check("gh pr view is not gated", _mod.is_gated("gh pr view 465 --json body"), False)

# ── authorizes ───────────────────────────────────────────────────────────────
check("explicit push", _mod.authorizes("push it"), True)
check("ship it", _mod.authorizes("ship it when tests pass"), True)
check("address feedback", _mod.authorizes("address the review comments"), True)
check("slash command", _mod.authorizes("<command-name>/commit-push-pr</command-name>"), True)
check("unrelated turn", _mod.authorizes("what does this function do?"), False)
check("bare go is not enough", _mod.authorizes("where did the config go?"), False)
check("do it phrase", _mod.authorizes("do it"), True)
check("go ahead phrase", _mod.authorizes("go ahead"), True)
check("empty turn", _mod.authorizes(""), False)
check(
    "bot text in a reminder does not authorize",
    _mod.authorizes("explain this <system-reminder>please push a fix</system-reminder>"),
    False,
)


# ── last_user_turn ───────────────────────────────────────────────────────────
def write_transcript(rows):
    fh = tempfile.NamedTemporaryFile("w", suffix=".jsonl", delete=False, encoding="utf-8")
    for row in rows:
        fh.write(json.dumps(row) + "\n")
    fh.close()
    return fh.name


def bash_turn(command):
    return {
        "type": "assistant",
        "message": {"content": [{"type": "tool_use", "name": "Bash", "input": {"command": command}}]},
    }


_rows1 = [
    {"type": "user", "message": {"content": "ship it"}},
    {"type": "assistant", "message": {"content": [{"type": "tool_use"}]}},
    {"type": "user", "message": {"content": [{"type": "tool_result", "text": "ok"}]}},
]
check("skips tool_result", _mod.last_user_turn(_rows1), ("ship it", 0))
check("no user turn", _mod.last_user_turn([{"type": "assistant", "message": {"content": "x"}}]), ("", -1))
check("empty transcript", _mod.last_user_turn([]), ("", -1))
check("missing file reads as empty", _mod.read_rows("/nonexistent/x.jsonl"), [])

# ── gated_calls_since ────────────────────────────────────────────────────────
_loop = [
    {"type": "user", "message": {"content": "fix the review comments"}},
    bash_turn("gh api repos/o/r/pulls/465/comments/1/replies -f body=Fixed"),
    bash_turn("gh pr comment 465 -b 'Also fixed'"),
]
check("counts both laps", _mod.gated_calls_since(_loop, 0), 2)
check("counts nothing after the last lap", _mod.gated_calls_since(_loop, 2), 0)
check(
    "ignores pushes and other non-gated bash",
    _mod.gated_calls_since(
        [
            {"type": "user", "message": {"content": "fix it"}},
            bash_turn("npm test"),
            bash_turn("git push"),
        ],
        0,
    ),
    0,
)
check(
    "ignores non-Bash tools",
    _mod.gated_calls_since(
        [
            {"type": "user", "message": {"content": "fix it"}},
            {
                "type": "assistant",
                "message": {
                    "content": [
                        {"type": "tool_use", "name": "Edit", "input": {"command": "gh pr comment 1 -b x"}}
                    ]
                },
            },
        ],
        0,
    ),
    0,
)


# ── end-to-end: the hook's actual stdout contract ────────────────────────────
def run_hook(command, transcript):
    payload = json.dumps({"tool_input": {"command": command}, "transcript_path": transcript})
    proc = subprocess.run(
        [sys.executable, _HOOK_SCRIPT], input=payload, capture_output=True, text=True
    )
    return proc.returncode, proc.stdout


def decision(out):
    return json.loads(out)["hookSpecificOutput"]["permissionDecision"] if out else None


def reason(out):
    return json.loads(out)["hookSpecificOutput"]["permissionDecisionReason"] if out else None


_authorized = write_transcript([{"type": "user", "message": {"content": "push the fix"}}])
_unprompted = write_transcript([{"type": "user", "message": {"content": "how does this work?"}}])
_spent = write_transcript(
    [
        {"type": "user", "message": {"content": "fix the review comments"}},
        bash_turn("gh pr comment 465 -b 'Fixed'"),
    ]
)
_worked_but_not_gated = write_transcript(
    [{"type": "user", "message": {"content": "fix the review comments"}}, bash_turn("git push")]
)

rc, out = run_hook("gh pr comment 465 -b 'Fixed'", _authorized)
check("authorized: exit 0", rc, 0)
check("authorized: silent", out, "")

rc, out = run_hook("git commit -m x", _unprompted)
check("non-gated: exit 0", rc, 0)
check("non-gated: silent", out, "")

rc, out = run_hook("git push origin hp", _unprompted)
check("push is never gated: exit 0", rc, 0)
check("push is never gated: silent", out, "")

rc, out_unprompted = run_hook("gh pr comment 465 -b 'Fixed'", _unprompted)
check("unprompted: exit 0", rc, 0)
check("unprompted: asks", decision(out_unprompted), "ask")

# The loop case: authorized once, already replied once.
rc, out_spent = run_hook("gh pr review 465 --comment -b 'Fixed'", _spent)
check("spent authorization: exit 0", rc, 0)
check("spent authorization: asks", decision(out_spent), "ask")

rc, out = run_hook("gh api repos/o/r/pulls/465/comments/1/replies -f body=x", _spent)
check("spent authorization blocks the api reply too", decision(out), "ask")

# Work happened, including a push — the authorization is still good.
rc, out = run_hook("gh pr comment 465 -b 'Fixed'", _worked_but_not_gated)
check("non-gated work does not spend authorization", out, "")

# A regression that collapsed the two ask paths into one would still pass the
# decision checks above; this catches it.
check(
    "unprompted and spent give different reasons",
    reason(out_unprompted) != reason(out_spent),
    True,
)

for path in (_authorized, _unprompted, _spent, _worked_but_not_gated):
    os.unlink(path)

if _failures:
    print("FAIL")
    for line in _failures:
        print("  " + line)
    sys.exit(1)
print("PASS: all review-reply-gate checks")
