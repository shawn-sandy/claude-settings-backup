---
description: Plan mode rules — when to plan, when to skip planning, and scope discipline. Document structure lives in plan-authoring.md.
---

# Plan Mode Instructions

## When to plan

- **Assess first.** Only plan if the change spans multiple files or has unclear requirements. For a
  single file, a simple fix, a typo, or a missing dep, call `ExitPlanMode` immediately and apply the
  change directly. Never produce a plan document for requests below this threshold.
- When a skill or slash command requires write operations (git, filesystem, migrations), **do not**
  enter plan mode. Execute directly.
- Do not add friction to well-specified requests. If the objectives are already clear, skip
  clarification and draft.

## Workflow

1. **Clarify** — If objectives are ambiguous or have open requirements, use `AskUserQuestion` to
   resolve them before drafting.
2. **Author** — Follow `~/.claude/rules/plan-authoring.md` for location, filename, frontmatter,
   required sections, and writing style. It auto-loads inside a plans directory; read it directly
   if it has not.
3. **Approve** — Request approval via `ExitPlanMode`. Never implement until the user explicitly
   approves.
