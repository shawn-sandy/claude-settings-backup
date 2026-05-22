---
status: todo
type: docs
created: 2026-05-22
---

# Plan: Strengthen plan-mode.md Rename rule to require meaningful filenames

> **Note on this plan's own filename:** the path `plan-mode-md-add-a-step-wobbly-bachman.md` was auto-generated with a random `wobbly-bachman` suffix. Per the very rule this plan introduces, it should be renamed before commit to something like `require-meaningful-plan-filenames.md` (a `verb-target` kebab-case name). Leaving it stale here is intentional so this plan can serve as a worked example of the problem.

## Context

The current [plan-mode.md](../../plan-mode.md) Workflow has a `Rename` rule (§3) that only triggers a rename **when the plan's purpose shifts**:

> 3. **Rename** — **Always** update the filename when the plan's purpose shifts; re-evaluate before committing. A stale filename is a plan defect — do not commit until the name matches the content.

In practice the more common case is different: plans are *created* with auto-generated placeholder slugs (this very file's `wobbly-bachman` suffix is a live example) and never renamed because the purpose hasn't "shifted" — it was simply never well-named in the first place. The rule as written doesn't cover that case, so junk filenames slip through to commit.

The user wants the rule to **always** require a meaningful `verb-target` filename, not only when the plan's purpose changes.

## Objective

Tighten Workflow §3 in [plan-mode.md](../../plan-mode.md) so it requires a meaningful `verb-target` kebab-case filename on **every** plan before commit — covering both (a) initial creation with an auto-generated/placeholder slug and (b) the existing purpose-shifted case.

## Steps

1. **Edit Workflow §3 (`Rename`) in `plan-mode.md`** to require a meaningful filename in two scenarios, not just one: (a) when the initial filename is auto-generated, placeholder, or otherwise non-descriptive, and (b) when the plan's purpose shifts after creation. Reference back to the `verb-target` kebab-case convention already defined in §1 (`Create`) as the authoritative shape, and keep the existing "stale filename is a plan defect — do not commit until the name matches the content" closing clause.
   - *Why:* Closes the gap where auto-generated slugs (e.g. `wobbly-bachman`) survive to commit because the plan's *purpose* never shifted — it just never had a real name. Reusing §1's `verb-target` convention avoids duplicating the naming spec in two places.
   - *Verify:* Re-read [plan-mode.md](../../plan-mode.md) §3 and confirm it (1) names both the placeholder-name and purpose-shift cases, (2) refers to the §1 `verb-target` kebab-case convention rather than restating it, (3) retains the "stale filename is a plan defect" closing clause.

2. **Leave Workflow numbering and all other sections unchanged.** Do not insert a new step; the change is a tightening of the existing §3, not an addition.
   - *Why:* The skeleton, status skill, and any downstream tooling reference these workflow positions implicitly via the file's shape. Renumbering would create unnecessary churn.
   - *Verify:* Diff the file — the only changed lines should be inside Workflow §3; the count of numbered workflow items remains 6 (§0 through §5).

## Acceptance Criteria

- [ ] `plan-mode.md` Workflow §3 explicitly requires a meaningful `verb-target` filename when the initial name is auto-generated, placeholder, or non-descriptive — not only when purpose shifts.
- [ ] §3 points to §1's `verb-target` kebab-case convention rather than restating naming rules.
- [ ] §3 retains the "stale filename is a plan defect — do not commit until the name matches the content" closing clause.
- [ ] No other section of `plan-mode.md` (When to plan, §0–§2, §4–§5, Required Structure, Writing Style, Skeleton) is altered.
- [ ] [reference/SKELETON.md](../../reference/SKELETON.md) is **not** modified — the skeleton is filename-agnostic and the rule lives in `plan-mode.md`.

## Verification

- Open [plan-mode.md](../../plan-mode.md) and read Workflow §3. It must name both triggers (placeholder-name on creation, and purpose-shift later), point back to §1's `verb-target` convention, and keep the "stale filename is a plan defect" closing clause.
- Diff the file and confirm only §3 changed; §0–§2 and §4–§5 are byte-identical to the prior version.
- Mentally walk a fresh plan through the workflow: a plan created at `something-wobbly-bachman.md` should now be flagged by §3 as needing a rename to `verb-target` form *before* commit, even though its purpose has not shifted.
- Re-read this plan file's own opening note — it serves as the canonical worked example of the rule being enforced.

## Next Steps *(optional)*

- Backfill meaningful filenames across existing plans:
  ```text
  Scan every plan file under ~/.claude/rules/docs/plans/ and identify any whose filename contains an auto-generated suffix (e.g. two-word random slugs like `wobbly-bachman`, `feigenbaum`, `teacup`, `bachman`) or otherwise fails the `verb-target` kebab-case convention from plan-mode.md §1. For each, propose a meaningful `verb-target` rename derived from the plan's title and Objective section. Do not rename anything yet — report a table of (current filename → proposed filename → one-sentence rationale) so the user can approve or adjust in bulk.
  ```

- Enforce the rule with a PreCommit / PostToolUse hook:
  ```text
  Draft the minimum-viable hook that prevents committing a plan file under docs/plans/ whose filename does not match the `verb-target` kebab-case convention in plan-mode.md §1. The hook should (a) only fire on .md files under docs/plans/, (b) skip files whose frontmatter `status: completed` (already-shipped plans shouldn't be retroactively blocked), (c) heuristically detect placeholder slugs (e.g. trailing two-word random pairs like `wobbly-bachman`) and reject them with a clear message pointing to plan-mode.md §3. Recommend PreToolUse on Bash(git commit*) vs. a Git pre-commit hook and justify the choice.
  ```
