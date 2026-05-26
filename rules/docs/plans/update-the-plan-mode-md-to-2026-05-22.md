---
status: todo
type: docs
created: 2026-05-21
repo-name: rules
---

# Plan: Add `repo-name` to required plan frontmatter

## Context

The current [plan-mode.md](../../plan-mode.md) rule requires three frontmatter fields on every plan: `status`, `type`, `created`. Plans are written to a global user plans directory (`~/.claude/rules/docs/plans/`) that aggregates work from many different repos. Once a plan lives there, its originating repository is not recoverable from the file alone — the filename and contents may reference paths, but nothing identifies the repo by name.

The user wants `repo-name` added to the required frontmatter so each plan is self-identifying about which repo it belongs to.

## Objective

Update [plan-mode.md](../../plan-mode.md) (and the matching skeleton in [reference/SKELETON.md](../../reference/SKELETON.md)) so every plan's YAML frontmatter is required to include a `repo-name` field, derived from the git remote when available and falling back to the cwd basename otherwise.

## Files to modify

- [/Users/shawnsandy/.claude/rules/plan-mode.md](../../plan-mode.md) — update the Frontmatter step under **Workflow** to require `repo-name` and specify how it is resolved.
- [/Users/shawnsandy/.claude/rules/reference/SKELETON.md](../../reference/SKELETON.md) — the skeleton does not currently include frontmatter; add a minimal frontmatter block at the top so new plans inherit all four required fields (`status`, `type`, `created`, `repo-name`).

## Steps

1. **Edit the Frontmatter step (Workflow §2) in `plan-mode.md`** to list `repo-name` alongside `status`, `type`, `created`, and add a short clause on resolution: use `basename` of the `origin` git remote URL (strip a trailing `.git`); if no remote exists, fall back to the basename of the current working directory.
   - *Why:* Makes `repo-name` a first-class required field with a single unambiguous resolution rule, so authors and any plan-generating skill agree on the value.
   - *Verify:* Re-read [plan-mode.md](../../plan-mode.md) and confirm step 2 of Workflow now names four fields (`status`, `type`, `created`, `repo-name`) and includes the remote-then-cwd resolution clause.

2. **Add a frontmatter block to the top of `reference/SKELETON.md`** containing all four required fields with placeholder values (`status: todo`, `type: <feature|fix|refactor|docs|chore>`, `created: YYYY-MM-DD`, `repo-name: <repo-name>`).
   - *Why:* The skeleton is copied as the starter for every new plan; without the frontmatter block here, authors who copy the skeleton will keep producing plans missing the new field.
   - *Verify:* Open [reference/SKELETON.md](../../reference/SKELETON.md) and confirm the file now begins with a `---` block listing the four fields, before the `# Plan: <title>` heading.

## Acceptance Criteria

- [ ] `plan-mode.md` Workflow §2 lists `repo-name` as a required frontmatter field, with the same emphasis as `status`, `type`, `created`.
- [ ] `plan-mode.md` specifies how `repo-name` is resolved: git remote basename first, cwd basename as fallback.
- [ ] `reference/SKELETON.md` begins with a YAML frontmatter block containing all four required fields.
- [ ] No other sections of `plan-mode.md` (When to plan, Required Structure, Writing Style, Skeleton) are altered.
- [ ] This plan file itself carries the new `repo-name` frontmatter field, so it serves as a worked example of the new rule.

## Verification

- Open [plan-mode.md](../../plan-mode.md) and read Workflow §2 — it must require four fields and describe the resolution rule.
- Open [reference/SKELETON.md](../../reference/SKELETON.md) — it must start with a `---` frontmatter block containing the four fields above the `# Plan: <title>` heading.
- Mentally draft a new plan against the updated rule from scratch: copying the skeleton should produce a file whose frontmatter already has all four required fields, needing only value substitution.
- Confirm this plan file's own frontmatter contains `repo-name: rules` (derived from the cwd `/Users/shawnsandy/.claude/rules` since this directory has no git remote), demonstrating the fallback path works.

## Next Steps *(optional)*

- Backfill `repo-name` into existing plans:
  ```text
  Scan every plan file under ~/.claude/rules/docs/plans/ and add a `repo-name` field to the YAML frontmatter of each one. Resolve the value by reading the plan's content for path hints (e.g. references to a specific repo); if ambiguous, use `rules` (the cwd basename for this global plans directory). Do not modify any other frontmatter fields. Report a list of files changed and any plans where repo-name could not be determined confidently.
  ```

- Teach plan-generating skills about the new field:
  ```text
  Audit the skills under ~/.claude/plugins/ and ~/.claude/skills/ that generate plan files (anything that writes to docs/plans/ or uses the SKELETON.md template). Update each so the frontmatter it emits includes `repo-name`, resolved as: basename of `git config --get remote.origin.url` (strip trailing `.git`) if a remote exists, otherwise basename of the current working directory. Report which skills you updated.
  ```
