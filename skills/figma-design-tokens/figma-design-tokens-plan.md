# Figma Design Tokens Skill Creation Plan

## Overview

This plan outlines the creation of a Claude Code skill that connects to the Figma MCP server and generates design tokens from Figma designs in multiple formats.

## User Requirements

**Output Formats:**
- CSS Custom Properties
- SCSS Variables
- JSON (Style Dictionary compatible)
- W3C Design Tokens Format (DTCG)

**Token Types:**
- Colors
- Typography
- Spacing
- All available types from Figma

**Additional Features:**
- Customizable token naming conventions
- Organized file structure generation
- TypeScript type definitions
- Auto-generated documentation

**MCP Setup:**
- Includes setup instructions for Figma MCP server

## Skill Directory Structure

```
figma-design-tokens/
├── SKILL.md
├── README.md
├── scripts/
│   ├── extract_tokens.py
│   ├── transform_tokens.py
│   └── validate_tokens.py
├── references/
│   ├── w3c-dtcg-spec.md
│   ├── figma-mcp-tools.md
│   └── token-naming-conventions.md
└── templates/
    ├── w3c-tokens.template.json
    ├── css-variables.template.css
    ├── scss-variables.template.scss
    ├── typescript-types.template.ts
    └── documentation.template.md
```

## Implementation Steps

### 1. Create Skill Directory Structure

Create the main directory and subdirectories:
- `figma-design-tokens/`
- `figma-design-tokens/scripts/`
- `figma-design-tokens/references/`
- `figma-design-tokens/templates/`

### 2. Write SKILL.md (~4-5k words)

**YAML Frontmatter:**
```yaml
---
name: figma-design-tokens
description: Extract design tokens from Figma designs using the Figma MCP server and generate them in multiple formats (CSS, SCSS, JSON, W3C DTCG) with customizable naming conventions, file organization, and TypeScript types
version: 0.1.0
---
```

**Content Sections:**
1. **Overview** - What the skill enables and when to use it
2. **Prerequisites** - Figma MCP server setup instructions
   - Remote server setup (with personal access token)
   - Desktop server setup (with Figma app)
   - Authentication requirements
3. **Workflow Decision Tree** - Help user choose the right approach
   - Extract from specific selection
   - Generate full design system
4. **Step-by-Step Processes:**
   - Using `get_variable_defs` MCP tool
   - Extracting colors, typography, spacing
   - Transforming to W3C DTCG format
   - Generating all output formats
   - Applying naming conventions
   - Organizing into file structure
   - Generating TypeScript types
   - Creating documentation
5. **Error Handling** - Common issues and solutions
   - MCP connection problems
   - Figma authentication errors
   - Selection issues
   - Color space conversion errors
6. **Token Organization Patterns**
   - Primitive vs semantic tokens
   - Multi-theme/mode handling
   - File organization strategies
7. **References** - Point to bundled reference files

### 3. Create Python Scripts

#### extract_tokens.py (~300 lines)

**Purpose:** Parse Figma MCP output and transform to W3C DTCG format

**Features:**
- Parse `get_variable_defs` tool output
- Extract color, typography, spacing variables
- Transform to W3C DTCG structure
- Handle color space conversions (RGB → sRGB)
- Resolve variable references/aliases
- Handle Figma variable modes (themes)

**CLI Interface:**
```python
python extract_tokens.py \
  --figma-data <path-to-json> \
  --output-path <output-file.tokens.json> \
  --token-types colors,typography,spacing
```

**Key Functions:**
- `parse_figma_variables()` - Parse MCP tool output
- `convert_color_to_w3c()` - RGB to W3C color object
- `extract_typography_tokens()` - Aggregate font properties
- `resolve_references()` - Handle variable aliases
- `build_w3c_structure()` - Generate compliant JSON

#### transform_tokens.py (~250 lines)

**Purpose:** Convert W3C DTCG tokens to various output formats

**Features:**
- Convert to CSS custom properties
- Convert to SCSS variables
- Convert to JSON (Style Dictionary format)
- Apply naming conventions (camelCase, kebab-case, BEM)
- Generate organized file structure (separate files per category)
- Generate TypeScript type definitions

**CLI Interface:**
```python
python transform_tokens.py \
  --input <tokens.json> \
  --format css,scss,json,typescript \
  --naming-convention kebab-case \
  --output-dir <output-directory>
```

**Key Functions:**
- `to_css_custom_properties()` - Generate CSS with `:root`
- `to_scss_variables()` - Generate SCSS with `$` prefix
- `to_style_dictionary_json()` - Transform for Style Dictionary
- `apply_naming_convention()` - Transform token names
- `organize_by_category()` - Split into multiple files
- `generate_typescript_types()` - Create type-safe definitions

#### validate_tokens.py (~200 lines)

**Purpose:** Validate W3C DTCG compliance and token structure

**Features:**
- Validate against W3C DTCG specification
- Check for circular references
- Verify required properties
- Validate token type values
- Generate validation report

**CLI Interface:**
```python
python validate_tokens.py \
  --input <tokens.json> \
  --report <validation-report.md>
```

**Key Functions:**
- `validate_w3c_compliance()` - Check spec adherence
- `detect_circular_references()` - Find circular aliases
- `validate_token_values()` - Type-specific validation
- `generate_report()` - Create markdown report

### 4. Create Reference Documentation

#### w3c-dtcg-spec.md (~2k words)

**Content:**
- W3C Design Tokens Format Module overview
- Token types and their structures:
  - `color` - Color space objects
  - `dimension` - Numeric with units
  - `fontFamily` - Font family names
  - `fontWeight` - Font weight values
  - `duration` - Time values
  - `cubicBezier` - Animation curves
  - `number` - Unitless values
  - `typography` - Composite type
  - `shadow` - Composite type
  - `border` - Composite type
  - `gradient` - Array of stops
- JSON structure requirements
- Required vs optional properties
- Reference/alias syntax: `{token.name}`
- Groups and type inheritance
- `$extensions` for vendor metadata
- Complete examples for each token type

#### figma-mcp-tools.md (~1k words)

**Content:**
- Overview of Figma MCP server
- Available tools:
  - `get_variable_defs` - Primary tool for design tokens
  - `get_design_context` - For design structure
  - `get_metadata` - For layer information
  - `get_screenshot` - For visual reference
- Tool parameters and return formats
- Authentication requirements
- Limitations:
  - Selection-based extraction
  - Enterprise plan for REST API
  - Design files only (not FigJam)
- Best practices for extraction
- Common error scenarios

#### token-naming-conventions.md (~800 words)

**Content:**
- Naming convention patterns:
  - kebab-case: `color-primary-500`
  - camelCase: `colorPrimary500`
  - snake_case: `color_primary_500`
  - BEM: `color__primary--500`
- Semantic vs primitive tokens:
  - Primitives: `blue-500`, `spacing-4`
  - Semantic: `color-primary`, `spacing-medium`
- Multi-theme organization:
  - Separate files approach
  - Token reference approach
  - Nested groups approach
- Category prefixes: `color-*`, `spacing-*`, `font-*`
- Scale naming: numeric (100-900) vs t-shirt (xs-xl)
- Best practices and recommendations

### 5. Create Output Templates

#### w3c-tokens.template.json

```json
{
  "$schema": "https://design-tokens.github.io/community-group/format.json",
  "colors": {
    "$type": "color",
    "{{TOKEN_NAME}}": {
      "$value": "{{TOKEN_VALUE}}",
      "$description": "{{TOKEN_DESCRIPTION}}"
    }
  },
  "spacing": {
    "$type": "dimension",
    "{{TOKEN_NAME}}": {
      "$value": "{{TOKEN_VALUE}}"
    }
  },
  "typography": {
    "$type": "typography",
    "{{TOKEN_NAME}}": {
      "$value": {
        "fontFamily": "{{FONT_FAMILY}}",
        "fontSize": "{{FONT_SIZE}}",
        "fontWeight": "{{FONT_WEIGHT}}",
        "lineHeight": "{{LINE_HEIGHT}}"
      }
    }
  }
}
```

#### css-variables.template.css

```css
/**
 * Design Tokens - CSS Custom Properties
 * Generated from Figma design variables
 */

:root {
  /* Colors */
  --{{COLOR_TOKEN_NAME}}: {{COLOR_VALUE}};

  /* Spacing */
  --{{SPACING_TOKEN_NAME}}: {{SPACING_VALUE}};

  /* Typography */
  --{{FONT_FAMILY_TOKEN_NAME}}: {{FONT_FAMILY_VALUE}};
  --{{FONT_SIZE_TOKEN_NAME}}: {{FONT_SIZE_VALUE}};
  --{{FONT_WEIGHT_TOKEN_NAME}}: {{FONT_WEIGHT_VALUE}};
  --{{LINE_HEIGHT_TOKEN_NAME}}: {{LINE_HEIGHT_VALUE}};
}
```

#### scss-variables.template.scss

```scss
/**
 * Design Tokens - SCSS Variables
 * Generated from Figma design variables
 */

// Colors
${{COLOR_TOKEN_NAME}}: {{COLOR_VALUE}};

// Spacing
${{SPACING_TOKEN_NAME}}: {{SPACING_VALUE}};

// Typography
${{FONT_FAMILY_TOKEN_NAME}}: {{FONT_FAMILY_VALUE}};
${{FONT_SIZE_TOKEN_NAME}}: {{FONT_SIZE_VALUE}};
${{FONT_WEIGHT_TOKEN_NAME}}: {{FONT_WEIGHT_VALUE}};
${{LINE_HEIGHT_TOKEN_NAME}}: {{LINE_HEIGHT_VALUE}};
```

#### typescript-types.template.ts

```typescript
/**
 * Design Tokens - TypeScript Type Definitions
 * Generated from Figma design variables
 */

export type ColorTokens = {
  {{COLOR_TOKEN_NAME}}: '{{COLOR_VALUE}}';
};

export type SpacingTokens = {
  {{SPACING_TOKEN_NAME}}: '{{SPACING_VALUE}}';
};

export type TypographyTokens = {
  {{TYPOGRAPHY_TOKEN_NAME}}: {
    fontFamily: '{{FONT_FAMILY}}';
    fontSize: '{{FONT_SIZE}}';
    fontWeight: {{FONT_WEIGHT}};
    lineHeight: '{{LINE_HEIGHT}}';
  };
};

export const tokens = {
  colors: {
    {{COLOR_TOKEN_NAME}}: '{{COLOR_VALUE}}',
  },
  spacing: {
    {{SPACING_TOKEN_NAME}}: '{{SPACING_VALUE}}',
  },
  typography: {
    {{TYPOGRAPHY_TOKEN_NAME}}: {
      fontFamily: '{{FONT_FAMILY}}',
      fontSize: '{{FONT_SIZE}}',
      fontWeight: {{FONT_WEIGHT}},
      lineHeight: '{{LINE_HEIGHT}}',
    },
  },
} as const;
```

#### documentation.template.md

```markdown
# Design Tokens Documentation

Auto-generated from Figma design variables.

## Colors

| Token Name | Value | Description |
|------------|-------|-------------|
| `{{TOKEN_NAME}}` | `{{TOKEN_VALUE}}` | {{DESCRIPTION}} |

## Spacing

| Token Name | Value | Description |
|------------|-------|-------------|
| `{{TOKEN_NAME}}` | `{{TOKEN_VALUE}}` | {{DESCRIPTION}} |

## Typography

| Token Name | Font Family | Size | Weight | Line Height |
|------------|-------------|------|--------|-------------|
| `{{TOKEN_NAME}}` | {{FONT_FAMILY}} | {{FONT_SIZE}} | {{FONT_WEIGHT}} | {{LINE_HEIGHT}} |

## Usage Examples

### CSS
```css
.element {
  color: var(--{{COLOR_TOKEN}});
  margin: var(--{{SPACING_TOKEN}});
}
```

### SCSS
```scss
.element {
  color: ${{COLOR_TOKEN}};
  margin: ${{SPACING_TOKEN}};
}
```

### TypeScript
```typescript
import { tokens } from './tokens';

const styles = {
  color: tokens.colors.{{COLOR_TOKEN}},
  margin: tokens.spacing.{{SPACING_TOKEN}},
};
```
```

### 6. Create User Documentation (README.md)

**Content:**
- Overview of skill capabilities
- Prerequisites:
  - Figma MCP server installation
  - Authentication setup
  - Figma file access
- Quick start guide
- Workflow examples:
  - Extract tokens from selection
  - Generate full design system
- Output format examples
- Customization options:
  - Naming conventions
  - File organization
  - Output formats
- Troubleshooting guide:
  - MCP connection issues
  - Authentication errors
  - Selection problems
  - Format conversion errors
- Advanced usage:
  - Multi-theme handling
  - Custom transformations
  - Integration with build tools

### 7. Testing & Validation

**Validation Steps:**
1. Validate SKILL.md frontmatter format
2. Test Python scripts with sample Figma data
3. Verify all output formats generate correctly
4. Check W3C DTCG compliance
5. Ensure TypeScript types compile
6. Test with different naming conventions
7. Verify file organization structure
8. Test error handling scenarios

**Test Data:**
- Create sample Figma MCP tool output JSON
- Include various token types (colors, typography, spacing)
- Include variable references/aliases
- Include multiple modes (light/dark themes)

## Key Features Summary

✓ **Multiple Output Formats**
  - CSS Custom Properties (`:root` variables)
  - SCSS Variables (`$` prefix)
  - JSON (Style Dictionary compatible)
  - W3C Design Tokens Format (DTCG spec)

✓ **All Token Types**
  - Colors (with color space conversion)
  - Typography (aggregated properties)
  - Spacing/dimensions
  - All available types from Figma

✓ **MCP Integration**
  - Complete Figma MCP server setup guide
  - Instructions for remote and desktop servers
  - Authentication configuration
  - Tool usage workflows

✓ **Customization Features**
  - Multiple naming conventions (kebab, camel, snake, BEM)
  - Organized file structure (per-category files)
  - TypeScript type definitions
  - Auto-generated documentation

✓ **Quality Assurance**
  - W3C DTCG validation
  - Circular reference detection
  - Token structure verification
  - Error reporting

## Workflow After Implementation

1. **User triggers skill** by requesting "extract design tokens from Figma"
2. **Skill loads** and presents prerequisite checklist
3. **User selects Figma elements** containing variables to extract
4. **Skill guides** user to use `get_variable_defs` MCP tool
5. **Scripts process** MCP output and transform to W3C DTCG
6. **Scripts generate** all requested output formats
7. **Files created** in organized structure:
   ```
   output/
   ├── tokens.json (W3C DTCG)
   ├── tokens.css (CSS custom properties)
   ├── tokens.scss (SCSS variables)
   ├── tokens.ts (TypeScript definitions)
   ├── colors.tokens.json
   ├── spacing.tokens.json
   ├── typography.tokens.json
   └── documentation.md
   ```
8. **Validation report** generated confirming compliance
9. **User integrates** tokens into project

## Implementation Timeline

1. **Directory structure** - Create all folders
2. **SKILL.md** - Write core skill instructions
3. **Python scripts** - Build extraction, transformation, validation
4. **Reference docs** - Create W3C spec, Figma tools, naming guides
5. **Templates** - Build all output format templates
6. **README.md** - Write user documentation
7. **Testing** - Validate and test with sample data
8. **Refinement** - Iterate based on test results

## Technical Considerations

**Color Space Handling:**
- Figma uses RGB internally
- W3C DTCG supports multiple color spaces (sRGB, Display P3, Oklch)
- Scripts will convert Figma RGB to W3C sRGB format
- Future enhancement: Support for modern color spaces

**Variable Modes:**
- Figma modes (light/dark themes) map to token organization
- Approach: Generate separate token files per mode
- Alternative: Use token references for theme switching

**Naming Transformations:**
- Figma allows `.` in variable names (e.g., `color.primary.500`)
- W3C prohibits `.` in token names
- Scripts will convert `.` to `/` or `-` based on convention

**Typography Aggregation:**
- Figma has separate properties (family, size, weight, height)
- W3C has composite typography type
- Scripts will aggregate related variables into composite tokens

**API Limitations:**
- Figma REST API for variables requires Enterprise plan
- MCP `get_variable_defs` provides alternative access
- Limited to selected elements (may require multiple extractions)

## Success Metrics

- Skill successfully extracts tokens from Figma selections
- All 4 output formats generate correctly
- W3C DTCG validation passes
- TypeScript types compile without errors
- Documentation is clear and comprehensive
- Error handling provides actionable guidance
- User can customize naming and organization
- Integration with existing tools (Style Dictionary, etc.) works smoothly

---

**Plan Status:** Ready for implementation
**Version:** 0.1.0
**Last Updated:** 2025-11-21
