# Team Commit Message Generator

Create a conventional commit message following our team standards:

## Requirements
1. Use conventional commit format: `type(scope): description`
2. Types: feat, fix, docs, style, refactor, test, chore, ci, perf
3. Scope should be one of: api, ui, auth, db, config, deps, core, tests
4. Description: imperative mood, lowercase, no period, max 50 chars
5. Body: detailed explanation of changes (if needed)
6. Footer: list changed files and reference tickets/issues

## Format Template
```
type(scope): brief description

Detailed explanation of what changed and why (optional)

- List specific changes made
- Include technical details
- Explain business impact if relevant

BREAKING CHANGE: describe any breaking changes (if applicable)

Files changed:
- path/to/file1.ext
- path/to/file2.ext

Closes: #123
```

## Validation Rules
- Subject line: 50 chars max
- Body lines: 72 chars max
- Use imperative mood ("add" not "added")
- Reference ticket numbers when available
- Include BREAKING CHANGE footer for breaking changes

## Examples

### Good Examples
```
feat(auth): add OAuth2 integration

Implement Google OAuth2 authentication flow with proper token handling
and refresh mechanism for improved user experience.

- Add OAuth2 service with Google provider
- Implement token refresh middleware
- Update login component with OAuth button
- Add user session persistence

Files changed:
- src/services/auth.js
- src/components/Login.jsx
- src/middleware/token.js

Closes: #456
```

```
fix(api): resolve user data validation error

Fix validation schema that was rejecting valid email formats
containing plus signs, affecting user registration.

Files changed:
- src/validators/user.js
- tests/validators/user.test.js

Fixes: #789
```

### Bad Examples
```
❌ Updated stuff
❌ fix: Fixed the bug in the thing
❌ Add new feature for users to login better
```

### Breaking Changes Example
```
feat(core)!: migrate to new authentication system

BREAKING CHANGE: The authentication API has changed. 
Users must re-authenticate and existing tokens are invalid.
Update client applications to use the new auth endpoints.

Files changed:
- src/auth/index.js
- docs/api.md
```

## Team Workflow Integration

### Ticket References
- Use `Closes: #123` for features that close issues
- Use `Fixes: #123` for bug fixes
- Use `Refs: #123` for partial work or related changes
- Use `Co-authored-by: Name <email>` for pair programming

### Code Review Requirements
- Commits should be atomic (one logical change per commit)
- Each commit should pass tests independently
- Use draft PRs with `WIP:` prefix for work in progress
- Squash commits before merging to main

### Branch Naming Convention
- `feat/ticket-number-brief-description`
- `fix/ticket-number-brief-description`
- `chore/brief-description`

## Scope Guidelines by Project Type

### Web Applications
- `ui` - User interface components, styling
- `api` - Backend API endpoints, routes
- `auth` - Authentication, authorization
- `db` - Database migrations, models
- `config` - Configuration changes
- `deps` - Dependency updates

### Libraries/Packages
- `core` - Core functionality
- `utils` - Utility functions
- `types` - Type definitions
- `docs` - Documentation
- `build` - Build system, packaging

### Monorepos
- Use package names: `@app/frontend`, `@app/backend`
- Or service names: `user-service`, `payment-service`

## Pre-Commit Validation

Before generating the commit message, verify:
- [ ] All tests pass
- [ ] Code follows linting rules
- [ ] No sensitive data (keys, passwords, tokens) included
- [ ] Breaking changes are documented
- [ ] Related documentation updated

## Quick Reference Card

| Type | Use For | Example |
|------|---------|---------|
| feat | New features | `feat(auth): add social login` |
| fix | Bug fixes | `fix(api): handle null user data` |
| docs | Documentation | `docs(readme): update setup guide` |
| style | Formatting, no logic change | `style(ui): fix button alignment` |
| refactor | Code improvement, no new features | `refactor(core): simplify validation logic` |
| test | Adding/updating tests | `test(auth): add OAuth flow tests` |
| chore | Maintenance tasks | `chore(deps): update React to v18` |
| ci | CI/CD changes | `ci(github): add automated testing` |
| perf | Performance improvements | `perf(api): optimize database queries` |

Generate the commit message with these standards, analyzing git status and git diff to understand all changes.