# CLAUDE.md — Global Instructions

Project `CLAUDE.md` and `./.claude/rules/` **override** these rules on conflict — check both in
unfamiliar projects. Machine-specific overrides belong in `CLAUDE.local.md`.

## Working Style

- No emojis in generated markdown.
- Never start additional work after completing the requested task.
- Never expand scope beyond the specified file or target — no drive-by cleanups, no fixing adjacent
  bugs, no reformatting untouched code. Being inside a file is not permission to fix other things in
  it. Mention unrelated problems in one line; do not edit them.
- Delete only what your own change orphaned. Pre-existing dead code stays; mention it in one line.
- Treat questions as exploration, not approval — answer or ask back, never implement.
- State assumptions before implementing. If the request has two plausible readings that lead to
  different work, name both and pick one out loud — never silently.
- Never search, glob, or read `*/plans/archive` (any depth) unless the user names the path.

## Verification

- Name the check that will prove the work correct before starting it, not after. If no check
  exists, say so in one line and proceed under a stated assumption.
- Any metric written into docs or comments — contrast ratio, measurement, benchmark — must come
  from an actual tool run. Never estimate.
- In a git worktree, confirm the dev server you are verifying against serves *that* worktree's
  checkout — check the port and cwd. Verifying against the main checkout invalidates the run.
- If verification is blocked, say so explicitly. Never mark a plan complete on unverified work.

## Shell Commands

- Use the Bash tool's `run_in_background` flag instead of `&`/`nohup`/`disown` — it survives across
  turns and reports exit status. Foreground `sleep` is blocked.
- `cd x && y` may prompt and its cwd does not persist — prefer absolute paths, or write the
  sequence to one driver script in the scratchpad and run that.
- `curl` and `rm` are denied outright — use WebFetch for fetches.

## Git

- Pull the latest default branch from origin before starting work, unless told otherwise.
- Commit ALL modified files in a single commit unless told otherwise — never leave a remainder that
  needs a second prompt.
- Execute git operations directly — never enter plan mode for git.
- Never merge a PR without explicit approval in the current turn. Green CI, an approving review,
  and "open a PR" are not merge authorization — report readiness, ask, wait.
- Never delete a branch, run `rm`/`mktemp`/`git clean`, or execute other destructive commands
  without explicit approval. "Merge it" does NOT authorize `--delete-branch`. To clean up a
  worktree, `cd` out of it first, then `git worktree remove` + `git branch -d` — never `rm -rf`.
- Never run bare `git stash pop`. List `git stash list` first and pop by explicit index — a bare pop
  has restored an unrelated stash and created conflicts. Never use `git stash` to isolate changes;
  use a scratch branch or `git worktree` instead.
- `git-agent` skills (`branch-agent`, `commit-agent`, `pr-agent`, `ship`) exit plan mode via their
  own Step 0. Callers do not pre-check plan-mode state.

## Pull Requests

- Pre-flight before any ship or merge skill: `gh auth status` succeeds, the working tree is clean,
  and — for a merge — a PR already exists. Report blockers verbatim and stop; do not attempt
  workarounds or guess at a re-auth.
- Check whether the branch is already merged before opening a PR. Update docs and changelogs.
- Run the full test suite and lint/type checks locally; do not rely on CI reviewers to catch
  regressions.
- Run a fresh-context adversarial review of `git diff <default-branch>...HEAD` (code-review agent
  when available) and fix confirmed defects before opening — review bots should find nothing. Hunt:
  no-op edits, vacuous assertions, self-introduced regressions, pagination/sort tie-breakers,
  unvalidated `parseInt`/`Number()` on user or query input, derived state left stale after a
  client-side update (counts, links, labels), timezone-dependent date anchors, and scripts that
  continue after a failed step. Add a regression test for each fix.
- Red CI is not evidence of a code defect — GitHub Actions is frequently billing-blocked on this
  account. Read `gh run view --log-failed` first: a billing/quota block fails every job in seconds
  with no test output. Report it as a billing block; do not "fix" the code.
- Never resolve a review thread you have not read end to end, including every reply — later replies
  routinely retract, narrow, or supersede the opening comment. Never resolve a thread whose fix you
  did not verify landed in the pushed diff.
- Review-bot triage is governed by `~/.claude/reference/review-bot-loops.md`. It no longer
  auto-loads — read it before acting on any review-bot comment. Core rule: verify a claim before
  fixing it, report declined nitpicks to the user rather than replying on the PR, and never treat a
  re-fired review as a new instruction.

## Tests You Write

- Every assertion must fail if the behaviour regresses. No tautologies, no assertions locked to
  exact wording.
- Write the regression test before the fix and watch it fail. If it was written after the fix,
  revert the fix and confirm it fails before committing.
- Clean up any temp directories the tests create.
- Default stack unless the project says otherwise: Vitest as the runner (React and plain JS),
  React Testing Library for components.

## Formatting & Generated Files

- Never run repo-wide formatters or codemods (bulk `prettier --write .`, repo-wide `sass` rebuilds,
  or any "fix everything" package script). Format only the files you touched:
  `npx prettier --write <files>`. If a repo-wide fix genuinely seems necessary, ask first.
- Produce generated files (galleries, plugin tables, migrations) with the repo's canonical generator
  script. Never hand-edit generated output or write an ad-hoc parser.

## Workflow

- Establish root cause before writing code: use DevTools, database queries, or runtime inspection to
  observe actual state. Do not guess iteratively.
- Before porting or re-implementing a fix, confirm it has not already landed on main — check merged
  PRs.
- When asked for a plan, proposal, or implementation doc, write the spec only. Create or edit
  implementation files only after explicit approval — in or out of plan mode.

## Rules Loaded On Demand

These carry the detail for narrower situations. Read one directly if it has not auto-loaded.

- `rules/ui-verification.md` — browser verification, axe, themes, responsive checks. Auto-loads for
  component, template, and stylesheet files.
- `rules/js-ts-conventions.md` — React and TypeScript style. Auto-loads for `.ts`/`.tsx`/`.js`/`.jsx`.
- `rules/component-driven-ui.md` — component-driven UI. Auto-loads for JS-framework component files.
- `rules/typescript-jsdoc.md` — JSDoc conventions. Auto-loads for JS/TS files.
- `rules/plan-authoring.md` — plan location, filename, frontmatter, required sections. Read before
  writing any plan file.
- `reference/review-bot-loops.md` — review-bot triage. Never auto-loads; read it when a review bot
  fires on a PR.
