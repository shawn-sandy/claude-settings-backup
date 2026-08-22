---
description: Plan document authoring — target directory, frontmatter, filename convention, required sections, and writing style. Loads when working inside a plans directory.
paths:
  - "**/plans/**"
  - "**/docs/plans/**"
---

# Plan Document Authoring

Read this before writing any plan file. Entering plan mode is governed by `plan-mode.md`.

## Filenames

- Before naming a new plan or artifact file, read the checks in
  `~/.claude/hooks/validate-plan-filename.py` — it exits 2 on a violation.
- Match all of them: strict kebab-case, first token in its `IMPERATIVE_VERBS` set, no stop-word
  second token, no trailing hex or `-YYYY-MM-DD` suffix, no generic name.
- Use a `verb-target` name: `add-dark-mode-toggle`, `fix-login-redirect`, `refactor-auth-module`.
- **Always** re-check the name before committing. Two triggers require a rename: the initial
  filename is auto-generated or non-descriptive, or the plan's purpose shifted after creation. A
  stale filename is a plan defect — do not commit until the name matches the content.

## Location

Resolve the target directory in order: (1) the configured `plansDirectory` if set, (2) `docs/plans/`
if it exists, (3) the default Claude user plans folder.

## Frontmatter

**Always** add YAML frontmatter to every new plan file: `status: todo`, `type:
<feature|fix|refactor|docs|chore>`, `created: YYYY-MM-DD`, `repo-name: <repo>`. Resolve `repo-name`
from the basename of the `origin` git remote URL (strip trailing `.git`); if no remote exists, fall
back to the basename of the current working directory.

**Always** update `status` (and `modified: YYYY-MM-DD`) as the plan progresses: `todo` →
`in-progress` → `completed`. Use `/plan-status` to automate this.

## Required Structure

Every plan must include:

- `context` — Background and motivation; why this work is needed.
- `objective` — One or two sentences summarising the goal.
- `steps` — A numbered list where each item has three parts: the action, a brief *why*, and a
  *verify* line stating how to confirm that step succeeded before moving on. Per-step verification
  is local; the top-level `verification` section covers end-to-end correctness.
- `tests` — Real application tests: actual test files written for the application or feature, run
  by the project's test runner, and committed to the codebase. Distinct from per-step verification
  and end-to-end verification, which are prose assertions inside the plan document. Two-tier depth:
  - **Tier 1** (code-touching plans) — Any plan whose steps create, modify, or delete application
    source files. Include all applicable test sub-sections (unit, integration, E2E) plus the
    mandatory objective-verification test. Unit tests target a single function/module in isolation;
    integration tests exercise multiple modules/services together; E2E tests drive a full user flow
    through the running application — include each "when applicable" based on what the steps touch.
  - **Tier 2** (non-code plans) — Plans whose steps only move/rename/delete non-source files, write
    docs, or update non-runtime metadata. Include only the mandatory objective-verification test;
    omit unit/integration/E2E sub-sections entirely rather than leaving empty stubs. Moving,
    renaming, or deleting application source files is Tier 1.
  - **Objective-verification test** (mandatory, both tiers) — A real mock or smoke test file that
    runs against the application and directly asserts the plan's stated objective is accomplished.
    Always appears first, as a highlighted hero card, before any unit/integration/E2E sub-sections.
  - Select the tier from what the steps actually do, not the `type:` frontmatter field — a
    `type: chore` plan that changes import paths is Tier 1; one that moves docs directories is Tier 2.
- `acceptance-criteria` — A checklist of conditions that must be true for the plan to be done from
  the requester's perspective. Each item is a short, falsifiable statement, not a task. Distinct
  from `verification`: verification checks that steps ran correctly; acceptance criteria check that
  the result meets the definition of done.
- `verification` — How to confirm the entire plan was executed correctly end-to-end.
- `next-steps` *(optional)* — Out-of-scope follow-ups and unsolicited ideas; never place these in
  `steps`. Each item is a short label with description followed by a fenced ```text block
  containing a self-contained prompt the user can paste directly into Claude.
- `unresolved-questions` *(optional)* — Open questions needing user input; omit entirely if none.
  Each item is a short label followed by a fenced ```text block containing a self-contained prompt
  that asks Claude to investigate and recommend.

## Alignment and Commit

- After the steps are drafted, use `AskUserQuestion` (batched, covering each step) to confirm every
  step aligns with the stated objective. This verifies step-to-objective alignment, not overall
  approval — approval is requested separately via `ExitPlanMode`.
- **Always** commit plan files to version control alongside the related changes.

## Writing Style

Direct, imperative, developer-friendly — real names (file paths, function names, CLI flags), lists
over prose, one idea per item, explicitly scoped. Plan only what was requested; unsolicited ideas
go in `next-steps`.

## Skeleton

Copy `~/.claude/reference/SKELETON.md` as a starter for every new plan. Read it when authoring a
plan — it is not loaded into context automatically.
