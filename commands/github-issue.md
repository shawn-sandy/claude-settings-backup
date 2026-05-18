---
description: Create a GitHub issue with intelligent analysis and formatting
argument-hint: [type] [title] - e.g., "bug Login form validation" or "feature Dark mode toggle"
allowed-tools: Bash(gh *), Grep, Read, LS
---

# GitHub Issue Creator

Create a comprehensive GitHub issue based on the provided type and title. Analyze the codebase context to provide relevant details, labels, and formatting.

## Instructions:

1. **Validate GitHub Connection**:
   - Check if `gh` CLI is installed and authenticated using `gh auth status`
   - Verify we're in the correct repository with `gh repo view`
   - Exit with error if GitHub connection fails

2. **Parse the arguments**: Extract issue type (bug, feature, enhancement, docs, chore) and title from `$ARGUMENTS`

3. **Analyze codebase context**: 
   - Search for related files and components
   - Check existing patterns and conventions from @CLAUDE.md
   - Look for similar existing issues/PRs using `gh issue list`

4. **Generate intelligent content**:
   - Create a detailed description based on the issue type
   - Suggest appropriate labels based on content analysis
   - Include relevant code references where applicable

5. **Create the GitHub issue** using `gh issue create` with:
   - Well-formatted title
   - Comprehensive description with sections appropriate to issue type
   - Relevant labels (bug, feature, enhancement, etc.)
   - References to related files/components

6. **Verify creation and provide feedback**:
   - Confirm the issue was created successfully
   - Display the GitHub issue URL
   - Show issue number and status

## Usage Examples:
- `/github-issue bug Button component not responsive on mobile`
- `/github-issue feature Add search functionality to component library`
- `/github-issue enhancement Improve TypeScript types for Form components`

Arguments: $ARGUMENTS

---

Let me create a GitHub issue for: **$ARGUMENTS**

**IMPORTANT**: This command will create an actual GitHub issue. I'll first validate the GitHub connection, then analyze the codebase and create the issue directly on GitHub.

Starting with GitHub validation and codebase analysis...