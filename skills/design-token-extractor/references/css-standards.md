# Modern CSS Standards for Design Tokens

This document covers modern CSS features that should be used when implementing design tokens: cascade layers, container queries, logical properties, and other cutting-edge features.

## CSS Cascade Layers

Cascade layers provide explicit control over specificity and the cascade, making design token implementation more predictable and maintainable.

### Layer Structure for Design Tokens

```css
@layer reset, tokens, components, utilities;
```

**Recommended layer order:**
1. **reset** - Normalize and reset styles
2. **tokens** - Core design token definitions
3. **components** - Component-specific styles
4. **utilities** - Utility classes

### Layer Implementation

```css
@layer reset, tokens, components, utilities;

@layer reset {
  /* Normalize/reset styles */
  *, *::before, *::after {
    box-sizing: border-box;
    margin: 0;
    padding: 0;
  }
}

@layer tokens {
  :root {
    /* Design token definitions */
    --color-primary-500: #2563eb;
    --spacing-scale-md: 1rem;
    --font-size-lg: 1.25rem;
  }
}

@layer components {
  .button {
    /* Component styles using tokens */
    background-color: var(--color-primary-500);
    padding: var(--spacing-scale-md);
    font-size: var(--font-size-lg);
  }
}

@layer utilities {
  /* Utility classes using tokens */
  .text-primary {
    color: var(--color-primary-500);
  }
  .p-md {
    padding: var(--spacing-scale-md);
  }
}
```

### Layer Benefits

- **Predictable cascade**: Lower layers have lower priority regardless of specificity
- **Organization**: Clear separation of concerns
- **Maintainability**: Easy to understand and modify
- **No !important**: Rarely needed with proper layer structure

### Layer Specificity Rules

```css
/* Even with high specificity, reset layer is lowest priority */
@layer reset {
  #id.class[attr] {
    color: red; /* Lower priority than... */
  }
}

@layer tokens {
  div {
    color: blue; /* ...this, despite lower specificity */
  }
}
```

## Container Queries

Container queries enable responsive design based on container size rather than viewport size, perfect for component-based design tokens.

### Container Types

```css
.card {
  container-type: inline-size; /* Width-based queries */
}

.sidebar {
  container-type: size; /* Width and height queries */
}

.article {
  container-name: article;
  container-type: inline-size;
}
```

**Container types:**
- `inline-size` - Query based on inline dimension (width in horizontal writing modes)
- `size` - Query based on both dimensions
- `normal` - Not a query container

### Container Query Units

```css
.card {
  container-type: inline-size;
}

.card-content {
  /* Container query units */
  padding: 2cqi;              /* 2% of container inline size */
  font-size: clamp(1rem, 3cqi, 2rem);
  gap: 1cqb;                  /* 1% of container block size */
}
```

**Available units:**
- `cqi` - 1% of container inline size
- `cqb` - 1% of container block size
- `cqw` - 1% of container width
- `cqh` - 1% of container height
- `cqmin` - Smaller of cqi or cqb
- `cqmax` - Larger of cqi or cqb

### Container Query Syntax

```css
.card {
  container-type: inline-size;
}

/* Container query */
@container (inline-size > 400px) {
  .card {
    --card-columns: 2;
    display: grid;
    grid-template-columns: repeat(var(--card-columns), 1fr);
  }
}

@container (inline-size > 600px) {
  .card {
    --card-columns: 3;
  }
}
```

### Fluid Design Tokens with Container Units

```css
@layer tokens {
  :root {
    /* Fluid typography using container queries */
    --font-size-fluid-sm: clamp(0.875rem, 1.5cqi, 1rem);
    --font-size-fluid-md: clamp(1rem, 2.5cqi, 1.5rem);
    --font-size-fluid-lg: clamp(1.25rem, 3.5cqi, 2rem);

    /* Fluid spacing */
    --spacing-fluid-xs: clamp(0.25rem, 1cqi, 0.5rem);
    --spacing-fluid-sm: clamp(0.5rem, 2cqi, 1rem);
    --spacing-fluid-md: clamp(1rem, 3cqi, 2rem);

    /* Container-aware padding */
    --container-padding: clamp(1rem, 4cqi, 3rem);
  }
}
```

## Logical Properties

Logical properties adapt to writing modes (left-to-right, right-to-left, vertical), making tokens more versatile and internationalization-friendly.

### Physical vs. Logical Properties

```css
/* Physical properties (avoid for tokens) */
.element {
  margin-left: 1rem;
  padding-right: 2rem;
  width: 100px;
  height: 200px;
}

/* Logical properties (preferred) */
.element {
  margin-inline-start: 1rem;   /* Start of inline direction */
  padding-inline-end: 2rem;    /* End of inline direction */
  inline-size: 100px;          /* Size in inline direction */
  block-size: 200px;           /* Size in block direction */
}
```

### Logical Property Mapping

**Inline direction** (horizontal in LTR/RTL, vertical in vertical writing):
- `margin-inline-start` - Start margin (left in LTR, right in RTL)
- `margin-inline-end` - End margin (right in LTR, left in RTL)
- `padding-inline` - Shorthand for both inline paddings
- `inline-size` - Inline dimension (width in horizontal, height in vertical)

**Block direction** (vertical in LTR/RTL, horizontal in vertical writing):
- `margin-block-start` - Top in horizontal writing
- `margin-block-end` - Bottom in horizontal writing
- `padding-block` - Shorthand for both block paddings
- `block-size` - Block dimension (height in horizontal, width in vertical)

### Design Tokens with Logical Properties

```css
@layer tokens {
  :root {
    /* Spacing tokens for logical properties */
    --spacing-inline-sm: 0.5rem;
    --spacing-inline-md: 1rem;
    --spacing-inline-lg: 2rem;

    --spacing-block-sm: 0.5rem;
    --spacing-block-md: 1rem;
    --spacing-block-lg: 2rem;
  }
}

@layer components {
  .content {
    /* Use logical properties with tokens */
    margin-inline: auto;
    padding-block: var(--spacing-block-lg);
    padding-inline: var(--spacing-inline-md);
    inline-size: min(100%, 70ch);
  }
}
```

### Common Logical Properties

```css
/* Margin */
margin-inline: auto;                    /* Horizontal centering */
margin-block-start: 1rem;               /* Top margin */
margin-block-end: 2rem;                 /* Bottom margin */

/* Padding */
padding-inline: 1rem 2rem;              /* Horizontal padding */
padding-block: 0.5rem;                  /* Vertical padding */

/* Border */
border-inline-start: 1px solid black;   /* Left border (LTR) */
border-block-end: 2px solid red;        /* Bottom border */

/* Position */
inset-inline-start: 0;                  /* left: 0 (LTR) */
inset-block-start: 0;                   /* top: 0 */
```

## Modern CSS Functions for Tokens

### clamp()

Responsive values with min, preferred, and max:

```css
:root {
  /* Typography */
  --font-size-responsive: clamp(1rem, 2vw + 0.5rem, 2rem);

  /* Spacing */
  --spacing-responsive: clamp(1rem, 5cqi, 4rem);

  /* Container width */
  --container-width: clamp(20rem, 90vw, 80rem);
}
```

**Syntax:** `clamp(MIN, PREFERRED, MAX)`

### min() and max()

Choose minimum or maximum value:

```css
:root {
  /* Responsive width with max limit */
  --content-width: min(100%, 70ch);

  /* Minimum readable font size */
  --font-size-readable: max(1rem, 16px);

  /* Spacing with limits */
  --spacing-safe: min(2rem, 5vw);
}
```

### calc()

Calculate token values:

```css
:root {
  --base-size: 1rem;
  --ratio: 1.618; /* Golden ratio */

  /* Modular scale */
  --font-size-sm: calc(var(--base-size) / var(--ratio));
  --font-size-md: var(--base-size);
  --font-size-lg: calc(var(--base-size) * var(--ratio));
  --font-size-xl: calc(var(--base-size) * var(--ratio) * var(--ratio));
}
```

## Color Functions

### oklch()

Modern perceptually uniform color space:

```css
:root {
  /* Define base colors in OKLCH */
  --color-primary: oklch(60% 0.15 250);
  --color-secondary: oklch(70% 0.12 180);

  /* Generate variants */
  --color-primary-dark: oklch(50% 0.15 250);
  --color-primary-light: oklch(80% 0.15 250);
}
```

**Syntax:** `oklch(lightness chroma hue / alpha)`
- **Lightness**: 0-100%
- **Chroma**: 0-0.4 (typically)
- **Hue**: 0-360 degrees

### Relative Color Syntax

Create color variations from existing tokens:

```css
:root {
  --color-primary: oklch(60% 0.15 250);
}

.button {
  background-color: var(--color-primary);

  /* Darken on hover */
  &:hover {
    background-color: oklch(from var(--color-primary) calc(l * 0.8) c h);
  }

  /* Adjust opacity */
  border-color: oklch(from var(--color-primary) l c h / 0.5);
}
```

## Nesting

Native CSS nesting for better token organization:

```css
@layer components {
  .card {
    background: var(--color-surface);
    padding: var(--spacing-md);

    & .card-title {
      font-size: var(--font-size-lg);
      margin-block-end: var(--spacing-sm);
    }

    & .card-content {
      color: var(--color-text-secondary);
    }

    &:hover {
      box-shadow: var(--shadow-md);
    }
  }
}
```

## Best Practices

### 1. Use Cascade Layers

```css
@layer reset, tokens, components, utilities;
```

### 2. Prefer Logical Properties

```css
/* Good */
margin-inline: auto;
padding-block: 1rem;

/* Avoid */
margin-left: auto;
margin-right: auto;
padding-top: 1rem;
padding-bottom: 1rem;
```

### 3. Use Container Queries for Components

```css
.component {
  container-type: inline-size;
}

@container (inline-size > 400px) {
  .component-child {
    --columns: 2;
  }
}
```

### 4. Leverage Modern Color Spaces

```css
/* OKLCH for perceptual uniformity */
--color-primary: oklch(60% 0.15 250);

/* Relative colors for variants */
--color-primary-hover: oklch(from var(--color-primary) calc(l * 0.9) c h);
```

### 5. Create Fluid Tokens

```css
/* Responsive without media queries */
--spacing-fluid: clamp(1rem, 3cqi, 3rem);
--font-fluid: clamp(1rem, 2.5cqi + 0.5rem, 2rem);
```

## Browser Support

All features mentioned have good modern browser support:

- **Cascade Layers**: Chrome 99+, Firefox 97+, Safari 15.4+
- **Container Queries**: Chrome 105+, Firefox 110+, Safari 16.0+
- **Logical Properties**: Chrome 89+, Firefox 66+, Safari 12.1+
- **OKLCH**: Chrome 111+, Firefox 113+, Safari 15.4+
- **Nesting**: Chrome 112+, Firefox 117+, Safari 16.5+

For production, consider progressive enhancement and fallbacks for older browsers.
