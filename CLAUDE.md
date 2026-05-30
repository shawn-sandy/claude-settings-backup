# CLAUDE.md — Global Instructions

Project-specific `CLAUDE.md` and `./.claude/rules/` **override** these global instructions when they conflict. Check both before acting on unfamiliar projects.

## Search Exclusions

- Never include `*/plans/archive` (any depth) in file searches, glob patterns, or exploratory reads. Skip it unless the user explicitly targets it by path.

## Working Style

- No emojis in generated markdown.
- Never autonomously start additional work after completing a requested task.
- Never expand scope beyond the specified file or target.

## Git & PRs

- Commit ALL modified files in a single commit unless explicitly told otherwise — do not leave uncommitted files requiring a second prompt.
- Confirm not on a protected branch before committing.
- Check if a feature branch is already merged before creating a PR.
- Follow the project's commit message conventions; reference relevant issues/tickets.
- Update docs and changelogs when creating a PR.
- Execute git operations directly — do not enter plan mode for git commands.
- `git-agent` skills (`branch-agent`, `commit-agent`, `pr-agent`, `ship`) self-bootstrap out of plan mode via their own Step 0 (`ExitPlanMode`). Callers do not pre-check plan-mode state.

## Planning

When in plan mode, never implement until the user explicitly approves the plan.

## Debugging

Investigate root cause first — use Chrome DevTools, database queries, or runtime inspection to understand actual state before writing code. Do not guess iteratively.

## Skills

- **graphify** (`~/.claude/skills/graphify/SKILL.md`) — any input to knowledge graph. Trigger: `/graphify`
  When the user types `/graphify`, invoke the Skill tool with `skill: "graphify"` before doing anything else.

## Tips

- Press `#` during any session to have Claude auto-incorporate session learnings into CLAUDE.md.
