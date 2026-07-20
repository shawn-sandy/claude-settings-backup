# CLAUDE.md — Global Instructions

Project `CLAUDE.md` and `./.claude/rules/` **override** these rules on conflict — check both in
unfamiliar projects. Machine-specific overrides belong in `CLAUDE.local.md`.

## Working Style

- No emojis in generated markdown.
- Never start additional work after completing the requested task.
- Never expand scope beyond the specified file or target.
- Treat questions as exploration, not approval — answer or ask back, never implement.
- Never search, glob, or read `*/plans/archive` (any depth) unless the user names the path.

## Git

- Pull the latest default branch from origin before starting work, unless told otherwise.
- Commit ALL modified files in a single commit unless told otherwise — never leave a remainder
  that needs a second prompt.
- Check whether a feature branch is already merged before opening a PR.
- Update docs and changelogs when opening a PR.
- Execute git operations directly — never enter plan mode for git.
- Never delete a branch, run `rm`/`mktemp`/`git clean`, or execute other destructive commands
  without explicit approval. "Merge it" does NOT authorize `--delete-branch`.
- `git-agent` skills (`branch-agent`, `commit-agent`, `pr-agent`, `ship`) exit plan mode via their
  own Step 0. Callers do not pre-check plan-mode state.

## Before Opening a PR

- Run the full test suite and lint/type checks locally; do not rely on CI reviewers to catch
  regressions.
- Verify UI changes in-browser in both light and dark themes; add srcset/responsive checks for any
  image change.

## Generated Files

- Produce generated files (galleries, plugin tables, migrations) with the repo's canonical
  generator script. Never hand-edit generated output or write an ad-hoc parser.

## Workflow

- Before porting or re-implementing a fix, confirm it has not already landed on main — check
  merged PRs.
- Establish root cause before writing code: use DevTools, database queries, or runtime inspection
  to observe actual state. Do not guess iteratively.
- In plan mode, never implement until the user explicitly approves the plan.

## Response Style

- Keep responses concise and under output token limits; summarize rather than dump.
