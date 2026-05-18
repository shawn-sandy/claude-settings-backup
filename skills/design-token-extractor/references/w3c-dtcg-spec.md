# W3C Design Tokens Community Group (DTCG) Specification

This document summarizes the W3C Design Tokens Community Group specification for creating standards-compliant design token files.

## Overview

The W3C DTCG specification defines a standard format for design tokens that can be shared across design tools, platforms, and teams. Tokens represent design decisions (colors, spacing, typography, etc.) in a platform-agnostic format.

## Token Structure

### Basic Token Format

Every design token must have:

```json
{
  "token-name": {
    "$value": "value",
    "$type": "type",
    "$description": "optional description"
  }
}
```

### Required Fields

- **$value**: The actual value of the token (required)
- **$type**: The type of token (recommended, required in some contexts)

### Optional Fields

- **$description**: Human-readable description of the token's purpose
- **$extensions**: Vendor-specific metadata (not part of standard)

## Token Types

### Color

Represents color values. Supports multiple formats:

```json
{
  "color": {
    "primary": {
      "$value": "#2563eb",
      "$type": "color",
      "$description": "Primary brand color"
    },
    "accent": {
      "$value": "rgb(37, 99, 235)",
      "$type": "color"
    },
    "background": {
      "$value": "hsl(217, 91%, 60%)",
      "$type": "color"
    }
  }
}
```

**Valid formats:**
- Hex: `#RGB`, `#RRGGBB`, `#RRGGBBAA`
- RGB: `rgb(r, g, b)`, `rgba(r, g, b, a)`
- HSL: `hsl(h, s%, l%)`, `hsla(h, s%, l%, a)`
- OKLCH: `oklch(l c h)` (modern color space)

### Dimension

Represents dimensional values (spacing, sizing, border radius, etc.):

```json
{
  "spacing": {
    "small": {
      "$value": "0.5rem",
      "$type": "dimension"
    },
    "medium": {
      "$value": "1rem",
      "$type": "dimension"
    }
  }
}
```

**Valid units:** `px`, `rem`, `em`, `%`, `vw`, `vh`, `vmin`, `vmax`, `cqi`, `cqb`, `cqw`, `cqh`, `cqmin`, `cqmax`

### Font Family

Represents font family values:

```json
{
  "fontFamily": {
    "body": {
      "$value": ["Inter", "system-ui", "sans-serif"],
      "$type": "fontFamily"
    },
    "mono": {
      "$value": "Roboto Mono",
      "$type": "fontFamily"
    }
  }
}
```

**Value types:**
- String: Single font family
- Array: Font stack (preferred → fallback)

### Font Weight

Represents font weight values:

```json
{
  "fontWeight": {
    "normal": {
      "$value": "400",
      "$type": "fontWeight"
    },
    "bold": {
      "$value": "700",
      "$type": "fontWeight"
    }
  }
}
```

**Valid values:**
- Numbers: `100`, `200`, `300`, `400`, `500`, `600`, `700`, `800`, `900`
- Keywords: `normal` (400), `bold` (700)

### Duration

Represents animation/transition duration:

```json
{
  "duration": {
    "fast": {
      "$value": "150ms",
      "$type": "duration"
    },
    "slow": {
      "$value": "0.5s",
      "$type": "duration"
    }
  }
}
```

**Valid units:** `ms` (milliseconds), `s` (seconds)

### Cubic Bezier

Represents easing functions for animations:

```json
{
  "easing": {
    "ease-in": {
      "$value": [0.42, 0, 1, 1],
      "$type": "cubicBezier"
    },
    "custom": {
      "$value": [0.25, 0.1, 0.25, 1],
      "$type": "cubicBezier"
    }
  }
}
```

**Value format:** Array of 4 numbers `[x1, y1, x2, y2]`

### Number

Represents unitless numeric values (line height, opacity, etc.):

```json
{
  "lineHeight": {
    "tight": {
      "$value": 1.25,
      "$type": "number"
    },
    "relaxed": {
      "$value": 1.75,
      "$type": "number"
    }
  }
}
```

### Composite Types

#### Shadow

Represents box shadow or drop shadow:

```json
{
  "shadow": {
    "small": {
      "$value": {
        "offsetX": "0px",
        "offsetY": "2px",
        "blur": "4px",
        "spread": "0px",
        "color": "#00000026"
      },
      "$type": "shadow"
    }
  }
}
```

#### Border

Represents border properties:

```json
{
  "border": {
    "default": {
      "$value": {
        "color": "#e5e7eb",
        "width": "1px",
        "style": "solid"
      },
      "$type": "border"
    }
  }
}
```

#### Typography

Composite type combining multiple typography properties:

```json
{
  "typography": {
    "heading": {
      "$value": {
        "fontFamily": "{fontFamily.display}",
        "fontSize": "{fontSize.2xl}",
        "fontWeight": "{fontWeight.bold}",
        "lineHeight": "{lineHeight.tight}"
      },
      "$type": "typography"
    }
  }
}
```

## Token References (Aliases)

Tokens can reference other tokens using curly brace syntax:

```json
{
  "color": {
    "blue-500": {
      "$value": "#2563eb",
      "$type": "color"
    },
    "primary": {
      "$value": "{color.blue-500}",
      "$type": "color",
      "$description": "Alias to blue-500 for semantic naming"
    }
  }
}
```

**Benefits:**
- Single source of truth
- Semantic naming
- Easy theme switching
- Maintain relationships between tokens

## Token Groups

Organize tokens hierarchically using nested objects:

```json
{
  "color": {
    "primary": {
      "50": { "$value": "#eff6ff", "$type": "color" },
      "100": { "$value": "#dbeafe", "$type": "color" },
      "500": { "$value": "#2563eb", "$type": "color" },
      "900": { "$value": "#1e3a8a", "$type": "color" }
    },
    "neutral": {
      "50": { "$value": "#fafafa", "$type": "color" },
      "500": { "$value": "#737373", "$type": "color" },
      "900": { "$value": "#171717", "$type": "color" }
    }
  }
}
```

**Group naming conventions:**
- Use semantic names when possible (primary, secondary, success, error)
- Use consistent scales (50-900 for colors, xs-xl for sizes)
- Group related tokens together

## Naming Conventions

### Best Practices

1. **Use kebab-case**: `border-radius-small`, not `borderRadiusSmall`
2. **Be semantic**: `color-primary`, not `color-blue`
3. **Use hierarchies**: `spacing-scale-md`, not `spacing-medium`
4. **Avoid abbreviations**: `background-color`, not `bg-color` (except common ones like `xl`, `sm`)

### Hierarchical Structure

```
category → subcategory → variant → scale
```

Examples:
- `color-primary-500`
- `spacing-scale-md`
- `font-size-heading-lg`
- `border-radius-button-sm`

## File Format

### JSON (Required)

The standard format is JSON:

```json
{
  "color": {
    "primary": {
      "$value": "#2563eb",
      "$type": "color"
    }
  }
}
```

### File Extensions

- `.tokens.json` - Recommended for clarity
- `.json` - Also valid

## Validation Rules

### Value Validation

1. **Colors** must be valid CSS color values
2. **Dimensions** must have valid CSS units or be unitless numbers
3. **Font weights** must be 100-900 or 'normal'/'bold'
4. **Durations** must have `ms` or `s` units
5. **Cubic beziers** must be arrays of 4 numbers

### Reference Validation

1. Referenced tokens must exist
2. No circular references
3. Reference syntax: `{group.subgroup.token-name}`

### Type Validation

1. `$type` must be one of the valid token types
2. `$value` must match the type requirements
3. Composite types must have all required properties

## Cross-Platform Compatibility

Design tokens should work across:

- **Web**: CSS, SCSS, styled-components
- **iOS**: Swift, UIKit, SwiftUI
- **Android**: Kotlin, Jetpack Compose
- **Design Tools**: Figma, Sketch, Adobe XD

### Transformation Tools

- **Style Dictionary** (Amazon): Most popular token transformer
- **Theo** (Salesforce): Token transformation
- **design-tokens** (Various): Community tools

## Versioning

Version your token files to track changes:

```json
{
  "$version": "1.0.0",
  "color": {
    "primary": {
      "$value": "#2563eb",
      "$type": "color"
    }
  }
}
```

Use semantic versioning (MAJOR.MINOR.PATCH):
- **MAJOR**: Breaking changes to token structure
- **MINOR**: New tokens added
- **PATCH**: Value updates, bug fixes

## Resources

- **Specification**: https://tr.designtokens.org/format/
- **Community Group**: https://www.w3.org/community/design-tokens/
- **GitHub**: https://github.com/design-tokens/community-group
- **Examples**: https://github.com/design-tokens/community-group/tree/main/examples
