# CLAUDE.md — Global Instructions

Project `CLAUDE.md` and `./.claude/rules/` **override** these rules on conflict — check both in
unfamiliar projects. Machine-specific overrides belong in `CLAUDE.local.md`.

## Working Style

- No emojis in generated markdown.
- Never start additional work after completing the requested task.
- Never expand scope beyond the specified file or target.
- Never make fixes unrelated to the requested change — no drive-by cleanups, no fixing adjacent
  bugs, no reformatting untouched code. Being inside a file is not permission to fix other things
  in it. Mention unrelated problems in one line; do not edit them.
- Treat questions as exploration, not approval — answer or ask back, never implement.
- Never search, glob, or read `*/plans/archive` (any depth) unless the user names the path.

## Git

- Pull the latest default branch from origin before starting work, unless told otherwise.
- Commit ALL modified files in a single commit unless told otherwise — never leave a remainder
  that needs a second prompt.
- Check whether a feature branch is already merged before opening a PR.
- Update docs and changelogs when opening a PR.
- Execute git operations directly — never enter plan mode for git.
- Never merge a PR without explicit approval in the current turn. Green CI, an approving review,
  and "open a PR" are not merge authorization — report readiness, ask, wait.
- Never delete a branch, run `rm`/`mktemp`/`git clean`, or execute other destructive commands
  without explicit approval. "Merge it" does NOT authorize `--delete-branch`. To clean up a
  worktree, `cd` out of it first, then `git worktree remove` + `git branch -d` — never `rm -rf`.
- `git-agent` skills (`branch-agent`, `commit-agent`, `pr-agent`, `ship`) exit plan mode via their
  own Step 0. Callers do not pre-check plan-mode state.

## CI Failures

- GitHub Actions is frequently billing-blocked on this account. Red CI is not evidence of a code
  defect until proven otherwise.
- Read the failure first (`gh run view --log-failed`): a billing/quota block fails every job in
  seconds with no test output. Report it as a billing block; do not "fix" the code.

## Code Review

- Never resolve a review thread you have not read end to end, including every reply. Later replies
  routinely retract, narrow, or supersede the opening comment.
- Never resolve a thread whose fix you did not verify landed in the pushed diff.

## Shell Commands

- Use the Bash tool's `run_in_background` flag instead of `&`/`nohup`/`disown` — it survives across
  turns and reports exit status; `&` detaches from the harness. Foreground `sleep` is blocked.
- `cd x && y` may prompt and its cwd does not persist — prefer absolute paths, or write the
  sequence to one driver script in the scratchpad and run that.
- `curl` and `rm` are denied outright — use WebFetch for fetches.

## UI Changes

- Verify every UI change in a live browser before committing, not before opening the PR. Load the
  page, exercise the change, check both light and dark themes.
- Evidence means measured values — computed styles, element boxes, console/network output. A
  screenshot alone is not evidence; screenshots have come back blank.
- Add srcset/responsive checks for any image change.

## Before Opening a PR

- Run the full test suite and lint/type checks locally; do not rely on CI reviewers to catch
  regressions.
- If verification is blocked, say so explicitly. Never mark a plan complete on unverified work.

## Tests You Write

- Every assertion must fail if the behaviour regresses. No tautologies, no assertions locked to
  exact wording.
- Clean up any temp directories the tests create.
- Default stack unless the project says otherwise: Vitest as the runner (React and plain JS),
  React Testing Library for components, Playwright for end-to-end, MSW for mocking API requests.

## Code Conventions

- React components: arrow functions, function components. No class components.
- TypeScript: `_underscore` prefix for private fields, `camelCase` for public fields.
- Prefer double quotes in JS/TS — matches the `quoteStyle` settings in the VS Code config.

## Plan and Artifact Filenames

- Before naming a new plan or artifact file, read the checks in
  `~/.claude/hooks/validate-plan-filename.py` — it exits 2 on a violation.
- Match all of them: strict kebab-case, first token in its `IMPERATIVE_VERBS` set, no stop-word
  second token, no trailing hex or `-YYYY-MM-DD` suffix, no generic name.

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
