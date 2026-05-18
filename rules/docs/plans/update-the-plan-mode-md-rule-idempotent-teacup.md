# Plan: Require per-step verification in plan-mode.md

## Context

The current [plan-mode.md](../../plan-mode.md) rule defines each step in a plan's `<ol>` as "a single, testable action with a brief *why*." It also defines a top-level `verification` section that covers the whole plan.

There is no requirement for each individual step to state how to confirm that step succeeded. In practice this means a plan's per-step "why" can drift away from being checkable — leaving plan-level verification to carry the entire load. The user wants per-step verification to be mandatory so each step is self-validating before moving on.

## Objective

Update [plan-mode.md](../../plan-mode.md) so the `steps` section requires every `<li>` to include a verification — i.e. each step must specify how to confirm it succeeded, not just what to do and why.

## Files to modify

- [/Users/shawnsandy/.claude/rules/plan-mode.md](../../plan-mode.md) — single file, single bullet under the **Required Structure** section.

## Steps

1. **Edit the `steps` bullet under Required Structure** to require three pieces per `<li>`: the action, a brief *why*, and a brief *verify* (how to confirm the step succeeded).
   - Verify: re-read the file and confirm the `steps` bullet now names all three (action, why, verify).

2. **Add a one-line clarifying note** distinguishing per-step verification (did this step do what it should?) from the top-level `verification` section (did the whole change achieve the goal?), so they don't become redundant.
   - Verify: the `verification` bullet still describes end-to-end confirmation, and the new `steps` bullet describes step-local confirmation.

## Verification

- Open [plan-mode.md](../../plan-mode.md) and confirm:
  - The `steps` bullet under **Required Structure** explicitly requires a verification per step.
  - The top-level `verification` bullet remains unchanged in intent (end-to-end confirmation).
  - No other sections (Workflow, File Format, Writing Style, Scope Discipline) are altered.
- Spot-check by mentally drafting a plan against the new rule: each `<li>` should now naturally include "do X, because Y, confirmed by Z."

## Next steps (out of scope)

- Backfill per-step verification into existing plans under `docs/plans/`.
- Update any plan-generating skills/templates that produce `<li>` items, so they emit the new three-part structure by default.
