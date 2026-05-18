# Design Tokens Documentation

This document provides comprehensive documentation for the design tokens extracted from {{SOURCE_NAME}}.

## Overview

**Generated:** {{GENERATION_DATE}}
**Source:** {{SOURCE_NAME}}
**Token Count:** {{TOKEN_COUNT}}

## Color Tokens

### Primary Colors

Primary colors are used for brand identity, key actions, and emphasis.

| Token | Value | Usage |
|-------|-------|-------|
| `--color-primary-50` | {{COLOR_PRIMARY_50}} | Lightest primary, backgrounds |
| `--color-primary-100` | {{COLOR_PRIMARY_100}} | Very light primary, hover states |
| `--color-primary-500` | {{COLOR_PRIMARY_500}} | Main brand color |
| `--color-primary-900` | {{COLOR_PRIMARY_900}} | Darkest primary, text on light |

**Accessibility:**
- Primary-500 on white: {{PRIMARY_500_CONTRAST}} contrast ratio
- Primary-900 on white: {{PRIMARY_900_CONTRAST}} contrast ratio

### Neutral Colors

Neutral colors for text, borders, and backgrounds.

| Token | Value | Usage |
|-------|-------|-------|
| `--color-neutral-50` | {{COLOR_NEUTRAL_50}} | Lightest backgrounds |
| `--color-neutral-500` | {{COLOR_NEUTRAL_500}} | Borders, secondary text |
| `--color-neutral-900` | {{COLOR_NEUTRAL_900}} | Primary text color |

### Semantic Colors

| Token | References | Usage |
|-------|------------|-------|
| `--color-text-primary` | `var(--color-neutral-900)` | Primary text |
| `--color-text-secondary` | `var(--color-neutral-500)` | Secondary text |
| `--color-background` | `var(--color-neutral-50)` | Page background |

## Typography Tokens

### Font Families

| Token | Value | Usage |
|-------|-------|-------|
| `--font-family-display` | {{FONT_FAMILY_DISPLAY}} | Headings, display text |
| `--font-family-body` | {{FONT_FAMILY_BODY}} | Body text, UI elements |
| `--font-family-mono` | {{FONT_FAMILY_MONO}} | Code, monospace text |

### Font Sizes

| Token | Value | Example |
|-------|-------|---------|
| `--font-size-xs` | {{FONT_SIZE_XS}} | Small labels, captions |
| `--font-size-sm` | {{FONT_SIZE_SM}} | Secondary text |
| `--font-size-base` | {{FONT_SIZE_BASE}} | Body text (default) |
| `--font-size-lg` | {{FONT_SIZE_LG}} | Subheadings |
| `--font-size-xl` | {{FONT_SIZE_XL}} | Main headings |

### Fluid Typography

Responsive font sizes using `clamp()`:

| Token | Min | Preferred | Max |
|-------|-----|-----------|-----|
| `--font-size-fluid-sm` | 0.875rem | 1.5cqi | 1rem |
| `--font-size-fluid-md` | 1rem | 2.5cqi | 1.5rem |
| `--font-size-fluid-lg` | 1.25rem | 3.5cqi | 2rem |

### Font Weights

| Token | Value | Usage |
|-------|-------|-------|
| `--font-weight-normal` | 400 | Body text |
| `--font-weight-medium` | 500 | Emphasis |
| `--font-weight-semibold` | 600 | Strong emphasis |
| `--font-weight-bold` | 700 | Headings |

### Line Heights

| Token | Value | Usage |
|-------|-------|-------|
| `--line-height-tight` | 1.25 | Headings |
| `--line-height-normal` | 1.5 | Body text (WCAG compliant) |
| `--line-height-relaxed` | 1.75 | Enhanced readability |

## Spacing Tokens

### Spacing Scale

Consistent spacing using mathematical progression:

| Token | Value | Multiplier |
|-------|-------|------------|
| `--spacing-scale-xs` | {{SPACING_XS}} | 0.25× |
| `--spacing-scale-sm` | {{SPACING_SM}} | 0.5× |
| `--spacing-scale-md` | {{SPACING_MD}} | 1× (base) |
| `--spacing-scale-lg` | {{SPACING_LG}} | 2× |
| `--spacing-scale-xl` | {{SPACING_XL}} | 4× |

### Fluid Spacing

Container-aware spacing using `clamp()`:

| Token | Min | Preferred | Max |
|-------|-----|-----------|-----|
| `--spacing-fluid-xs` | 0.25rem | 1cqi | 0.5rem |
| `--spacing-fluid-sm` | 0.5rem | 2cqi | 1rem |
| `--spacing-fluid-md` | 1rem | 3cqi | 2rem |
| `--spacing-fluid-lg` | 2rem | 5cqi | 4rem |

## Dimension Tokens

### Border Radius

| Token | Value | Usage |
|-------|-------|-------|
| `--border-radius-none` | 0 | Sharp corners |
| `--border-radius-sm` | {{BORDER_RADIUS_SM}} | Subtle rounding |
| `--border-radius-md` | {{BORDER_RADIUS_MD}} | Standard buttons, cards |
| `--border-radius-lg` | {{BORDER_RADIUS_LG}} | Prominent elements |
| `--border-radius-full` | 9999px | Circular/pill shapes |

### Shadows

| Token | Value | Usage |
|-------|-------|-------|
| `--shadow-sm` | 0 1px 2px 0 {{SHADOW_COLOR}} | Subtle depth |
| `--shadow-md` | 0 4px 6px -1px {{SHADOW_COLOR}} | Cards, modals |
| `--shadow-lg` | 0 10px 15px -3px {{SHADOW_COLOR}} | Floating elements |

## Motion Tokens

### Durations

| Token | Value | Usage |
|-------|-------|-------|
| `--duration-fast` | {{DURATION_FAST}} | Quick transitions |
| `--duration-normal` | {{DURATION_NORMAL}} | Standard animations |
| `--duration-slow` | {{DURATION_SLOW}} | Emphasis animations |

**Note:** All durations respect `prefers-reduced-motion` and become 0ms when users prefer reduced motion.

### Easing Functions

| Token | Cubic Bezier | Usage |
|-------|--------------|-------|
| `--easing-standard` | cubic-bezier(0.4, 0.0, 0.2, 1) | General purpose |
| `--easing-enter` | cubic-bezier(0.0, 0.0, 0.2, 1) | Elements entering |
| `--easing-exit` | cubic-bezier(0.4, 0.0, 1, 1) | Elements exiting |

## Accessibility Tokens

### Focus Indicators

| Token | Value | WCAG Requirement |
|-------|-------|------------------|
| `--focus-ring-color` | #0066cc | 3:1 contrast required |
| `--focus-ring-width` | 2px | 2px minimum perimeter |
| `--focus-ring-offset` | 2px | Visual separation |

### Touch Targets

| Token | Value | Standard |
|-------|-------|----------|
| `--touch-target-min` | 24px | WCAG AA minimum |
| `--touch-target-comfortable` | 44px | Recommended |

## Usage Examples

### Basic Usage

```css
.button {
  background-color: var(--color-primary-500);
  color: var(--color-surface);
  padding: var(--spacing-scale-md);
  border-radius: var(--border-radius-sm);
  font-size: var(--font-size-base);
  font-weight: var(--font-weight-medium);
}
```

### Container Queries

```css
.card {
  container-type: inline-size;
  padding: var(--container-padding-inline);
}

@container (inline-size > 400px) {
  .card {
    display: grid;
    grid-template-columns: repeat(2, 1fr);
    gap: var(--spacing-scale-md);
  }
}
```

### Logical Properties

```css
.content {
  margin-inline: auto;
  padding-block: var(--spacing-scale-lg);
  padding-inline: var(--spacing-fluid-md);
  inline-size: min(100%, 70ch);
}
```

## Implementation Notes

### Browser Support

- **Cascade Layers**: Chrome 99+, Firefox 97+, Safari 15.4+
- **Container Queries**: Chrome 105+, Firefox 110+, Safari 16.0+
- **Logical Properties**: Chrome 89+, Firefox 66+, Safari 12.1+

### Integration

1. Import the token file in your main CSS
2. Use cascade layers for proper organization
3. Respect motion and contrast preferences
4. Test with accessibility tools

## Validation

Tokens validated against:
- W3C Design Tokens Community Group specification
- WCAG 2.2 Level AA accessibility standards
- Modern CSS standards (cascade layers, container queries)

## Resources

- [W3C DTCG Specification](https://tr.designtokens.org/format/)
- [CSS Cascade Layers](https://developer.mozilla.org/en-US/docs/Web/CSS/@layer)
- [Container Queries](https://developer.mozilla.org/en-US/docs/Web/CSS/CSS_Container_Queries)
- [WCAG 2.2](https://www.w3.org/WAI/WCAG22/quickref/)

---

**Last Updated:** {{GENERATION_DATE}}
