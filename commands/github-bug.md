---
description: Create a detailed bug report with reproduction steps and environment info
argument-hint: [component/area] [brief description] - e.g., "Button hover state not working"
allowed-tools: Bash(gh *, node --version, npm --version), Grep, Read, LS
---

# Bug Report Generator

Create a comprehensive bug report with structured information, reproduction steps, and environment details.

## Instructions:

1. **Validate GitHub Connection**:
   - Check if `gh` CLI is installed and authenticated using `gh auth status`
   - Verify we're in the correct repository with `gh repo view`
   - Exit with error if GitHub connection fails

2. **Parse the issue**: Extract the component/area and description from `$ARGUMENTS`

3. **Gather environment information**:
   - Node.js version using `node --version`
   - npm version using `npm --version`
   - Browser information (if applicable)
   - Project dependencies from package.json

4. **Analyze the component/area**:
   - Find related source files
   - Check for recent changes (git log)
   - Look for existing tests
   - Search for similar issues using `gh issue list`

5. **Generate structured bug report**:
   - Clear title with [BUG] prefix
   - Problem description
   - Steps to reproduce
   - Expected vs actual behavior
   - Environment information
   - Related files and code references
   - Screenshots/logs section (if applicable)

6. **Create the GitHub issue** using `gh issue create` with:
   - Appropriate labels: bug, needs-investigation, component-specific labels
   - Structured bug report format
   - Environment details

7. **Verify creation and provide feedback**:
   - Confirm the bug report was created successfully on GitHub
   - Display the GitHub issue URL
   - Show issue number and status

## Usage Examples:
- `/github-bug Button Component not rendering properly on Safari`
- `/github-bug Form validation Form submission fails with empty required fields`
- `/github-bug Storybook Stories not loading in development mode`

Arguments: $ARGUMENTS

---

Let me create a detailed bug report for: **$ARGUMENTS**

**IMPORTANT**: This command will create an actual GitHub issue with a structured bug report. I'll first validate the GitHub connection, gather environment information, and then create the bug report directly on GitHub.

Starting with GitHub validation and environment analysis...