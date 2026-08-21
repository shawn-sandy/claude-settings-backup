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
- Delete only what your own change orphaned — imports, variables, or functions your edit made
  unused. Pre-existing dead code stays; mention it in one line.
- Treat questions as exploration, not approval — answer or ask back, never implement.
- State assumptions before implementing. If the request has two plausible readings that lead to
  different work, name both and pick one out loud — never silently.
- Never search, glob, or read `*/plans/archive` (any depth) unless the user names the path.

## Verification

- Name the check that will prove the work correct before starting it, not after. If no check
  exists, say so in one line and proceed under a stated assumption.
- Never verify rendered output with `grep` against source files or CSS selectors. Verify against the
  *rendered* artifact — built HTML, live DOM, computed styles — using Playwright or the browser MCP.
- If neither is available, say `UNVERIFIED — no browser` explicitly. Never substitute a source-level
  grep and report it as verification.
- Any contrast ratio, measurement, or computed metric written into docs or comments must come from an
  actual tool run. Never estimate.
- In a git worktree, confirm the dev server you are verifying against serves *that* worktree's
  checkout — check the port and cwd. Verifying against the main checkout invalidates the run.

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
- Never run bare `git stash pop`. List `git stash list` first and pop by explicit index — a bare pop
  has restored an unrelated stash and created conflicts.
- Never use `git stash` to isolate changes — use a scratch branch or `git worktree` instead. Run
  `git status` and `git stash list` before any stash operation.
- `git-agent` skills (`branch-agent`, `commit-agent`, `pr-agent`, `ship`) exit plan mode via their
  own Step 0. Callers do not pre-check plan-mode state.

## Ship / PR Workflow

- Pre-flight before any ship or merge skill: confirm `gh auth status` succeeds, the working tree is
  clean, and — for a merge — that a PR already exists. Report blockers verbatim and stop; do not
  attempt workarounds or guess at a re-auth.
- Review-bot triage is governed by `~/.claude/rules/review-bot-loops.md`: verify a claim before
  fixing it, report declined nitpicks to you rather than replying on the PR, and never treat a
  re-fired review as a new instruction.

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
  page, exercise the change, check both light and dark themes, and re-check at a mobile width.
- Run axe against the real page, not a Storybook iframe — navigate to the page first, then audit.
  Auditing inside the iframe stalls and produces no result.
- Evidence means measured values — computed styles, element boxes, console/network output. A
  screenshot alone is not evidence; screenshots have come back blank.
- Add srcset/responsive checks for any image change.

## Before Opening a PR

- Run the full test suite and lint/type checks locally; do not rely on CI reviewers to catch
  regressions.
- Run a fresh-context adversarial review of `git diff <default-branch>...HEAD` (code-review agent
  when available) and fix confirmed defects before opening the PR — review bots should find
  nothing. Hunt especially: no-op edits, vacuous assertions, self-introduced regressions.
- Add these five to that review — each has shipped past self-review and been caught by a bot instead:
  pagination/sort tie-breakers, unvalidated `parseInt`/`Number()` on user or query input, derived
  state left stale after a client-side update (counts, links, labels), timezone-dependent date
  anchors, and scripts that continue after a failed step. Add a regression test for each fix.
- If verification is blocked, say so explicitly. Never mark a plan complete on unverified work.

## Tests You Write

- Every assertion must fail if the behaviour regresses. No tautologies, no assertions locked to
  exact wording.
- Clean up any temp directories the tests create.
- Write the regression test before the fix and watch it fail. If it was written after the fix,
  revert the fix and confirm it fails before committing.
- Default stack unless the project says otherwise: Vitest as the runner (React and plain JS),
  React Testing Library for components.

## Code Conventions

- React components: arrow functions, function components. No class components.
- TypeScript: `_underscore` prefix for private fields, `camelCase` for public fields.
- Prefer double quotes in JS/TS — matches the `quoteStyle` settings in the VS Code config.
- When a file's local style differs from the conventions above, match the file. Mention the
  mismatch; do not restyle it.

## Formatting & Scope

- Never run repo-wide formatters or codemods (`npm run fix:all`, `prettier --write .`, bulk `sass`
  rebuilds). Format only the files you touched: `npx prettier --write <files>`.
- If a repo-wide fix genuinely seems necessary, ask first. A formatter that rewrites hundreds of
  untouched files buries the real diff and needs a guarded revert.

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
- When asked for a plan, proposal, or implementation doc, write the spec only. Create or edit
  implementation files only after explicit approval — in or out of plan mode.

## Response Style

- Keep responses concise and under output token limits; summarize rather than dump.
