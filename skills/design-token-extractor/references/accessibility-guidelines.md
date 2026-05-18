# Accessibility Guidelines for Design Tokens

This document covers WCAG 2.2 Level AA accessibility requirements that design tokens must meet, including color contrast, focus indicators, motion preferences, and more.

## WCAG 2.2 Overview

Web Content Accessibility Guidelines (WCAG) 2.2 is the current standard for web accessibility. Level AA is the recommended conformance level for most websites and applications.

## Color Contrast Requirements

### Text Contrast (WCAG 1.4.3)

**Normal text** (< 18pt or < 14pt bold):
- Minimum contrast ratio: **4.5:1**

**Large text** (≥ 18pt or ≥ 14pt bold):
- Minimum contrast ratio: **3:1**

### Examples

```css
/* PASS: 4.51:1 contrast ratio */
--color-text-on-white: #595959;  /* on #ffffff */

/* FAIL: 3.2:1 contrast ratio */
--color-text-on-white-fail: #999999;  /* on #ffffff */

/* PASS: Large text at 3:1 */
--color-heading-on-white: #767676;  /* on #ffffff, 18pt+ */
```

### Contrast Calculation

Use the WCAG formula:

```
Contrast Ratio = (L1 + 0.05) / (L2 + 0.05)
```

Where:
- L1 = Relative luminance of lighter color
- L2 = Relative luminance of darker color
- L ranges from 0 (black) to 1 (white)

### Tools for Checking Contrast

- **Online**: WebAIM Contrast Checker, Coolors Contrast Checker
- **Browser DevTools**: Chrome, Firefox, Edge have built-in contrast checkers
- **Design Tools**: Figma plugins (Stark, Contrast), Sketch plugins

### Color Palettes with Guaranteed Contrast

Create color scales where adjacent colors don't meet contrast requirements, forcing proper pairing:

```json
{
  "color": {
    "gray": {
      "50": {"$value": "#fafafa", "$type": "color"},
      "100": {"$value": "#f5f5f5", "$type": "color"},
      "200": {"$value": "#e5e5e5", "$type": "color"},
      "300": {"$value": "#d4d4d4", "$type": "color"},
      "400": {"$value": "#a3a3a3", "$type": "color"},
      "500": {"$value": "#737373", "$type": "color"},
      "600": {"$value": "#525252", "$type": "color"},
      "700": {"$value": "#404040", "$type": "color"},
      "800": {"$value": "#262626", "$type": "color"},
      "900": {"$value": "#171717", "$type": "color"}
    }
  }
}
```

**Safe pairings** (4.5:1+ contrast):
- 50-700, 50-800, 50-900
- 100-700, 100-800, 100-900
- 200-800, 200-900
- 900-50, 900-100, 900-200, 900-300

## Non-Text Contrast (WCAG 1.4.11)

**UI Components and graphical objects**:
- Minimum contrast ratio: **3:1** against adjacent colors

This applies to:
- Form input borders
- Focus indicators
- Icons (when meaning isn't conveyed through text)
- Charts and graphs
- Custom controls

### Examples

```css
/* PASS: Button border at 3.2:1 against background */
--color-button-border: #767676;  /* on #ffffff */

/* FAIL: Input border at 2.1:1 */
--color-input-border-fail: #c0c0c0;  /* on #ffffff */

/* PASS: Focus indicator at 3:1 */
--color-focus-ring: #0066cc;  /* on #ffffff */
```

## Focus Indicators (WCAG 2.4.7, 2.4.13)

### Basic Requirements

**WCAG 2.4.7** (Level AA):
- Focus indicators must be visible
- Cannot rely solely on color change

**WCAG 2.4.13** (Level AAA, but recommended):
- Focus indicators must have 3:1 contrast against adjacent colors
- Minimum area of 2px CSS pixels (perimeter or 1px outline)

### Focus Token Examples

```css
@layer tokens {
  :root {
    /* Focus ring */
    --focus-ring-color: #0066cc;
    --focus-ring-width: 2px;
    --focus-ring-offset: 2px;
    --focus-ring-style: solid;

    /* Focus ring with high visibility */
    --focus-ring-color-high-contrast: #000000;
    --focus-ring-width-high-contrast: 3px;
  }
}

@layer components {
  button:focus-visible {
    outline: var(--focus-ring-width) var(--focus-ring-style) var(--focus-ring-color);
    outline-offset: var(--focus-ring-offset);
  }
}
```

### Focus Indicator Patterns

**Outline (recommended)**:
```css
:focus-visible {
  outline: 2px solid var(--color-focus);
  outline-offset: 2px;
}
```

**Box shadow** (when outline isn't suitable):
```css
:focus-visible {
  box-shadow: 0 0 0 3px var(--color-focus-ring);
}
```

**Combined** (maximum visibility):
```css
:focus-visible {
  outline: 2px solid var(--color-focus);
  outline-offset: 2px;
  box-shadow: 0 0 0 4px var(--color-focus-glow);
}
```

## Motion and Animation (WCAG 2.3.3)

### Reduced Motion

Users can indicate motion sensitivity via `prefers-reduced-motion` media query. Design tokens should respect this preference.

### Motion Tokens

```css
@layer tokens {
  :root {
    /* Default motion */
    --duration-fast: 150ms;
    --duration-normal: 300ms;
    --duration-slow: 500ms;

    --easing-standard: cubic-bezier(0.4, 0.0, 0.2, 1);
    --easing-enter: cubic-bezier(0.0, 0.0, 0.2, 1);
    --easing-exit: cubic-bezier(0.4, 0.0, 1, 1);
  }

  /* Respect reduced motion preference */
  @media (prefers-reduced-motion: reduce) {
    :root {
      --duration-fast: 0ms;
      --duration-normal: 0ms;
      --duration-slow: 0ms;

      /* Or use very short durations instead of none */
      --duration-fast: 50ms;
      --duration-normal: 50ms;
      --duration-slow: 50ms;
    }
  }
}
```

### Animation Best Practices

```css
.button {
  transition: background-color var(--duration-fast) var(--easing-standard);
}

/* Disable when user prefers reduced motion */
@media (prefers-reduced-motion: reduce) {
  .button {
    transition: none;
  }
}

/* Or use tokens that auto-adjust */
.card {
  /* Duration automatically becomes 0ms or 50ms with reduced motion */
  transition: transform var(--duration-normal) var(--easing-standard);
}
```

## Color Blind Considerations

Don't rely solely on color to convey information.

### Good Practices

**Use multiple indicators**:
```css
/* Good: Color + icon + text */
.success {
  color: var(--color-success);
  &::before {
    content: "✓ ";
  }
}

/* Bad: Color only */
.success {
  color: green;
}
```

**Ensure contrast with colorblindness**:
- Red-green colorblindness (protanopia/deuteranopia): Most common
- Blue-yellow colorblindness (tritanopia): Less common
- Complete colorblindness (achromatopsia): Rare

Test color palettes with colorblindness simulators.

### Safe Color Combinations

These color combinations work well for colorblind users:

- **Blue + Orange**: High contrast for all types
- **Purple + Yellow**: Good differentiation
- **Cyan + Magenta**: Clear separation

**Avoid**:
- Red + Green (indistinguishable for red-green colorblindness)
- Blue + Purple (hard to distinguish for some)

## Typography Tokens for Accessibility

### Minimum Font Sizes

**WCAG doesn't specify minimum font size**, but best practices:
- Body text: 16px (1rem) minimum
- Small text: 14px (0.875rem) minimum
- Captions/labels: 12px (0.75rem) absolute minimum

### Line Height

**WCAG 1.4.12** requires:
- Line height: At least 1.5× font size for paragraphs
- Paragraph spacing: At least 2× font size

```css
@layer tokens {
  :root {
    /* Typography tokens */
    --font-size-sm: 0.875rem;   /* 14px */
    --font-size-base: 1rem;      /* 16px */
    --font-size-lg: 1.25rem;     /* 20px */

    /* Line heights (1.5× minimum for body text) */
    --line-height-tight: 1.25;
    --line-height-normal: 1.5;   /* WCAG compliant */
    --line-height-relaxed: 1.75;

    /* Paragraph spacing (2× font size minimum) */
    --paragraph-spacing: 2em;
  }
}
```

### Letter Spacing

**WCAG 1.4.12** requires support for:
- Letter spacing: At least 0.12× font size
- Word spacing: At least 0.16× font size

```css
:root {
  /* Support user overrides */
  --letter-spacing-normal: normal;
  --letter-spacing-wide: 0.05em;
  --letter-spacing-wider: 0.1em;

  --word-spacing-normal: normal;
  --word-spacing-wide: 0.16em;
}
```

## Interactive Element Sizing (WCAG 2.5.5)

**Target Size** (Level AAA, but recommended):
- Minimum: 24×24 CSS pixels
- Recommended: 44×44 CSS pixels (easier for motor impairments)

```css
@layer tokens {
  :root {
    /* Interactive element sizing */
    --touch-target-min: 24px;
    --touch-target-comfortable: 44px;

    /* Button tokens */
    --button-height-sm: 32px;
    --button-height-md: 44px;   /* Comfortable touch target */
    --button-height-lg: 56px;

    --button-padding-inline: 1rem;
    --button-min-width: 44px;
  }
}

@layer components {
  .button {
    min-block-size: var(--button-height-md);
    min-inline-size: var(--button-min-width);
    padding-inline: var(--button-padding-inline);
  }
}
```

## High Contrast Mode

Support Windows High Contrast Mode and forced-colors media query.

```css
@layer tokens {
  :root {
    --color-text: #1a1a1a;
    --color-background: #ffffff;
    --color-border: #d4d4d4;
  }

  /* Forced colors mode (high contrast) */
  @media (forced-colors: active) {
    :root {
      /* Use system colors */
      --color-text: CanvasText;
      --color-background: Canvas;
      --color-border: ButtonBorder;
      --color-link: LinkText;
    }
  }
}
```

## Testing Checklist

### Color Contrast
- [ ] All text meets 4.5:1 (normal) or 3:1 (large)
- [ ] UI components meet 3:1 against adjacent colors
- [ ] Focus indicators meet 3:1 contrast
- [ ] Tested with colorblindness simulators

### Focus Indicators
- [ ] Visible on all interactive elements
- [ ] 2px minimum perimeter or 1px outline
- [ ] Uses :focus-visible to avoid mouse focus rings

### Motion
- [ ] Respects prefers-reduced-motion
- [ ] No flashing content (3+ times per second)
- [ ] Animations have reduced/disabled alternative

### Typography
- [ ] Line height 1.5× minimum for body text
- [ ] Paragraph spacing 2× font size
- [ ] Supports letter/word spacing overrides

### Touch Targets
- [ ] 24×24px minimum (44×44px recommended)
- [ ] Adequate spacing between targets

### Tools
- **Contrast**: WebAIM Contrast Checker, browser DevTools
- **Colorblind simulation**: Stark, Color Oracle, browser DevTools
- **Screen readers**: NVDA (Windows), JAWS (Windows), VoiceOver (macOS/iOS)
- **Automated testing**: axe DevTools, Lighthouse, WAVE

## Resources

- **WCAG 2.2**: https://www.w3.org/WAI/WCAG22/quickref/
- **WebAIM**: https://webaim.org/
- **A11y Project**: https://www.a11yproject.com/
- **MDN Accessibility**: https://developer.mozilla.org/en-US/docs/Web/Accessibility
- **Contrast Checker**: https://webaim.org/resources/contrastchecker/
