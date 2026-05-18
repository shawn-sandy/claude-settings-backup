# Figma Design Tokens Generator

A Claude Code skill that extracts design tokens from Figma designs and generates production-ready files in multiple formats.

## Overview

This skill connects to the Figma MCP server to extract design variables (colors, typography, spacing, etc.) from Figma files and transforms them into:

- **W3C Design Tokens Format** (DTCG) - Industry standard JSON
- **CSS Custom Properties** - Browser-native variables
- **SCSS Variables** - Sass-compatible format
- **TypeScript Types** - Type-safe definitions
- **Documentation** - Auto-generated markdown

## Features

- Extract design tokens from Figma variable collections
- **Automatic fallback:** Extract from node styles when no variables exist
- **Duplicate detection:** Automatically prevent duplicate token values
- Transform to multiple output formats in one command
- Customizable naming conventions (kebab-case, camelCase, snake_case, BEM)
- Organized file structure (single file or per-category)
- W3C DTCG specification compliance validation
- Support for multiple themes/modes (light/dark)
- TypeScript type generation for type-safe token access
- Auto-generated documentation

## Prerequisites

### 1. Install and Configure Figma MCP Server

The Figma MCP server must be installed and configured before using this skill. Follow these detailed steps:

#### Option A: Remote Server (Recommended)

**Step 1: Install Node.js**

The Figma MCP server requires Node.js. Verify you have Node.js installed:

```bash
node --version
npm --version
```

If not installed, download from [nodejs.org](https://nodejs.org/)

**Step 2: Test Figma MCP Server**

Test that the server can be accessed:

```bash
npx @figma/mcp-server-figma
```

This will download and run the server. Press Ctrl+C to stop after verification.

**Step 3: Get Figma Personal Access Token**

1. Open your web browser and go to [Figma](https://www.figma.com)
2. Click your profile icon → **Settings**
3. Scroll to **Personal Access Tokens** section
4. Click **Generate new token**
5. Give it a descriptive name (e.g., "Claude Code MCP")
6. Click **Generate token**
7. **IMPORTANT:** Copy the token immediately - you won't be able to see it again!

Your token will look like: `figd_XXXXXXXXXXXXXXXXXXXXXXXXXXXXX`

**Step 4: Configure Claude Code**

1. Locate your Claude Code config file:
   - **macOS/Linux:** `~/.claude/config.json`
   - **Windows:** `%USERPROFILE%\.claude\config.json`

2. If the file doesn't exist, create it with this content:

```json
{
  "mcpServers": {
    "figma": {
      "command": "npx",
      "args": ["@figma/mcp-server-figma"],
      "env": {
        "FIGMA_PERSONAL_ACCESS_TOKEN": "figd_YOUR_TOKEN_HERE"
      }
    }
  }
}
```

3. If the file exists, add the `figma` entry to the `mcpServers` object:

```json
{
  "mcpServers": {
    "existing-server": { ... },
    "figma": {
      "command": "npx",
      "args": ["@figma/mcp-server-figma"],
      "env": {
        "FIGMA_PERSONAL_ACCESS_TOKEN": "figd_YOUR_TOKEN_HERE"
      }
    }
  }
}
```

4. Replace `figd_YOUR_TOKEN_HERE` with your actual token from Step 3

**Step 5: Restart Claude Code**

Completely quit and restart Claude Code for the configuration to take effect.

**Step 6: Verify Connection**

In Claude Code, test the connection by asking:

```
"Can you check if the Figma MCP server is connected?"
```

If successful, you should be able to use Figma MCP tools.

#### Option B: Desktop Server (Alternative)

Use this option if you prefer to use the Figma desktop app instead of API tokens.

**Requirements:**

- Figma desktop app installed ([Download here](https://www.figma.com/downloads/))
- Figma desktop app must be running when using the skill
- Logged into your Figma account in the desktop app

**Configuration:**

Add to `~/.claude/config.json`:

```json
{
  "mcpServers": {
    "figma": {
      "command": "npx",
      "args": ["@figma/mcp-server-figma", "--desktop"]
    }
  }
}
```

**Note:** Desktop server mode:

- ✓ No token required
- ✓ Can access local files and drafts
- ✗ Requires Figma desktop app running
- ✗ Only works with files open or accessible in desktop app

### 2. Figma File Requirements

Before using this skill, ensure your Figma file has:

- **Design variables** (not just styles)
  - Variables are in the Variables panel (not Styles panel)
  - You need at least some color, number, string, or boolean variables defined
- **Appropriate access**
  - View access minimum (for extraction)
  - Edit access (if creating code connections)
- **File URL or file key**
  - Format: `https://www.figma.com/design/FILE_KEY/File-Name`
  - Or just the file key: `aBc123XyZ...`

**How to check if you have variables:**

1. Open your Figma file
2. Look for the Variables icon in the right panel (looks like two circles connected)
3. If you see variables listed, you're good to go!
4. If not, you'll need to create variables first (Styles won't work with this skill)

#### Figma MCP Tools Reference

[Figma MCP Server Documentation](https://developers.figma.com/docs/figma-mcp-server/)

### 3. Verify Everything Works

**Test the full setup:**

1. Ensure Figma MCP server is configured
2. Restart Claude Code
3. Have a Figma file URL ready with variables
4. Ask Claude Code:

   ```
   "Extract design tokens from my Figma file: https://www.figma.com/design/YOUR_FILE_KEY/..."
   ```

If everything is configured correctly, the skill will load and guide you through the extraction process.

### Troubleshooting Installation

**"MCP server 'figma' not found"**

- Check `~/.claude/config.json` exists and has the figma entry
- Verify JSON syntax is valid (use a JSON validator)
- Restart Claude Code completely

**"Authentication failed"**

- Verify your personal access token is correct
- Token should start with `figd_`
- Regenerate token in Figma if needed
- Check for extra spaces in config file

**"npx: command not found"**

- Install Node.js from nodejs.org
- Restart your terminal/Claude Code after installation

**"Cannot find module '@figma/mcp-server-figma'"**

- Run `npx @figma/mcp-server-figma` manually first
- Check your internet connection
- Try clearing npm cache: `npm cache clean --force`

## Quick Start

### 1. Trigger the Skill

Ask Claude Code to extract design tokens from Figma:

```
"Extract design tokens from my Figma design system"
"Generate design tokens from Figma variables"
"Convert Figma variables to CSS custom properties"
```

### 2. Provide Figma File

Share your Figma file URL:

```
https://www.figma.com/design/YOUR_FILE_KEY/File-Name
```

### 3. Select Elements (Optional)

If extracting from specific frames:

- Open the Figma file
- Select the frames/components with design variables
- Note the node IDs if needed

### 4. Choose Options

The skill will guide you through:

- Token types to extract (colors, typography, spacing, all)
- Output formats (CSS, SCSS, JSON, TypeScript, documentation)
- Naming convention (kebab-case, camelCase, etc.)
- File organization (single file or per-category)
- Theme/mode handling (if applicable)

### 5. Review Output

Generated files will be saved to your specified output directory:

```
output/
├── tokens.json          # W3C DTCG format
├── tokens.css           # CSS custom properties
├── tokens.scss          # SCSS variables
├── tokens.ts            # TypeScript types
├── documentation.md     # Auto-generated docs
└── validation-report.md # Compliance report
```

## Usage Examples

### Extract All Tokens

```bash
# Use Figma MCP get_variable_defs tool
# Then run extraction
python figma-design-tokens/scripts/extract_tokens.py \
  --figma-data mcp-output.json \
  --output-path tokens.json \
  --token-types all
```

### Generate All Formats

```bash
python figma-design-tokens/scripts/transform_tokens.py \
  --input tokens.json \
  --format css,scss,json,typescript,documentation \
  --naming-convention kebab-case \
  --output-dir ./dist
```

### Validate Tokens

```bash
python figma-design-tokens/scripts/validate_tokens.py \
  --input tokens.json \
  --report validation-report.md
```

### Extract Specific Theme

```bash
# Extract light mode only
python figma-design-tokens/scripts/extract_tokens.py \
  --figma-data mcp-output.json \
  --mode light \
  --output-path tokens-light.json
```

### Organize by Category

```bash
python figma-design-tokens/scripts/transform_tokens.py \
  --input tokens.json \
  --format css,scss \
  --organize-by-category \
  --output-dir ./dist
```

Generates:

```
dist/
├── colors.css
├── colors.scss
├── spacing.css
├── spacing.scss
├── typography.css
└── typography.scss
```

## Naming Conventions

Choose from four built-in naming conventions:

### kebab-case (Default)

```css
--color-primary-500
--spacing-medium
--font-family-heading
```

### camelCase

```javascript
colorPrimary500
spacingMedium
fontFamilyHeading
```

### snake_case

```python
color_primary_500
spacing_medium
font_family_heading
```

### BEM

```css
--color__primary--500
--spacing__medium
--font-family__heading
```

## Output Formats

### W3C Design Tokens (JSON)

Specification-compliant format for maximum interoperability.

```json
{
  "color": {
    "$type": "color",
    "primary": {
      "$value": "#0066cc",
      "$description": "Primary brand color"
    }
  }
}
```

**Use for:** Style Dictionary, design tools integration

### CSS Custom Properties

Browser-native CSS variables.

```css
:root {
  --color-primary: #0066cc;
  --spacing-medium: 16px;
}
```

**Use for:** Vanilla CSS, PostCSS, any CSS framework

### SCSS Variables

Sass-compatible variables.

```scss
$color-primary: #0066cc;
$spacing-medium: 16px;
```

**Use for:** Sass/SCSS projects

### TypeScript Types

Type-safe token access for TypeScript/JavaScript.

```typescript
export const tokens = {
  color: {
    primary: '#0066cc',
  },
  spacing: {
    medium: '16px',
  },
} as const;

export type ColorTokens = typeof tokens.color;
```

**Use for:** React, Vue, Angular, any TypeScript project

### Documentation

Auto-generated markdown reference.

**Use for:** Design system documentation, style guides

## Integration Examples

### CSS Projects

```css
@import './tokens.css';

.button {
  background-color: var(--color-primary);
  padding: var(--spacing-medium);
}
```

### SCSS Projects

```scss
@import './tokens';

.button {
  background-color: $color-primary;
  padding: $spacing-medium;
}
```

### React/TypeScript

```typescript
import { tokens } from './tokens';

const Button: React.FC = () => (
  <button
    style={{
      backgroundColor: tokens.color.primary,
      padding: tokens.spacing.medium,
    }}
  >
    Click Me
  </button>
);
```

### Style Dictionary

```javascript
const StyleDictionary = require('style-dictionary');

const sd = StyleDictionary.extend({
  source: ['tokens.json'],
  platforms: {
    css: {
      transformGroup: 'css',
      buildPath: 'dist/',
      files: [{
        destination: 'variables.css',
        format: 'css/variables'
      }]
    }
  }
});

sd.buildAllPlatforms();
```

## Multi-Theme Support

### Separate Files Approach

Extract each theme separately:

```bash
# Light theme
python extract_tokens.py --mode light --output-path tokens-light.json

# Dark theme
python extract_tokens.py --mode dark --output-path tokens-dark.json
```

Use theme-specific files:

```css
/* light-theme.css */
@import './tokens-light.css';

/* dark-theme.css */
@import './tokens-dark.css';
```

### Token References Approach

Use W3C token references:

```json
{
  "base": {
    "blue": { "$value": "#0066cc" },
    "white": { "$value": "#ffffff" }
  },
  "theme": {
    "light": {
      "primary": { "$value": "{base.blue}" }
    },
    "dark": {
      "primary": { "$value": "{base.white}" }
    }
  }
}
```

## Troubleshooting

### MCP Connection Issues

**Problem:** "MCP server 'figma' not found"

**Solution:**

1. Verify config in `~/.claude/config.json`
2. Restart Claude Code
3. Test with simple MCP command

### Authentication Errors

**Problem:** "Authentication failed"

**Solution:**

1. Regenerate personal access token in Figma
2. Update token in config
3. Restart Claude Code

### No Variables Found

**Problem:** "No variables extracted from Figma"

**Solution:**

1. Verify file has variables (not just styles)
2. Check you have access to the file
3. Try desktop server if using remote
4. Select specific frames with variables

### Validation Errors

**Problem:** "W3C DTCG validation failed"

**Solution:**

1. Review validation report for specific errors
2. Check token structure matches W3C spec
3. Verify all tokens have `$value` property
4. Check for circular references

## Advanced Usage

### Custom Token Types

For Figma variables that don't map to standard W3C types:

```bash
python extract_tokens.py \
  --custom-type "CUSTOM_TYPE:my-custom-type" \
  --figma-data input.json \
  --output-path output.json
```

### Batch Processing

Process multiple Figma files:

```bash
for file in *.json; do
  python extract_tokens.py \
    --figma-data "$file" \
    --output-path "output/$(basename $file .json).tokens.json"
done
```

### CI/CD Integration

Automate token generation in your pipeline:

```yaml
# .github/workflows/tokens.yml
name: Update Design Tokens

on:
  workflow_dispatch:
  schedule:
    - cron: '0 0 * * 1' # Weekly

jobs:
  update-tokens:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Generate Tokens
        run: |
          # Fetch from Figma
          # Extract and transform
          # Commit changes
```

## Best Practices

1. **Version control tokens** - Track changes in git
2. **Validate before committing** - Run validation script
3. **Document token usage** - Use `$description` fields
4. **Use semantic naming** - Name by purpose, not value
5. **Organize hierarchically** - Group related tokens
6. **Test in components** - Verify tokens work in UI
7. **Automate updates** - Set up regular sync from Figma
8. **Communicate changes** - Notify team of token updates

## Skill Structure

```
figma-design-tokens/
├── SKILL.md              # Skill instructions for Claude
├── README.md             # This file
├── scripts/
│   ├── extract_tokens.py    # Figma → W3C DTCG
│   ├── transform_tokens.py  # W3C → Multiple formats
│   └── validate_tokens.py   # W3C compliance checker
├── references/
│   ├── w3c-dtcg-spec.md             # W3C specification
│   ├── figma-mcp-tools.md           # Figma MCP reference
│   └── token-naming-conventions.md  # Naming guide
└── templates/
    ├── w3c-tokens.template.json     # W3C format example
    ├── css-variables.template.css   # CSS example
    ├── scss-variables.template.scss # SCSS example
    ├── typescript-types.template.ts # TypeScript example
    └── documentation.template.md    # Docs example
```

## Contributing

This is a Claude Code skill. To improve it:

1. Modify `SKILL.md` for workflow changes
2. Update scripts for new features
3. Add references for additional documentation
4. Create templates for new output formats
5. Test thoroughly with real Figma files

## Resources

- **W3C Design Tokens Spec:** <https://tr.designtokens.org/format/>
- **Figma Variables Guide:** <https://help.figma.com/hc/en-us/articles/15339657135383>
- **Figma MCP Server:** <https://github.com/figma/mcp-server-figma>
- **Style Dictionary:** <https://amzn.github.io/style-dictionary/>
- **Design Tokens Community Group:** <https://www.designtokens.org/>

## Support

For issues with:

- **The skill itself:** Modify SKILL.md or scripts
- **Figma MCP server:** Check Figma MCP documentation
- **Claude Code:** Visit <https://github.com/anthropics/claude-code/issues>
- **W3C DTCG spec:** Consult the specification

## License

This skill is provided as-is for use with Claude Code.

---

**Version:** 0.2.0
**Last Updated:** 2025-11-22
