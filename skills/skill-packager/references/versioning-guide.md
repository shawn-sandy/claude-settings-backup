# Semantic Versioning Guide for Claude Code Skills

This guide explains how to apply semantic versioning (semver) principles to Claude Code skills, helping you choose the appropriate version number when packaging your skills.

## What is Semantic Versioning?

Semantic Versioning is a versioning scheme that uses a three-part number: `MAJOR.MINOR.PATCH`

```
1.2.3
│ │ │
│ │ └─ PATCH: Bug fixes, documentation updates
│ └─── MINOR: New features, backward-compatible changes
└───── MAJOR: Breaking changes, major refactors
```

## Automated Version Management (New!)

The skill-packager now supports **automatic version incrementing** with sensible defaults:

### Default Behavior: Minor Increment

By default, the packager automatically bumps the **MINOR** version when you don't specify an explicit version:

```bash
# Current version: 1.2.3
python scripts/package_and_document.py --skill-path ./my-skill --output-dir ./output
# → Automatically creates version 1.3.0
```

**Why minor by default?**
- Most skill updates add features or improvements (minor changes)
- Safer than major bumps (no breaking changes)
- More significant than patch (typically more than just bug fixes)

### Bump Type Options

You can specify the type of version bump:

```bash
# Patch bump: 1.2.3 → 1.2.4 (bug fixes only)
--bump-type patch

# Minor bump: 1.2.3 → 1.3.0 (new features) [DEFAULT]
--bump-type minor

# Major bump: 1.2.3 → 2.0.0 (breaking changes) [REQUIRES CONFIRMATION]
--bump-type major
```

### Major Version Safeguard

**Major version bumps require explicit confirmation** to prevent accidental breaking changes:

Before executing `--bump-type major`, the skill will prompt:
> "This will create a MAJOR version bump (breaking change). Are you sure this release includes breaking changes or major refactoring?"

Only proceed if you genuinely have breaking changes.

### Explicit Version Override

For full control, you can specify an exact version:

```bash
# Explicit version (bypasses auto-increment)
python scripts/package_and_document.py \
  --skill-path ./my-skill \
  --version 2.0.0 \
  --output-dir ./output
```

Use explicit versions when:
- Correcting a version mistake
- Jumping to a specific version for organizational reasons
- The auto-increment doesn't match your needs

## Version Number Components

### MAJOR Version (X.0.0)

Increment the MAJOR version when you make **incompatible or breaking changes** that require users to modify how they use the skill.

**Examples of MAJOR changes:**
- Complete workflow restructuring
- Removing or renaming required fields in frontmatter
- Changing the skill's core purpose or domain
- Removing bundled scripts or resources that users depend on
- Changing script interfaces (parameters, return values)
- Incompatible changes to asset templates
- Removing support for previously supported use cases

**Version Examples:**
- `0.9.0` → `1.0.0` (first stable release)
- `1.5.3` → `2.0.0` (breaking workflow change)
- `2.1.0` → `3.0.0` (removed critical script)

**When to bump MAJOR:**
```
❓ Will users need to change how they invoke or use the skill?
❓ Are existing users' workflows broken by this change?
❓ Did you remove functionality that users relied on?

✅ Yes to any? → MAJOR version bump
```

### MINOR Version (x.Y.0)

Increment the MINOR version when you add **new functionality** in a **backward-compatible** manner.

**Examples of MINOR changes:**
- Adding new workflow steps or options
- Adding optional fields to frontmatter
- Adding new scripts to the `scripts/` directory
- Adding new references to the `references/` directory
- Adding new templates to `assets/`
- Enhancing existing features without breaking them
- Adding new use cases to the skill's capabilities
- Improving validation or error handling

**Version Examples:**
- `1.0.0` → `1.1.0` (added new optional feature)
- `1.1.0` → `1.2.0` (added helper script)
- `2.3.1` → `2.4.0` (added new workflow option)

**When to bump MINOR:**
```
❓ Are you adding new capabilities or features?
❓ Will the skill do more than before?
❓ Are the changes completely optional?

✅ Yes to any? → MINOR version bump
```

### PATCH Version (x.y.Z)

Increment the PATCH version for **bug fixes** and **backward-compatible corrections** that don't add new features.

**Examples of PATCH changes:**
- Fixing typos in SKILL.md or documentation
- Correcting errors in workflow instructions
- Fixing bugs in scripts
- Improving error messages
- Updating references with corrections
- Performance improvements without feature changes
- Documentation updates and clarifications
- Fixing validation logic bugs

**Version Examples:**
- `1.0.0` → `1.0.1` (fixed typo in docs)
- `1.2.0` → `1.2.1` (fixed script bug)
- `2.3.4` → `2.3.5` (improved error message)

**When to bump PATCH:**
```
❓ Are you fixing something that was broken?
❓ Are you improving docs or error messages?
❓ Is the skill more correct but not more capable?

✅ Yes to any? → PATCH version bump
```

## Special Version Numbers

### Pre-1.0 Versions (0.y.z)

Initial development versions. Use these when the skill is still under active development and not yet considered stable.

**Characteristics:**
- Major changes can happen in MINOR versions
- Breaking changes are acceptable
- API/workflow is not yet stable
- For experimental or beta skills

**Progression:**
```
0.1.0 → Initial release
0.2.0 → Added features
0.3.0 → Major refactor (OK in 0.x)
0.9.0 → Release candidate
1.0.0 → First stable release
```

### Version 1.0.0

This is your first **stable, production-ready** release. Use 1.0.0 when:

- The skill is feature-complete for its primary use case
- The workflow is well-tested and stable
- You're confident in the skill's interface
- You're ready to maintain backward compatibility

**Don't rush to 1.0.0!** It's okay to stay in 0.x for a while during development.

## Decision Tree for Version Bumps

When packaging a skill, use this decision tree to choose the appropriate bump type:

```
START: What changed since the last version?

1. Did you remove or break existing functionality?
   YES → Use --bump-type major (requires confirmation)
   NO → Go to 2

2. Did you add new features or capabilities?
   YES → Use default (no flag) or --bump-type minor
   NO → Go to 3

3. Did you only fix bugs or improve documentation?
   YES → Use --bump-type patch
   NO → Keep current version (re-package with same version)
```

**In practice:**

- **Most releases**: Just run without flags (defaults to minor)
- **Bug fixes only**: Add `--bump-type patch`
- **Breaking changes**: Add `--bump-type major` (will prompt for confirmation)
- **Special cases**: Use `--version X.Y.Z` for explicit control

## Practical Examples for Skills

### Example 1: Documentation Fix

**Changes:**
- Fixed typo in SKILL.md
- Updated example in references/

**Version Decision:**
- Current: `1.2.3`
- New: `1.2.4` (PATCH)

**Reasoning:** Bug fix, no new features, no breaking changes.

### Example 2: Adding Helper Script

**Changes:**
- Added new script to automate validation
- Updated SKILL.md to mention new script
- Script is optional, doesn't change existing workflow

**Version Decision:**
- Current: `1.2.4`
- New: `1.3.0` (MINOR)

**Reasoning:** New feature (script), backward-compatible, existing workflows still work.

### Example 3: Workflow Restructure

**Changes:**
- Completely reorganized the workflow steps
- Changed how the skill is invoked
- Users must adapt their usage

**Version Decision:**
- Current: `1.3.0`
- New: `2.0.0` (MAJOR)

**Reasoning:** Breaking change, existing users must update how they use the skill.

### Example 4: First Stable Release

**Changes:**
- Tested thoroughly in 0.9.x
- Confident in workflow stability
- Ready to commit to backward compatibility

**Version Decision:**
- Current: `0.9.5`
- New: `1.0.0` (MAJOR)

**Reasoning:** First stable release, signal production readiness.

## Best Practices

### 1. Use Auto-Increment (Default to Minor)

Let the packager handle version bumping automatically:
- For most releases, use the default (no `--version` or `--bump-type` flag)
- The default minor bump is appropriate for most skill updates
- Only use explicit versions when necessary

### 2. Start with 0.1.0

For new skills, start with version `0.1.0` rather than `1.0.0`. This signals that the skill is still under development.

### 3. Be Cautious with Major Bumps

The packager requires confirmation for major version bumps for a reason:
- Major bumps signal breaking changes to users
- Only use `--bump-type major` when you truly have breaking changes
- If possible, make changes backward-compatible and use minor instead

### 4. Document Changes

Keep track of what changed between versions. Consider maintaining a changelog in your skill directory (though not strictly required).

### 5. Reset Lower Numbers (Automatic)

The auto-increment handles this automatically:
- `1.2.3` → `2.0.0` (not `2.2.3`) when using `--bump-type major`
- `1.2.3` → `1.3.0` (not `1.3.3`) when using default or `--bump-type minor`

### 6. Don't Skip Numbers

Increment by 1 only. Don't jump from `1.0.0` to `1.5.0` or `3.0.0`. The auto-increment enforces this automatically.

### 7. When in Doubt, Use Default

If you're unsure what version bump to use:
- Default (minor) is usually correct for most updates
- If only fixing bugs → use `--bump-type patch`
- If breaking compatibility → use `--bump-type major` (will prompt for confirmation)
- Think about existing users: would they need to change anything?

### 8. Pre-release Tags (Optional)

For advanced use, you can use pre-release tags:
- `1.0.0-alpha`
- `1.0.0-beta.1`
- `1.0.0-rc.1`

These are considered less stable than the release version.

## Version Lifecycle Example

Here's a realistic version progression for a skill:

```
0.1.0  - Initial release, basic functionality
0.2.0  - Added validation script
0.2.1  - Fixed bug in validation
0.3.0  - Added reference documentation
0.3.1  - Updated docs with examples
0.9.0  - Feature-complete, testing phase
0.9.1  - Bug fixes from testing
1.0.0  - First stable release
1.0.1  - Documentation improvements
1.1.0  - Added optional helper script
1.1.1  - Fixed script bug
1.2.0  - Added new workflow option
2.0.0  - Major workflow restructure
```

## Versioning SKILL.md Frontmatter

Always keep the version in your SKILL.md frontmatter in sync with your package version:

```yaml
---
name: my-skill
description: Does something useful
version: 1.2.3
---
```

The skill-packager tool will update this automatically when packaging.

## FAQ

**Q: I forgot to bump the version. What do I do?**
A: Package with the correct new version. The old version remains in the downloads directory.

**Q: Can I go backwards in version numbers?**
A: No, version numbers should always increase. If you need to "undo" changes, create a new version.

**Q: What if I have multiple changes (bug fix + new feature)?**
A: Use the highest applicable version bump (MINOR in this case, since new feature > bug fix).

**Q: Should I version the templates?**
A: No, templates are part of the skill-packager skill itself. Version the packaged skill.

**Q: What about build metadata (+)?**
A: For simplicity, stick to MAJOR.MINOR.PATCH for skills. Build metadata is optional.

## Summary

**Quick Reference:**
- **MAJOR** (x.0.0): Breaking changes [REQUIRES CONFIRMATION]
- **MINOR** (x.y.0): New features, backward-compatible [DEFAULT]
- **PATCH** (x.y.z): Bug fixes, documentation

**Automated Versioning:**
- **Default**: Auto-increment minor version (no flags needed)
- **Bug fixes**: Use `--bump-type patch`
- **Breaking changes**: Use `--bump-type major` (requires confirmation)
- **Custom**: Use `--version X.Y.Z` for explicit control

**Decision Process:**
1. Breaking changes? → `--bump-type major` (will prompt)
2. New features? → Default (or `--bump-type minor`)
3. Bug fixes/docs? → `--bump-type patch`
4. No changes? → Keep version (re-package)

**Start at:** `0.1.0` (auto-assigned if no version exists)
**First stable:** `1.0.0`
**Always increment:** By 1 only (enforced automatically)

---

For more information on semantic versioning, see https://semver.org/
