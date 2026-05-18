# Skill Packager

A Claude Code skill that packages custom skills into versioned distributable ZIP files with comprehensive documentation and semantic versioning support.

## Overview

The Skill Packager automates the process of packaging custom skills for distribution. It validates skill structure, generates installation and user documentation, creates versioned ZIP archives, and manages version increments according to semantic versioning principles.

This skill extends basic packaging with versioning, documentation generation, centralized distribution directories, and version history management.

## Features

- **Semantic Versioning Support** - Manage MAJOR.MINOR.PATCH versions automatically
- **Automatic Validation** - Validates skill structure before packaging
- **Installation Guide Generation** - Creates Download.md with installation instructions
- **User Documentation Generation** - Creates {SkillName}-doc.md with usage guide
- **Version History Management** - Preserves all previous versions in organized directories
- **Template-Based Documentation** - Uses customizable templates for consistent docs

## Installation

### Option 1: Install via gitpick (Recommended)

The fastest and easiest way to install directly from GitHub:

#### User-level installation (available in all projects)

```bash
npx gitpick shawn-sandy/acss/tree/main/.claude/skills/skill-packager ~/.claude/skills/skill-packager
```

#### Project-specific installation

```bash
cd /path/to/your/project
npx gitpick shawn-sandy/acss/tree/main/.claude/skills/skill-packager ./.claude/skills/skill-packager
```

**Why gitpick?**

- ✅ Single command - no ZIP download or extraction
- ✅ Selective cloning - only downloads the skill folder
- ✅ Zero dependencies - lightweight and fast (<35kb)
- ✅ Always up-to-date - pulls latest version from GitHub

**Learn more:** [github.com/nrjdalal/gitpick](https://github.com/nrjdalal/gitpick)

### Option 2: Manual Installation

1. Download or clone the skill files
2. Copy the `skill-packager` directory to your Claude skills location:

**For user-level installation:**
```bash
cp -r skill-packager ~/.claude/skills/
```

**For project-specific installation:**
```bash
cp -r skill-packager /path/to/your/project/.claude/skills/
```

3. Verify installation by checking that Claude Code recognizes the skill

### Option 3: Clone from GitHub

Clone the entire repository and copy the skill:

```bash
# Clone the repository
git clone https://github.com/shawn-sandy/acss.git

# Copy the skill to your Claude skills directory
cp -r acss/.claude/skills/skill-packager ~/.claude/skills/
```

### Option 4: Install from ZIP Package

If you have a packaged ZIP file:

1. Extract the ZIP file
2. Move the extracted `skill-packager` folder to `~/.claude/skills/` (user-level) or `./.claude/skills/` (project-specific)
3. Restart Claude Code to recognize the new skill

## When to Use This Skill

Invoke this skill when you need to:

- Package a skill for sharing with other users
- Create a versioned release of a skill
- Generate installation and usage documentation
- Archive skill versions for distribution
- Update an existing skill package with a new version

## Workflow Overview

### Step 1: Skill Selection and Validation

**Action:** Provide the path to the skill directory or paste the SKILL.md content.

**Validation Checks:**
- Verify SKILL.md exists
- Validate YAML frontmatter format
- Confirm required fields: `name` and `description`
- Check naming conventions (hyphen-case, lowercase, max 40 chars)
- Verify version field (add if missing, default to 0.1.0)

**Error Handling:**
- Report specific errors if validation fails
- Suggest corrections for common issues
- Offer to fix minor issues automatically

### Step 2: Download Directory Selection

**Prompt for Download Location:**

- **Default:** `{current-working-directory}/downloads/{skill-name}/`
- Display the full path that will be used
- Allow user to accept default or specify custom base directory
- Validate path is writable and accessible

**Directory Structure:**
```
{base-dir}/{skill-name}/
├── {skill-name}-v0.1.0.zip
├── {skill-name}-v0.2.0.zip (if previous versions exist)
├── {skill-name}-Download.md (updated with latest version)
└── {skill-name}-doc.md (updated with latest version)
```

### Step 3: Version Management

**Read Current Version:**
- Extract from SKILL.md frontmatter
- Parse as semantic version (MAJOR.MINOR.PATCH)
- Display current version to user

**Determine New Version:**

Choose version action:
- **Keep current** - Use existing version (for re-packaging)
- **Patch increment** - Bug fixes, docs (0.1.0 → 0.1.1)
- **Minor increment** - New features, backward-compatible (0.1.0 → 0.2.0)
- **Major increment** - Breaking changes (0.1.0 → 1.0.0)
- **Custom version** - User specifies exact version

**Version Validation:**
- Ensure format is MAJOR.MINOR.PATCH (e.g., 1.2.3)
- Warn if new version is lower than current
- Confirm with user if version seems unusual

### Step 4: Documentation Generation

**Generate Download.md (Installation Instructions):**

Uses `templates/download_template.md` to create:
- Skill name and version
- Prerequisites and requirements
- Installation steps (extract ZIP, copy to skills directory)
- Verification steps
- Compatibility notes
- Next steps

**Generate {SkillName}-doc.md (User Documentation):**

Uses `templates/doc_template.md` to create:
- Skill overview and purpose
- When to use this skill
- Usage instructions and workflow
- Examples and common use cases
- Troubleshooting tips
- Reference to bundled resources

**Template Variables:**
- `{{SKILL_NAME}}` - Skill name from frontmatter
- `{{SKILL_VERSION}}` - Current version being packaged
- `{{SKILL_DESCRIPTION}}` - Description from frontmatter
- `{{INSTALLATION_DATE}}` - Current date in ISO format
- `{{SKILL_DIR_NAME}}` - Directory name of the skill

### Step 5: Package Creation

**Execute Packaging Script:**

```bash
python scripts/package_and_document.py \
  --skill-path /path/to/skill \
  --version 1.0.0 \
  --output-dir ./downloads/my-skill
```

**Script Responsibilities:**
- Validate skill structure
- Create ZIP file: `{skill-name}-v{version}.zip`
- Include all skill files (SKILL.md, scripts/, references/, assets/, LICENSE.txt)
- Exclude unnecessary files (.DS_Store, __pycache__, *.pyc, .git)
- Maintain directory structure within ZIP
- Generate checksums (SHA-256) for integrity verification

**Output Files:**
```
downloads/my-skill/
├── my-skill-v1.0.0.zip
├── my-skill-Download.md
└── my-skill-doc.md
```

### Step 6: Update Skill Metadata

**Update SKILL.md Frontmatter:**

Replace version field with new version number while preserving all other fields.

**Example Update:**
```yaml
# Before
---
name: my-skill
description: Does something useful
version: 0.1.0
---

# After
---
name: my-skill
description: Does something useful
version: 1.0.0
---
```

### Step 7: Package Summary

**Display Summary:**
```
✓ Skill packaged successfully!

Package Details:
- Skill: my-skill
- Version: v1.0.0
- Location: ./downloads/my-skill/

Generated Files:
- my-skill-v1.0.0.zip (2.3 MB)
- my-skill-Download.md (installation guide)
- my-skill-doc.md (user documentation)

Updated:
- SKILL.md frontmatter (version: 1.0.0)

Previous Versions:
- v0.1.0 (still available)
```

**Next Steps:**
- Share the ZIP file with others
- Distribute Download.md for installation instructions
- Provide doc.md for usage guidance
- Consider publishing to a skill registry

## Semantic Versioning

Skills use semantic versioning (MAJOR.MINOR.PATCH):

### When to Increment

**PATCH (X.Y.Z+1)** - Bug Fixes and Documentation
- Bug fixes in existing functionality
- Documentation updates
- Typo corrections
- No new features or breaking changes

**MINOR (X.Y+1.0)** - New Features (Backward Compatible)
- New functionality added
- New bundled resources (scripts, references)
- Enhancements to existing features
- Deprecation notices (not removal)
- Backward compatible changes

**MAJOR (X+1.0.0)** - Breaking Changes
- Incompatible API/workflow changes
- Removal of functionality
- Significant refactoring requiring user changes
- Changes to SKILL.md structure that affect usage

### Version Examples

```
0.1.0 → 0.1.1  (Patch: Fixed validation script bug)
0.1.1 → 0.2.0  (Minor: Added new reference guide)
0.2.0 → 1.0.0  (Major: Redesigned workflow structure)
```

## Bundled Resources

### Scripts

**package_and_document.py** - Main packaging automation script

**Usage:**
```bash
python scripts/package_and_document.py \
  --skill-path <path/to/skill> \
  --version <X.Y.Z> \
  --output-dir <output-directory>
```

**Responsibilities:**
- ZIP creation with proper file organization
- Validation before packaging
- Documentation generation from templates
- Version numbering in filenames
- Checksum generation

### Templates

**download_template.md** - Installation instructions template

Contains placeholders for:
- Skill name and version
- Installation steps
- Prerequisites
- Compatibility notes

**doc_template.md** - User documentation template

Contains placeholders for:
- Skill overview
- Usage instructions
- Examples
- Troubleshooting

### References

**versioning-guide.md** - Semantic versioning guidelines

Detailed guide covering:
- When to use MAJOR vs MINOR vs PATCH
- Examples and best practices
- Version increment decision tree
- Breaking change identification

## Error Handling and Edge Cases

### Missing Version Field

- Offer to add version field to SKILL.md
- Suggest starting at 0.1.0 for initial packages
- Update frontmatter before packaging

### Duplicate Version

- Warn if version already exists in downloads directory
- Offer to increment automatically or overwrite
- Confirm action with user

### Invalid Skill Structure

- Report validation errors clearly
- Suggest fixes based on skill-creator guidelines
- Do not proceed until fixed

### Large File Sizes

- Warn if ZIP exceeds 10MB
- Suggest checking for unnecessary files
- Offer to show file size breakdown

### Missing Templates

- Check for template files before starting
- Provide fallback generic templates if missing
- Warn that documentation may be basic

## Success Criteria

A successful packaging operation results in:

1. ✓ Valid semantic version in SKILL.md frontmatter
2. ✓ Versioned ZIP file in skill-specific downloads directory
3. ✓ Installation instructions (Download.md) generated
4. ✓ User documentation ({SkillName}-doc.md) generated
5. ✓ All previous versions preserved
6. ✓ Package ready for distribution

## Example Usage

**User:** "Package the my-data-analyzer skill"

**Claude Response:**

1. Locates skill at `~/.claude/skills/my-data-analyzer/`
2. Validates structure and reads current version (0.2.3)
3. Asks: "Where should I save the package? Default: ./downloads/my-data-analyzer/"
4. User accepts default or provides custom path
5. Asks: "Current version is 0.2.3. What version action? (keep/patch/minor/major/custom)"
6. User selects "minor" → new version 0.3.0
7. Generates my-data-analyzer-Download.md and my-data-analyzer-doc.md
8. Creates my-data-analyzer-v0.3.0.zip in chosen directory
9. Updates SKILL.md frontmatter with version: 0.3.0
10. Reports success with full package location path

## Integration with Existing Tools

### Reuse from skill-creator

- Validation logic from `quick_validate.py`
- Directory structure conventions
- Naming pattern enforcement

### Complement to package_skill.py

- Extends basic packaging with versioning
- Adds documentation generation
- Provides centralized distribution directory
- Maintains version history

## Requirements

- Python 3.7 or higher
- Claude Code installed and configured
- Skills directory at `~/.claude/skills/`
- Write permissions for output directory

## Resources

### Internal Documentation

- `SKILL.md` - Complete packaging workflow
- `scripts/package_and_document.py` - Automation script
- `templates/` - Documentation templates
- `references/versioning-guide.md` - Versioning guidelines

### External Resources

- [Semantic Versioning Spec](https://semver.org/)
- [Claude Code Documentation](https://docs.claude.com/claude-code)

## Best Practices

### Before Packaging

1. Validate skill structure first
2. Test skill with real tasks
3. Update documentation in SKILL.md
4. Increment version appropriately
5. Clean up unnecessary files

### During Packaging

1. Choose version increment carefully
2. Review generated documentation
3. Verify all files are included
4. Check ZIP file size
5. Test extraction and installation

### After Packaging

1. Test installation in clean environment
2. Verify documentation is clear
3. Share Download.md with ZIP file
4. Keep version history for reference

## Troubleshooting

### Packaging Fails

- Run validation first on skill directory
- Check SKILL.md has valid YAML frontmatter
- Verify all referenced files exist
- Ensure output directory is writable

### Documentation Missing

- Verify template files exist in templates/
- Check template placeholders are correct
- Ensure SKILL.md has required metadata
- Review script output for errors

### Version Conflicts

- Check version format is X.Y.Z
- Verify version is higher than current (unless re-packaging)
- Review version history in output directory
- Confirm intended version action

## Contributing

To improve this skill:

1. Modify SKILL.md with enhancements
2. Update packaging script with new features
3. Enhance templates for better documentation
4. Test with various skill structures
5. Submit improvements back to repository

## License

This skill follows the same license as your project configuration. See LICENSE.txt for complete terms.

---

**Made for Claude Code** - Simplifying skill distribution and version management
