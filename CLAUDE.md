# CLAUDE.md — Global AI Assistant Instructions

This file provides baseline guidance for Claude Code (claude.ai/code) when working with code in any repository.

**Project-specific instructions OVERRIDE these global instructions when they conflict.**

Always check `./CLAUDE.md` and `./.claude/rules/` before acting on unfamiliar projects.

## Global Guidelines

### General Behavior

- Don't use emojis when creating markdown unless absolutely necessary
- Do what has been asked; nothing more, nothing less
- When the user asks you to do something, DO IT. Do not over-plan, ask excessive clarifying questions, or spend time exploring when the task is clear. If the user asks for a migration, generate the migration. If they ask for a fix, fix it.
- NEVER create files unless they're absolutely necessary for achieving your goal
- ALWAYS prefer editing an existing file to creating a new one
- NEVER proactively create documentation files (\*.md) or README files unless explicitly requested

### Behavioral Rules

- NEVER autonomously start additional work after completing a requested task
- NEVER expand scope beyond the specified file or target
- ALWAYS execute git operations directly without entering plan mode (unless asked)
- ALWAYS confirm not on a protected branch before committing
- ALWAYS check if a feature branch is already merged before creating a PR

### Pull/Merge Requests

- When creating a pull/merge request, update the necessary docs and changelogs to reflect new changes and features
- Follow the project's commit message conventions (check existing commits)
- Reference relevant issues/tickets in commit messages

### Project-Specific Guides

- When documentation is requested, check for project-specific documentation tools
- Follow the project's documentation structure and conventions

---

## Git Workflow

When asked to commit changes, always stage and commit ALL modified files in a single commit unless explicitly told otherwise. Do not leave uncommitted files requiring a second prompt.

## Planning & Implementation

When in plan mode, NEVER start implementing code until the user explicitly approves the plan. Present the plan, ask for approval, and wait. Do not exit plan mode on your own.

git-agent skills (`branch-agent`, `commit-agent`, `pr-agent`, `ship`) self-bootstrap out of plan mode via their own Step 0 (`ExitPlanMode`). Callers do not need to pre-check plan-mode state before invoking these skills.

## Debugging

When asked to fix a bug, investigate the root cause FIRST before attempting fixes. Use Chrome DevTools, database queries, or runtime inspection to understand the actual state before writing code. Do not guess at fixes iteratively.

---

## Security Reminders

- Never commit sensitive information (API keys, passwords, tokens)
- Validate and sanitize user input
- Check authentication/authorization before protected operations
- Follow principle of least privilege

---

## Testing

- Write tests for new functionality when test infrastructure exists
- Update existing tests when modifying code
- Follow project's testing conventions (check existing test files)

---

## When In Doubt

1. **Check project-specific instructions** (CLAUDE.md, CLAUDE-PATTERNS.md, etc.)
2. **Review existing code** for similar patterns
3. **Ask the user** for clarification before making assumptions
4. **Prefer consistency** over personal preference

---

## Skills

- **graphify** (`~/.claude/skills/graphify/SKILL.md`) — any input to knowledge graph. Trigger: `/graphify`
  When the user types `/graphify`, invoke the Skill tool with `skill: "graphify"` before doing anything else.

## Tips

- Press `#` during any session to have Claude auto-incorporate session learnings into CLAUDE.md
