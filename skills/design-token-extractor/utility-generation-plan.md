# Design Token Extractor Enhancement Plan
## Adding Atomic Utility Class Generation

**Date**: 2025-11-23
**Version**: 0.2.0 (planned)
**Scope**: Add comprehensive Tailwind-style atomic utility class generation with full variant support

---

## Requirements Summary

Based on user requirements:
- **Style**: Atomic utilities (Tailwind-style) - granular, single-purpose classes
- **Token Categories**: Colors, Spacing, Typography, Layout (all categories)
- **Integration**: All approaches (standalone file, enhanced templates, new transformation script)
- **Variants**: Container queries, State variants (hover/focus/active), Dark mode

---

## Implementation Steps

### 1. Create New Utility Generation Script

**File**: `scripts/generate_utilities.py`

**Purpose**: Parse W3C JSON tokens and generate atomic utility classes

**Features**:
- Parse W3C DTCG JSON format tokens
- Generate atomic utilities for each token type:

  **Color Utilities**:
  - `.text-{name}` - Text color
  - `.bg-{name}` - Background color
  - `.border-{name}` - Border color
  - `.fill-{name}` - SVG fill color
  - `.stroke-{name}` - SVG stroke color

  **Spacing Utilities** (with logical properties):
  - `.p-{size}` - Padding (all sides)
  - `.px-{size}` - Padding inline (horizontal)
  - `.py-{size}` - Padding block (vertical)
  - `.pt-{size}`, `.pr-{size}`, `.pb-{size}`, `.pl-{size}` - Individual sides
  - `.m-{size}` - Margin (all sides)
  - `.mx-{size}` - Margin inline (horizontal)
  - `.my-{size}` - Margin block (vertical)
  - `.mt-{size}`, `.mr-{size}`, `.mb-{size}`, `.ml-{size}` - Individual sides
  - `.gap-{size}` - Grid/flex gap
  - `.gap-x-{size}`, `.gap-y-{size}` - Directional gap

  **Typography Utilities**:
  - `.font-{family}` - Font family
  - `.text-{size}` - Font size
  - `.font-{weight}` - Font weight
  - `.leading-{height}` - Line height
  - `.tracking-{spacing}` - Letter spacing

  **Layout Utilities**:
  - `.rounded-{size}` - Border radius
  - `.shadow-{name}` - Box shadow
  - `.w-{size}` - Width
  - `.h-{size}` - Height

- Generate all variant types:

  **Container Query Variants**:
  ```css
  @container (min-width: {breakpoint}) {
    .{bp}\:{utility} { /* styles */ }
  }
  ```
  Examples: `.md:text-lg`, `.lg:p-4`, `.xl:grid-cols-3`

  **State Variants**:
  ```css
  .hover\:{utility}:hover { /* styles */ }
  .focus\:{utility}:focus { /* styles */ }
  .active\:{utility}:active { /* styles */ }
  ```
  Examples: `.hover:bg-primary`, `.focus:outline-accent`, `.active:scale-95`

  **Dark Mode Variants**:
  ```css
  @media (prefers-color-scheme: dark) {
    .dark\:{utility} { /* styles */ }
  }
  ```
  Examples: `.dark:bg-neutral-900`, `.dark:text-neutral-100`

  **Accessibility Variants** (auto-included):
  ```css
  @media (prefers-reduced-motion: reduce) {
    .motion-safe\:{utility} { /* styles */ }
  }
  ```

**Technical Approach**:
- Use modern CSS features:
  - Logical properties (`padding-inline` instead of `padding-left/right`)
  - Cascade layers for specificity control
  - Container queries for responsive design
  - CSS custom properties for values
- Support configuration object:
  ```python
  config = {
      'categories': ['colors', 'spacing', 'typography', 'layout'],
      'variants': ['container', 'state', 'dark-mode'],
      'prefix': '',  # Optional prefix like 'tw-'
      'separator': ':',  # Variant separator
      'output_format': 'css'  # css, scss, or both
  }
  ```

**Function Signature**:
```python
def generate_utilities(
    tokens_json_path: str,
    output_path: str,
    config: dict = None
) -> None:
    """
    Generate atomic utility classes from W3C DTCG tokens.

    Args:
        tokens_json_path: Path to W3C JSON tokens file
        output_path: Path to write generated utilities CSS
        config: Configuration dict for customization
    """
```

---

### 2. Create Standalone Utilities Template

**File**: `templates/utilities.template.css`

**Purpose**: Standalone CSS file with all generated utilities organized by cascade layers

**Structure**:
```css
/**
 * Design System Utilities
 * Auto-generated from design tokens
 *
 * Organization:
 * - utilities.colors: Text, background, border color utilities
 * - utilities.spacing: Padding, margin, gap utilities with logical properties
 * - utilities.typography: Font family, size, weight, line-height utilities
 * - utilities.layout: Border radius, shadows, dimensions
 * - utilities.variants: Container queries, state variants, dark mode
 */

@layer utilities.reset,
       utilities.colors,
       utilities.spacing,
       utilities.typography,
       utilities.layout,
       utilities.variants;

/* Reset layer for utility-specific resets */
@layer utilities.reset {
  /* Allow utilities to override component styles */
}

/* ============================================
   COLOR UTILITIES
   ============================================ */
@layer utilities.colors {

  /* Text Colors */
  /* ---------------------------------------- */
  {{TEXT_COLOR_UTILITIES}}

  /* Background Colors */
  /* ---------------------------------------- */
  {{BACKGROUND_COLOR_UTILITIES}}

  /* Border Colors */
  /* ---------------------------------------- */
  {{BORDER_COLOR_UTILITIES}}

  /* Fill Colors (SVG) */
  /* ---------------------------------------- */
  {{FILL_COLOR_UTILITIES}}

  /* Stroke Colors (SVG) */
  /* ---------------------------------------- */
  {{STROKE_COLOR_UTILITIES}}
}

/* ============================================
   SPACING UTILITIES
   ============================================ */
@layer utilities.spacing {

  /* Padding - All Sides */
  /* ---------------------------------------- */
  {{PADDING_ALL_UTILITIES}}

  /* Padding - Inline (Horizontal) */
  /* ---------------------------------------- */
  {{PADDING_INLINE_UTILITIES}}

  /* Padding - Block (Vertical) */
  /* ---------------------------------------- */
  {{PADDING_BLOCK_UTILITIES}}

  /* Padding - Individual Sides */
  /* ---------------------------------------- */
  {{PADDING_INDIVIDUAL_UTILITIES}}

  /* Margin - All Sides */
  /* ---------------------------------------- */
  {{MARGIN_ALL_UTILITIES}}

  /* Margin - Inline (Horizontal) */
  /* ---------------------------------------- */
  {{MARGIN_INLINE_UTILITIES}}

  /* Margin - Block (Vertical) */
  /* ---------------------------------------- */
  {{MARGIN_BLOCK_UTILITIES}}

  /* Margin - Individual Sides */
  /* ---------------------------------------- */
  {{MARGIN_INDIVIDUAL_UTILITIES}}

  /* Gap Utilities */
  /* ---------------------------------------- */
  {{GAP_UTILITIES}}
}

/* ============================================
   TYPOGRAPHY UTILITIES
   ============================================ */
@layer utilities.typography {

  /* Font Family */
  /* ---------------------------------------- */
  {{FONT_FAMILY_UTILITIES}}

  /* Font Size */
  /* ---------------------------------------- */
  {{FONT_SIZE_UTILITIES}}

  /* Font Weight */
  /* ---------------------------------------- */
  {{FONT_WEIGHT_UTILITIES}}

  /* Line Height */
  /* ---------------------------------------- */
  {{LINE_HEIGHT_UTILITIES}}

  /* Letter Spacing */
  /* ---------------------------------------- */
  {{LETTER_SPACING_UTILITIES}}
}

/* ============================================
   LAYOUT UTILITIES
   ============================================ */
@layer utilities.layout {

  /* Border Radius */
  /* ---------------------------------------- */
  {{BORDER_RADIUS_UTILITIES}}

  /* Box Shadow */
  /* ---------------------------------------- */
  {{SHADOW_UTILITIES}}

  /* Width */
  /* ---------------------------------------- */
  {{WIDTH_UTILITIES}}

  /* Height */
  /* ---------------------------------------- */
  {{HEIGHT_UTILITIES}}
}

/* ============================================
   RESPONSIVE & STATE VARIANTS
   ============================================ */
@layer utilities.variants {

  /* Container Query Variants */
  /* ---------------------------------------- */
  {{CONTAINER_QUERY_VARIANTS}}

  /* Hover State Variants */
  /* ---------------------------------------- */
  {{HOVER_VARIANTS}}

  /* Focus State Variants */
  /* ---------------------------------------- */
  {{FOCUS_VARIANTS}}

  /* Active State Variants */
  /* ---------------------------------------- */
  {{ACTIVE_VARIANTS}}

  /* Dark Mode Variants */
  /* ---------------------------------------- */
  {{DARK_MODE_VARIANTS}}

  /* Reduced Motion Variants */
  /* ---------------------------------------- */
  {{REDUCED_MOTION_VARIANTS}}

  /* Forced Colors Variants (High Contrast) */
  /* ---------------------------------------- */
  {{FORCED_COLORS_VARIANTS}}
}
```

**Template Variables**: Each `{{VARIABLE_NAME}}` will be replaced by the generated utility CSS from the script.

---

### 3. Enhance Existing CSS Layers Template

**File**: `templates/css-layers.template.css`

**Changes**:
- Replace the hardcoded utilities section with dynamic generation
- Maintain backward compatibility
- Add documentation about auto-generated utilities

**Before** (current hardcoded utilities):
```css
@layer utilities {
  /* Text utilities */
  .text-primary { color: var(--color-text-primary); }
  .text-secondary { color: var(--color-text-secondary); }
  /* ... more hardcoded utilities ... */
}
```

**After** (dynamic generation):
```css
@layer utilities {
  /* ============================================
     AUTO-GENERATED UTILITIES
     These utilities are generated from design tokens
     ============================================ */
  {{GENERATED_UTILITIES}}

  /* ============================================
     CUSTOM PROJECT UTILITIES
     Add project-specific utilities below
     ============================================ */
  /* Add your custom utilities here */
}
```

---

### 4. Update Token Transformation Script

**File**: `scripts/transform_tokens.py`

**Changes**:
1. Import the new utility generator
2. Add new output format options
3. Support configuration for utility generation

**New Output Formats**:
- `'utilities'` - Standalone utilities.css file
- `'css-layers-full'` - Enhanced css-layers.css with generated utilities

**Updated Function**:
```python
def transform_tokens(
    input_path: str,
    output_format: str,
    output_path: str,
    config: dict = None
) -> None:
    """
    Transform W3C DTCG tokens to various formats.

    Supported formats:
    - 'css-variables': Simple CSS custom properties
    - 'css-layers': CSS with cascade layers (existing utilities)
    - 'css-layers-full': CSS with cascade layers + generated utilities
    - 'utilities': Standalone atomic utilities CSS
    - 'scss': SCSS variables
    - 'swift': iOS Swift code
    - 'kotlin': Android Kotlin code
    """
```

**Integration Logic**:
```python
if output_format == 'utilities':
    # Generate standalone utilities file
    generate_utilities(input_path, output_path, config)

elif output_format == 'css-layers-full':
    # Generate utilities and merge with css-layers template
    utilities_css = generate_utilities_string(input_path, config)
    template = load_template('css-layers.template.css')
    template = template.replace('{{GENERATED_UTILITIES}}', utilities_css)
    write_output(output_path, template)
```

---

### 5. Update Skill Documentation

**File**: `SKILL.md`

**Changes**:

1. **Update frontmatter version**:
```yaml
---
name: design-token-extractor
description: Extract design tokens from images and convert to CSS/SCSS/Swift/Kotlin with atomic utility class generation
version: 0.2.0
---
```

2. **Add utility generation section**:

```markdown
## Utility Class Generation

The skill now generates comprehensive atomic utility classes (Tailwind-style) from extracted design tokens.

### Generated Utilities

**Color Utilities:**
```css
/* Text colors */
.text-primary-500 { color: var(--color-primary-500); }
.text-neutral-900 { color: var(--color-neutral-900); }

/* Background colors */
.bg-surface-elevated { background-color: var(--color-surface-elevated); }
.bg-primary-500 { background-color: var(--color-primary-500); }

/* Border colors */
.border-accent-600 { border-color: var(--color-accent-600); }
```

**Spacing Utilities (with logical properties):**
```css
/* Padding */
.p-md { padding: var(--spacing-scale-md); }
.px-lg { padding-inline: var(--spacing-scale-lg); }
.py-sm { padding-block: var(--spacing-scale-sm); }
.pt-xs { padding-block-start: var(--spacing-scale-xs); }

/* Margin */
.m-md { margin: var(--spacing-scale-md); }
.mx-auto { margin-inline: auto; }
.my-lg { margin-block: var(--spacing-scale-lg); }

/* Gap */
.gap-md { gap: var(--spacing-scale-md); }
.gap-x-sm { column-gap: var(--spacing-scale-sm); }
```

**Typography Utilities:**
```css
.font-display { font-family: var(--font-family-display); }
.text-xl { font-size: var(--font-size-xl); }
.font-bold { font-weight: var(--font-weight-bold); }
.leading-tight { line-height: var(--line-height-tight); }
```

**Layout Utilities:**
```css
.rounded-md { border-radius: var(--border-radius-md); }
.rounded-full { border-radius: var(--border-radius-full); }
.shadow-elevated { box-shadow: var(--shadow-elevated); }
```

### Utility Variants

**Container Query Variants:**
```css
/* Apply utilities at specific container sizes */
@container (min-width: 768px) {
  .md\:text-xl { font-size: var(--font-size-xl); }
  .md\:p-lg { padding: var(--spacing-scale-lg); }
}
```

Usage:
```html
<div class="text-base md:text-xl">
  Responsive text that grows at medium container size
</div>
```

**State Variants:**
```css
/* Hover, focus, and active states */
.hover\:bg-primary-500:hover {
  background-color: var(--color-primary-500);
}

.focus\:outline-accent:focus {
  outline-color: var(--color-accent-500);
}

.active\:scale-95:active {
  transform: scale(0.95);
}
```

Usage:
```html
<button class="bg-primary-600 hover:bg-primary-700 active:scale-95">
  Interactive Button
</button>
```

**Dark Mode Variants:**
```css
@media (prefers-color-scheme: dark) {
  .dark\:bg-neutral-900 {
    background-color: var(--color-neutral-900);
  }
  .dark\:text-neutral-100 {
    color: var(--color-neutral-100);
  }
}
```

Usage:
```html
<div class="bg-white dark:bg-neutral-900 text-neutral-900 dark:text-neutral-100">
  Adapts to system dark mode preference
</div>
```

### Output Formats

**Standalone Utilities File:**
```
Output format: 'utilities'
Generates: utilities.css with all atomic utility classes
Use case: Import into any project for utility-first development
```

**Enhanced CSS Layers:**
```
Output format: 'css-layers-full'
Generates: Complete design system with tokens + components + utilities
Use case: Full design system implementation
```

### Configuration

Control which utilities are generated:

```python
config = {
    'categories': ['colors', 'spacing', 'typography', 'layout'],
    'variants': ['container', 'state', 'dark-mode'],
    'prefix': '',  # Optional: 'tw-', 'ds-', etc.
    'separator': ':'  # Variant separator
}
```

### Usage Examples

**Utility-First Layout:**
```html
<div class="p-lg bg-surface-elevated rounded-md shadow-md">
  <h1 class="font-display text-2xl font-bold text-primary-900 mb-md">
    Card Title
  </h1>
  <p class="text-base leading-relaxed text-neutral-700">
    Card content with proper spacing and typography.
  </p>
  <button class="mt-lg px-lg py-md bg-primary-600 hover:bg-primary-700
                 text-white rounded-sm font-semibold">
    Action Button
  </button>
</div>
```

**Responsive Grid:**
```html
<div class="grid gap-md md:gap-lg grid-cols-1 md:grid-cols-2 lg:grid-cols-3">
  <div class="p-md bg-white dark:bg-neutral-800">Item 1</div>
  <div class="p-md bg-white dark:bg-neutral-800">Item 2</div>
  <div class="p-md bg-white dark:bg-neutral-800">Item 3</div>
</div>
```
```

3. **Update workflow instructions**:
```markdown
## Updated Workflow

1. **Extract tokens from image**
   ```
   Ask Claude to analyze the image and extract design tokens
   ```

2. **Choose output format**
   - `utilities` - Standalone atomic utilities
   - `css-layers-full` - Complete design system with utilities
   - `css-variables` - Just CSS custom properties (no utilities)
   - `scss` - SCSS variables
   - Platform-specific: `swift`, `kotlin`

3. **Configure utility generation** (optional)
   - Specify which categories to generate
   - Choose which variants to include
   - Set custom prefix or separator

4. **Validate and refine**
   - Review generated utilities
   - Adjust token values if needed
   - Re-generate as necessary
```

---

## Expected Output Examples

### Example 1: Color Utilities

**Input Token (W3C JSON)**:
```json
{
  "color": {
    "primary": {
      "500": {
        "$type": "color",
        "$value": "#3b82f6",
        "$description": "Primary brand color"
      }
    }
  }
}
```

**Generated Utilities**:
```css
/* Text color */
.text-primary-500 {
  color: var(--color-primary-500);
}

/* Background color */
.bg-primary-500 {
  background-color: var(--color-primary-500);
}

/* Border color */
.border-primary-500 {
  border-color: var(--color-primary-500);
}

/* Hover variant */
.hover\:bg-primary-500:hover {
  background-color: var(--color-primary-500);
}

/* Dark mode variant */
@media (prefers-color-scheme: dark) {
  .dark\:text-primary-500 {
    color: var(--color-primary-500);
  }
}
```

### Example 2: Spacing Utilities with Logical Properties

**Input Token (W3C JSON)**:
```json
{
  "spacing": {
    "scale": {
      "md": {
        "$type": "dimension",
        "$value": "1rem",
        "$description": "Medium spacing"
      }
    }
  }
}
```

**Generated Utilities**:
```css
/* Padding - all sides */
.p-md {
  padding: var(--spacing-scale-md);
}

/* Padding - inline (horizontal) */
.px-md {
  padding-inline: var(--spacing-scale-md);
}

/* Padding - block (vertical) */
.py-md {
  padding-block: var(--spacing-scale-md);
}

/* Padding - individual sides (logical) */
.pt-md {
  padding-block-start: var(--spacing-scale-md);
}

.pr-md {
  padding-inline-end: var(--spacing-scale-md);
}

/* Margin - all sides */
.m-md {
  margin: var(--spacing-scale-md);
}

/* Container query variant */
@container (min-width: 768px) {
  .md\:p-md {
    padding: var(--spacing-scale-md);
  }
}
```

### Example 3: Typography Utilities

**Input Token (W3C JSON)**:
```json
{
  "font": {
    "size": {
      "xl": {
        "$type": "dimension",
        "$value": "1.25rem",
        "$description": "Extra large text"
      }
    },
    "weight": {
      "bold": {
        "$type": "number",
        "$value": 700,
        "$description": "Bold weight"
      }
    }
  }
}
```

**Generated Utilities**:
```css
/* Font size */
.text-xl {
  font-size: var(--font-size-xl);
}

/* Font weight */
.font-bold {
  font-weight: var(--font-weight-bold);
}

/* Container query variant */
@container (min-width: 1024px) {
  .lg\:text-xl {
    font-size: var(--font-size-xl);
  }
}

/* Hover variant (for interactive typography) */
.hover\:text-xl:hover {
  font-size: var(--font-size-xl);
}
```

---

## Technical Decisions & Rationale

### 1. Why Cascade Layers?

**Decision**: Organize utilities in cascade layers (`@layer utilities.colors`, etc.)

**Rationale**:
- Provides explicit specificity control without !important
- Allows utilities to override component styles predictably
- Makes it easy to add custom utilities that integrate properly
- Modern CSS feature with good browser support
- Follows W3C CSSWG recommendations

### 2. Why Logical Properties?

**Decision**: Use logical properties (`padding-inline`, `margin-block`) instead of directional (`padding-left`, `margin-top`)

**Rationale**:
- Supports internationalization (RTL languages) automatically
- More semantic and maintainable
- Future-proof approach recommended by W3C
- Aligns with modern CSS best practices
- Works with writing modes automatically

### 3. Why Container Queries Over Media Queries?

**Decision**: Use `@container` for responsive variants instead of `@media`

**Rationale**:
- More flexible - components respond to their container, not viewport
- Better for modular/reusable components
- Enables true component-driven design
- Modern CSS feature gaining wide adoption
- Can fallback to media queries if needed

### 4. Why Template Variables Over Direct Generation?

**Decision**: Use template files with `{{VARIABLE}}` placeholders instead of generating CSS directly in Python

**Rationale**:
- Separation of concerns - logic in Python, structure in CSS
- Easier to customize output format without changing code
- Templates are more readable and maintainable
- Non-developers can modify CSS structure
- Supports multiple output variations easily

### 5. Why Configuration Object?

**Decision**: Support optional configuration for customizing utility generation

**Rationale**:
- Flexibility - users can generate only what they need
- File size control - avoid generating unused utilities
- Framework compatibility - can match existing naming conventions
- Progressive adoption - can start with subset of utilities
- Team preferences - can customize to match coding standards

---

## File Size Considerations

### Challenge
Generating all utilities with all variants can create large CSS files.

**Example calculation**:
- 50 color tokens × 5 utility types (text, bg, border, fill, stroke) = 250 utilities
- 10 spacing tokens × 12 utility types (p, px, py, pt, pr, pb, pl, m, mx, my, mt, etc.) = 120 utilities
- Add 3 variant types (container, state, dark) × all utilities = ~1,110 additional variants
- **Total**: ~1,500+ CSS rules

### Mitigation Strategies

1. **Configuration-based generation**
   - Only generate requested categories
   - Only include needed variants
   - Selective token inclusion

2. **Modular output**
   - Separate files per category (colors.css, spacing.css, etc.)
   - Import only needed modules
   - Tree-shaking friendly structure

3. **PurgeCSS compatibility**
   - Predictable class naming for scanning
   - Documentation of all possible class patterns
   - Safelist patterns for dynamic classes

4. **Cascade layer optimization**
   - Layers can be selectively imported
   - Component-specific utility subsets
   - Critical CSS extraction support

5. **Future: Just-in-Time (JIT) generation**
   - Generate utilities on-demand during build
   - Only include classes actually used in HTML
   - Requires build tool integration (future enhancement)

---

## Accessibility Features

All generated utilities include automatic accessibility support:

### 1. Reduced Motion
```css
@media (prefers-reduced-motion: reduce) {
  .motion-safe\:animate-fade {
    animation: none;
  }
}
```

### 2. Forced Colors (High Contrast Mode)
```css
@media (forced-colors: active) {
  .forced-colors\:border-2 {
    border-width: 2px;
    border-color: CanvasText;
  }
}
```

### 3. Dark Mode
```css
@media (prefers-color-scheme: dark) {
  .dark\:bg-neutral-900 {
    background-color: var(--color-neutral-900);
  }
}
```

### 4. Focus Visible
```css
.focus-visible\:outline-accent:focus-visible {
  outline-color: var(--color-accent-500);
  outline-width: 2px;
  outline-offset: 2px;
}
```

---

## Browser Support

**Target**: Modern browsers with CSS custom properties support

- Chrome/Edge: 88+ (container queries)
- Firefox: 110+
- Safari: 16+

**Progressive Enhancement**:
- Base utilities work in all browsers with custom property support
- Container query variants gracefully degrade to mobile-first on older browsers
- Cascade layers polyfill available if needed
- Logical properties fallbacks can be added if supporting older browsers

---

## Testing Strategy

### 1. Unit Tests (Python)
- Test token parsing from W3C JSON
- Test utility generation for each category
- Test variant generation
- Test configuration options
- Test edge cases (missing tokens, invalid values)

### 2. Integration Tests
- Test full pipeline: image → tokens → utilities
- Test multiple output formats
- Test template variable replacement
- Test file I/O operations

### 3. Visual Tests
- Generate sample utilities CSS
- Create HTML test page using all utilities
- Visual regression testing for variants
- Cross-browser testing

### 4. Validation
- CSS validation (W3C CSS validator)
- Accessibility testing (axe-core)
- Performance testing (file size, parse time)
- Specificity verification (cascade layer ordering)

---

## Future Enhancements (Out of Scope for v0.2.0)

### 1. Just-in-Time (JIT) Generation
- Scan HTML/JSX files for used classes
- Generate only required utilities
- Build tool integration (webpack, vite, etc.)

### 2. Component Utilities
- Higher-level utilities for common patterns
- `.btn-primary`, `.card-elevated`, `.input-field`
- Generated from component token compositions

### 3. Animation Utilities
- Motion token support
- Transition utilities
- Animation keyframe generation

### 4. Grid/Layout Utilities
- Grid template utilities
- Flexbox utilities
- Display utilities

### 5. Interactive Configuration
- Web UI for configuring utility generation
- Real-time preview
- Export custom configurations

### 6. Framework Integrations
- Tailwind config export
- Bootstrap variable export
- Material Design token mapping

---

## Migration Guide

For existing users of the skill:

### Backward Compatibility
- All existing functionality remains unchanged
- Current templates still work as before
- No breaking changes to existing outputs

### Adopting New Features

**Option 1: Add utilities to existing setup**
```
1. Use 'css-layers-full' format instead of 'css-layers'
2. Existing components and tokens unchanged
3. New utilities available in HTML
```

**Option 2: Standalone utilities**
```
1. Generate 'utilities' format separately
2. Import utilities.css alongside existing styles
3. Gradually adopt utility classes
```

**Option 3: Full adoption**
```
1. Generate 'utilities' format
2. Refactor components to use utility classes
3. Reduce custom component CSS
4. Embrace utility-first approach
```

---

## Success Metrics

### Developer Experience
- Time to prototype new UI components
- Consistency of spacing/colors across designs
- Ease of responsive design implementation
- Learning curve for new team members

### Technical Metrics
- CSS file size (with/without purge)
- Number of custom CSS rules needed
- Build time impact
- Browser performance (parse time)

### Design System Metrics
- Token usage consistency
- Design-dev handoff efficiency
- Component reusability
- Accessibility compliance rate

---

## Questions & Decisions

### Open Questions
1. Should we support custom utility prefixes (e.g., `tw-`, `ds-`)? **Decision**: Yes, via config
2. Should we generate negative margin utilities? **Decision**: Yes, for layout flexibility
3. Should we include deprecated utility formats for migration? **Decision**: No, keep clean
4. Should container breakpoints be configurable? **Decision**: Yes, derived from spacing scale or custom

### Resolved Decisions
- ✅ Use Tailwind naming conventions (familiar to developers)
- ✅ Use logical properties (future-proof, i18n support)
- ✅ Use cascade layers (specificity control)
- ✅ Support full variant matrix (container, state, dark mode)
- ✅ Configuration-based generation (file size control)
- ✅ Template-based output (maintainability)

---

## Implementation Checklist

- [ ] Create `scripts/generate_utilities.py`
  - [ ] Token parsing logic
  - [ ] Color utility generation
  - [ ] Spacing utility generation (with logical properties)
  - [ ] Typography utility generation
  - [ ] Layout utility generation
  - [ ] Container query variant generation
  - [ ] State variant generation
  - [ ] Dark mode variant generation
  - [ ] Configuration support
  - [ ] Documentation/docstrings

- [ ] Create `templates/utilities.template.css`
  - [ ] Cascade layer structure
  - [ ] Template variables for all utility types
  - [ ] Documentation comments
  - [ ] Example usage comments

- [ ] Update `templates/css-layers.template.css`
  - [ ] Replace hardcoded utilities with template variable
  - [ ] Add documentation about generated utilities
  - [ ] Maintain backward compatibility

- [ ] Update `scripts/transform_tokens.py`
  - [ ] Import utility generator
  - [ ] Add 'utilities' output format
  - [ ] Add 'css-layers-full' output format
  - [ ] Configuration parameter support
  - [ ] Error handling

- [ ] Update `SKILL.md`
  - [ ] Update version to 0.2.0
  - [ ] Add utility generation section
  - [ ] Document all utility types
  - [ ] Document variants
  - [ ] Add usage examples
  - [ ] Update workflow instructions
  - [ ] Add configuration documentation

- [ ] Testing
  - [ ] Create test tokens JSON
  - [ ] Test utility generation
  - [ ] Test variant generation
  - [ ] Visual test HTML page
  - [ ] Cross-browser testing
  - [ ] File size analysis

- [ ] Documentation
  - [ ] README updates
  - [ ] Code comments
  - [ ] Example output files
  - [ ] Migration guide
  - [ ] Troubleshooting guide

---

## Timeline Estimate

**Note**: This is an implementation complexity estimate, not a calendar timeline.

- **Script development**: 6-8 hours
  - Token parsing and utility generation logic
  - Variant generation
  - Configuration handling

- **Template creation**: 2-3 hours
  - utilities.template.css structure
  - css-layers.template.css updates

- **Integration**: 2-3 hours
  - Update transform_tokens.py
  - Hook up all pieces

- **Documentation**: 3-4 hours
  - SKILL.md updates
  - Code documentation
  - Examples

- **Testing**: 4-5 hours
  - Unit tests
  - Visual testing
  - Cross-browser verification
  - Edge case testing

**Total Development Effort**: ~17-23 hours

---

## Conclusion

This enhancement transforms the design-token-extractor from a token extraction tool into a comprehensive utility-first design system generator. By adding Tailwind-style atomic utilities with full variant support, designers and developers can rapidly prototype and build consistent UIs directly from design tokens.

The implementation maintains backward compatibility while adding powerful new capabilities through a flexible, configuration-driven approach. Modern CSS features (cascade layers, logical properties, container queries) ensure the output is future-proof and accessible.

The modular architecture allows for incremental adoption - teams can start with standalone utilities or fully integrate into their existing design system. File size concerns are addressed through configuration options and future JIT generation support.

This positions the skill as a complete solution for design token management and utility-first development workflows.
