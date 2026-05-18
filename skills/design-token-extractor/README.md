# Design Token Extractor

Extract design tokens from images and convert them into CSS custom properties, atomic utility classes (Tailwind-style), W3C Design Token format, and platform-specific implementations.

## Overview

This skill helps you analyze design mockups, screenshots, or design system documentation to extract design tokens (colors, typography, spacing, dimensions, motion) and convert them into standards-compliant, production-ready code including comprehensive atomic utility classes for utility-first development.

**New in v0.2.0:** Comprehensive atomic utility class generation with Tailwind-style naming, including color, spacing (with logical properties), typography, and layout utilities, plus full support for container query variants, state variants (hover/focus/active), and dark mode.

## Features

- **W3C DTCG Compliance**: Generates tokens following W3C Design Tokens Community Group specification
- **Atomic Utility Generation**: Create comprehensive Tailwind-style utility classes from design tokens
- **Modern CSS**: Leverages cascade layers, container queries, and logical properties
- **Responsive Variants**: Container query breakpoints (sm/md/lg/xl) for all utilities
- **State Management**: Hover, focus, and active state variants for interactive elements
- **Dark Mode Support**: Automatic dark mode variants using prefers-color-scheme
- **Cross-Platform**: Exports to CSS, SCSS, iOS (Swift), Android (Kotlin), and more
- **Accessibility First**: Validates WCAG 2.2 contrast ratios, motion preferences, and forced-colors
- **Multiple Formats**: W3C JSON, CSS custom properties, atomic utilities, SCSS variables, platform-specific
- **Automated Validation**: Ensures tokens meet W3C specification requirements

## When to Use This Skill

Use this skill when you need to:

- Extract design tokens from design mockups or screenshots
- Convert visual designs into CSS custom properties
- **Generate atomic utility classes (Tailwind-style) from design tokens**
- **Create utility-first design systems with comprehensive responsive and state variants**
- Generate W3C-compliant design token JSON
- Create cross-platform design token libraries
- Validate existing tokens against W3C specifications
- Transform tokens between different formats (JSON → CSS → SCSS → utilities → platform)
- **Build complete design systems with both tokens and generated utilities**

## Installation

### Option 1: Using gitpick (Recommended)

```bash
gitpick anthropics/claude-code-skills design-token-extractor
```

### Option 2: Manual Installation

1. Clone or download this skill directory
2. Move it to `~/.claude/skills/design-token-extractor/`
3. Restart Claude Code if running

### Option 3: From ZIP Package

1. Download the latest release ZIP
2. Extract to `~/.claude/skills/`
3. Restart Claude Code if running

## Prerequisites

- **Python 3.7+**: Required for token extraction and transformation scripts
- **Image Analysis**: Skill works best with clear, high-resolution design mockups

## Quick Start

### Basic Usage

Simply provide an image or design mockup:

```
Extract design tokens from this image: [attach mockup.png]
```

Claude will:
1. Analyze the image for colors, typography, spacing, and other tokens
2. Ask which output format you prefer (W3C JSON, CSS, SCSS, etc.)
3. Generate tokens following modern standards
4. Validate output against W3C specifications

### Specify Output Format

Request a specific format:

```
Extract design tokens from this mockup and output as CSS custom properties
```

```
Generate W3C Design Token JSON from this screenshot
```

### Transform Existing Tokens

Convert between formats:

```
Transform these W3C tokens to CSS custom properties with cascade layers
```

```
Convert this CSS to iOS Swift code
```

### Generate Atomic Utilities

Create utility classes from tokens:

```
Generate Tailwind-style utility classes from these tokens
```

```
Create a complete design system with tokens and utilities
```

```
python scripts/transform_tokens.py --input tokens.json --format utilities --output utilities.css
```

```
python scripts/transform_tokens.py --input tokens.json --format css-layers-full --output design-system.css
```

## Output Formats

### W3C Design Tokens (JSON)

Standard format for design tools and token pipelines:

```json
{
  "color": {
    "primary": {
      "$value": "#2563eb",
      "$type": "color",
      "$description": "Primary brand color"
    }
  }
}
```

### CSS Custom Properties

Modern CSS with cascade layers:

```css
@layer tokens {
  :root {
    --color-primary-500: #2563eb;
    --spacing-scale-md: 1rem;
  }
}
```

### Atomic Utilities (New in v0.2.0)

Comprehensive Tailwind-style utility classes:

```css
/* Color utilities */
.text-primary-500 { color: var(--color-primary-500); }
.bg-surface-elevated { background-color: var(--color-surface-elevated); }

/* Spacing with logical properties */
.p-md { padding: var(--spacing-scale-md); }
.mx-auto { margin-inline: auto; }

/* Responsive variants */
.md\:text-lg { /* Applied at md breakpoint */ }

/* State variants */
.hover\:bg-primary-600:hover { background-color: var(--color-primary-600); }

/* Dark mode */
.dark\:bg-neutral-900 { /* Applied in dark mode */ }
```

### Complete Design System (css-layers-full)

Full design system with tokens AND generated utilities in organized cascade layers.

### Platform-Specific

iOS (Swift), Android (Kotlin), and other platforms supported.

## Atomic Utility Classes (v0.2.0)

### Overview

The skill generates comprehensive Tailwind-style atomic utility classes from extracted design tokens. These utilities enable rapid prototyping and utility-first development with full support for responsive variants, state management, and accessibility.

### Generated Utility Categories

#### Color Utilities

```css
/* Text colors */
.text-primary-500 { color: var(--color-primary-500); }
.text-neutral-900 { color: var(--color-neutral-900); }

/* Background colors */
.bg-surface-elevated { background-color: var(--color-surface-elevated); }
.bg-primary-500 { background-color: var(--color-primary-500); }

/* Border colors */
.border-accent-600 { border-color: var(--color-accent-600); }

/* SVG colors */
.fill-primary-500 { fill: var(--color-primary-500); }
.stroke-neutral-900 { stroke: var(--color-neutral-900); }
```

#### Spacing Utilities (Logical Properties)

```css
/* Padding */
.p-md { padding: var(--spacing-scale-md); }
.px-lg { padding-inline: var(--spacing-scale-lg); }  /* horizontal */
.py-sm { padding-block: var(--spacing-scale-sm); }   /* vertical */

/* Margin */
.m-md { margin: var(--spacing-scale-md); }
.mx-auto { margin-inline: auto; }  /* center horizontally */
.my-lg { margin-block: var(--spacing-scale-lg); }

/* Gap (for Grid/Flexbox) */
.gap-md { gap: var(--spacing-scale-md); }
.gap-x-sm { column-gap: var(--spacing-scale-sm); }
```

#### Typography Utilities

```css
/* Font family */
.font-display { font-family: var(--font-family-display); }
.font-body { font-family: var(--font-family-body); }

/* Font size */
.text-xl { font-size: var(--font-size-xl); }
.text-base { font-size: var(--font-size-base); }

/* Font weight */
.font-bold { font-weight: var(--font-weight-bold); }

/* Line height */
.leading-tight { line-height: var(--line-height-tight); }
```

#### Layout Utilities

```css
/* Border radius */
.rounded-md { border-radius: var(--border-radius-md); }
.rounded-full { border-radius: var(--border-radius-full); }

/* Shadows */
.shadow-md { box-shadow: var(--shadow-md); }
.shadow-elevated { box-shadow: var(--shadow-elevated); }
```

### Utility Variants

#### Container Query Variants (Responsive)

```html
<div class="text-base md:text-lg lg:text-xl">
  Text that grows with container size
</div>

<div class="p-sm md:p-md lg:p-lg">
  Padding that increases at larger sizes
</div>
```

Breakpoints: `sm:` (640px), `md:` (768px), `lg:` (1024px), `xl:` (1280px)

#### State Variants

```html
<!-- Hover -->
<button class="bg-primary-500 hover:bg-primary-600">
  Button with hover state
</button>

<!-- Focus -->
<input class="outline-neutral-300 focus:outline-primary-500">

<!-- Active -->
<button class="bg-primary-500 active:bg-primary-700">
  Button with active state
</button>
```

#### Dark Mode Variants

```html
<div class="bg-white dark:bg-neutral-900
            text-neutral-900 dark:text-neutral-100">
  Content that adapts to dark mode
</div>
```

### Usage Examples

#### Utility-First Card Component

```html
<article class="bg-white dark:bg-neutral-800
                p-lg rounded-lg shadow-md
                border border-neutral-200 dark:border-neutral-700">
  <h2 class="font-display text-2xl font-bold
             text-neutral-900 dark:text-white
             mb-md">
    Card Title
  </h2>
  <p class="text-base leading-relaxed
            text-neutral-700 dark:text-neutral-300
            mb-lg">
    Card content with proper spacing and typography.
  </p>
  <button class="px-lg py-md
                 bg-primary-600 hover:bg-primary-700
                 text-white rounded-sm font-semibold
                 focus:outline-accent-500">
    Action Button
  </button>
</article>
```

#### Responsive Grid Layout

```html
<div class="grid gap-md md:gap-lg
            grid-cols-1 md:grid-cols-2 lg:grid-cols-3">
  <div class="p-md bg-neutral-50 dark:bg-neutral-800 rounded-md">
    Grid Item 1
  </div>
  <div class="p-md bg-neutral-50 dark:bg-neutral-800 rounded-md">
    Grid Item 2
  </div>
</div>
```

### Configuration Options

Customize utility generation with a config JSON file:

```json
{
  "categories": ["colors", "spacing", "typography", "layout"],
  "variants": ["container", "state", "dark-mode"],
  "prefix": ""
}
```

**Usage:**
```bash
python scripts/generate_utilities.py \
  --input tokens.json \
  --output utilities.css \
  --config custom-config.json
```

### Browser Support

- Chrome/Edge: 88+ (container queries)
- Firefox: 110+
- Safari: 16+

Base utilities work in all browsers with CSS custom property support. Container query variants gracefully degrade on older browsers.

## Bundled Resources

### Scripts

- **extract_tokens.py**: Extract tokens from image analysis
- **transform_tokens.py**: Convert between formats (CSS, SCSS, utilities, iOS, Android)
- **generate_utilities.py**: Generate atomic utility classes from tokens (new in v0.2.0)
- **validate_tokens.py**: Validate against W3C spec

### Templates

- **w3c-tokens.template.json**: W3C format structure
- **css-variables.template.css**: CSS custom properties
- **css-layers.template.css**: Full cascade layers implementation with utilities placeholder
- **utilities.template.css**: Atomic utility classes template (new in v0.2.0)
- **documentation.template.md**: Token documentation

### References

- **w3c-dtcg-spec.md**: W3C Design Tokens specification
- **css-standards.md**: Modern CSS features guide
- **accessibility-guidelines.md**: WCAG 2.2 compliance

## Implementation Strategy

1. **Start with W3C JSON format** for design tool compatibility
2. **Use Style Dictionary or similar** to transform tokens into platform-specific formats
3. **Implement cascade layers** in the correct order for proper inheritance
4. **Test container queries** across different component sizes
5. **Validate accessibility** using automated tools and manual testing
6. **Document token relationships** and usage patterns for team adoption

## Token Naming Conventions

- **Colors**: `--color-{role}-{variant}` (e.g., `--color-primary-500`)
- **Typography**: `--font-{property}-{size}` (e.g., `--font-size-lg`)
- **Spacing**: `--spacing-{scale}-{size}` (e.g., `--spacing-scale-md`)
- **Dimensions**: `--{element}-{property}` (e.g., `--border-radius-sm`)

## Troubleshooting

### Tokens Not Extracted

- Ensure image is clear and high-resolution
- Provide context about which elements to extract
- Specify if you want all tokens or specific categories

### Validation Errors

- Check token values match W3C types (color, dimension, fontFamily, etc.)
- Ensure proper JSON structure with `$value`, `$type`, `$description`
- Review error messages from validate_tokens.py

### Format Conversion Issues

- Verify input format is valid
- Check target format is supported
- Ensure all required token properties are present

## External Resources

- [W3C Design Tokens Community Group](https://www.w3.org/community/design-tokens/)
- [Design Tokens Format Module](https://tr.designtokens.org/format/)
- [Style Dictionary](https://amzn.github.io/style-dictionary/)
- [CSS Cascade Layers](https://developer.mozilla.org/en-US/docs/Web/CSS/@layer)
- [CSS Container Queries](https://developer.mozilla.org/en-US/docs/Web/CSS/CSS_Container_Queries)

## License

See LICENSE.txt for complete terms.

## Version

Current version: 0.2.0

### Changelog

**v0.2.0** - Atomic Utility Generation
- Added comprehensive Tailwind-style atomic utility class generation
- New output formats: `utilities` (standalone) and `css-layers-full` (tokens + utilities)
- Container query variants (sm/md/lg/xl breakpoints)
- State variants (hover/focus/active)
- Dark mode support with automatic variants
- Logical properties for better internationalization
- New `generate_utilities.py` script and `utilities.template.css` template

**v1.0.0** - Initial Release
- W3C Design Tokens extraction and validation
- CSS custom properties with cascade layers
- Cross-platform export (iOS, Android, SCSS)
- Accessibility-first approach with WCAG 2.2 compliance
