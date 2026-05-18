---
description: Create a feature request with user stories, acceptance criteria, and implementation considerations
argument-hint: [feature name] [brief description] - e.g., "Dark mode Add theme switching capability"
allowed-tools: Bash(gh *), Grep, Read, LS
---

# Feature Request Generator

Create a comprehensive feature request with user stories, acceptance criteria, and implementation considerations based on the project's architecture.

## Instructions:

1. **Validate GitHub Connection**:
   - Check if `gh` CLI is installed and authenticated using `gh auth status`
   - Verify we're in the correct repository with `gh repo view`
   - Exit with error if GitHub connection fails

2. **Parse the feature request**: Extract feature name and description from `$ARGUMENTS`

3. **Analyze project context**:
   - Review existing component patterns from @CLAUDE.md
   - Check current architecture and conventions
   - Look for similar existing features using `gh issue list`
   - Identify affected components and areas

4. **Research implementation approach**:
   - Review existing component structure
   - Check TypeScript patterns and interfaces
   - Look at styling conventions (SCSS)
   - Consider accessibility requirements (WCAG 2.1)
   - Review testing patterns

5. **Generate structured feature request**:
   - Clear title with [FEATURE] prefix
   - User story format ("As a... I want... So that...")
   - Detailed description and rationale
   - Acceptance criteria checklist
   - Implementation considerations
   - Affected components/files
   - Design considerations (if UI-related)
   - Testing requirements
   - Documentation needs

6. **Create the GitHub issue** using `gh issue create` with:
   - Labels: feature, enhancement, needs-design (if applicable)
   - Structured feature request format
   - Implementation considerations

7. **Verify creation and provide feedback**:
   - Confirm the feature request was created successfully on GitHub
   - Display the GitHub issue URL
   - Show issue number and status

## Usage Examples:
- `/github-feature Search Add search functionality to component library`
- `/github-feature Dark-mode Add theme switching with light/dark modes`
- `/github-feature Accessibility Improve keyboard navigation for all components`

Arguments: $ARGUMENTS

---

Let me create a comprehensive feature request for: **$ARGUMENTS**

**IMPORTANT**: This command will create an actual GitHub issue with a structured feature request. I'll first validate the GitHub connection, analyze the project architecture, and then create the feature request directly on GitHub.

Starting with GitHub validation and project analysis...