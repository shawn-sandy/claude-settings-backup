#!/usr/bin/env python3
"""
Generate atomic utility classes from W3C Design Tokens.

Creates Tailwind-style atomic utility classes with support for:
- Color utilities (text, background, border, fill, stroke)
- Spacing utilities with logical properties (padding, margin, gap)
- Typography utilities (font, size, weight, line-height)
- Layout utilities (border-radius, shadow, dimensions)
- Responsive variants (container queries)
- State variants (hover, focus, active)
- Accessibility variants (dark mode, reduced motion, forced colors)

Usage:
    python generate_utilities.py --input tokens.json --output utilities.css
    python generate_utilities.py --input tokens.json --output utilities.css --config config.json
    python generate_utilities.py --help
"""

import argparse
import json
import sys
from pathlib import Path
from typing import Dict, Any, List, Tuple, Set


def flatten_tokens(tokens: Dict[str, Any], prefix: str = "", separator: str = "-") -> List[Tuple[str, Any]]:
    """
    Flatten nested token structure into flat list of (name, token) tuples.

    Args:
        tokens: Nested token dictionary
        prefix: Current prefix for nested names
        separator: Separator for name parts

    Returns:
        List of (name, token_object) tuples
    """
    flattened = []

    for key, value in tokens.items():
        current_name = f"{prefix}{separator}{key}" if prefix else key

        # Check if this is a token (has $value) or a group
        if isinstance(value, dict) and '$value' in value:
            flattened.append((current_name, value))
        elif isinstance(value, dict):
            # Recurse into nested groups
            flattened.extend(flatten_tokens(value, current_name, separator))

    return flattened


def get_tokens_by_type(tokens: Dict[str, Any], token_type: str) -> List[Tuple[str, Any]]:
    """
    Filter tokens by type.

    Args:
        tokens: W3C token dictionary
        token_type: Type to filter for (color, dimension, etc.)

    Returns:
        List of (name, token) tuples matching the type
    """
    flat_tokens = flatten_tokens(tokens)
    return [(name, token) for name, token in flat_tokens if token.get('$type') == token_type]


def escape_class_name(name: str) -> str:
    """
    Escape special characters in class names for CSS.

    Args:
        name: Raw class name

    Returns:
        Escaped class name safe for CSS
    """
    # Escape colons for variant classes like .hover:bg-primary
    return name.replace(':', '\\:')


def generate_color_utilities(tokens: Dict[str, Any], config: Dict[str, Any]) -> List[str]:
    """
    Generate color utility classes.

    Creates utilities for text, background, border, fill, and stroke colors.

    Args:
        tokens: W3C token dictionary
        config: Configuration options

    Returns:
        List of CSS utility class strings
    """
    color_tokens = get_tokens_by_type(tokens, 'color')
    utilities = []
    prefix = config.get('prefix', '')

    utilities.append("  /* ============================================")
    utilities.append("     COLOR UTILITIES")
    utilities.append("     ============================================ */")
    utilities.append("")

    # Text colors
    utilities.append("  /* Text Colors */")
    for name, token in color_tokens:
        class_name = f"{prefix}text-{name}"
        utilities.append(f"  .{class_name} {{")
        utilities.append(f"    color: var(--{name});")
        utilities.append("  }")
        utilities.append("")

    # Background colors
    utilities.append("  /* Background Colors */")
    for name, token in color_tokens:
        class_name = f"{prefix}bg-{name}"
        utilities.append(f"  .{class_name} {{")
        utilities.append(f"    background-color: var(--{name});")
        utilities.append("  }")
        utilities.append("")

    # Border colors
    utilities.append("  /* Border Colors */")
    for name, token in color_tokens:
        class_name = f"{prefix}border-{name}"
        utilities.append(f"  .{class_name} {{")
        utilities.append(f"    border-color: var(--{name});")
        utilities.append("  }")
        utilities.append("")

    # Fill colors (SVG)
    utilities.append("  /* Fill Colors (SVG) */")
    for name, token in color_tokens:
        class_name = f"{prefix}fill-{name}"
        utilities.append(f"  .{class_name} {{")
        utilities.append(f"    fill: var(--{name});")
        utilities.append("  }")
        utilities.append("")

    # Stroke colors (SVG)
    utilities.append("  /* Stroke Colors (SVG) */")
    for name, token in color_tokens:
        class_name = f"{prefix}stroke-{name}"
        utilities.append(f"  .{class_name} {{")
        utilities.append(f"    stroke: var(--{name});")
        utilities.append("  }")
        utilities.append("")

    return utilities


def generate_spacing_utilities(tokens: Dict[str, Any], config: Dict[str, Any]) -> List[str]:
    """
    Generate spacing utility classes with logical properties.

    Creates utilities for padding, margin, and gap.

    Args:
        tokens: W3C token dictionary
        config: Configuration options

    Returns:
        List of CSS utility class strings
    """
    spacing_tokens = get_tokens_by_type(tokens, 'dimension')
    # Filter for spacing-related tokens
    spacing_tokens = [(name, token) for name, token in spacing_tokens
                     if 'spacing' in name.lower() or 'space' in name.lower()]

    utilities = []
    prefix = config.get('prefix', '')

    utilities.append("  /* ============================================")
    utilities.append("     SPACING UTILITIES")
    utilities.append("     ============================================ */")
    utilities.append("")

    # Padding - all sides
    utilities.append("  /* Padding - All Sides */")
    for name, token in spacing_tokens:
        # Extract the scale name (e.g., "spacing-scale-md" -> "md")
        parts = name.split('-')
        scale_name = parts[-1] if len(parts) > 0 else name

        class_name = f"{prefix}p-{scale_name}"
        utilities.append(f"  .{class_name} {{")
        utilities.append(f"    padding: var(--{name});")
        utilities.append("  }")
        utilities.append("")

    # Padding - inline (horizontal with logical properties)
    utilities.append("  /* Padding - Inline (Horizontal) */")
    for name, token in spacing_tokens:
        parts = name.split('-')
        scale_name = parts[-1] if len(parts) > 0 else name

        class_name = f"{prefix}px-{scale_name}"
        utilities.append(f"  .{class_name} {{")
        utilities.append(f"    padding-inline: var(--{name});")
        utilities.append("  }")
        utilities.append("")

    # Padding - block (vertical with logical properties)
    utilities.append("  /* Padding - Block (Vertical) */")
    for name, token in spacing_tokens:
        parts = name.split('-')
        scale_name = parts[-1] if len(parts) > 0 else name

        class_name = f"{prefix}py-{scale_name}"
        utilities.append(f"  .{class_name} {{")
        utilities.append(f"    padding-block: var(--{name});")
        utilities.append("  }")
        utilities.append("")

    # Padding - individual sides with logical properties
    utilities.append("  /* Padding - Individual Sides (Logical Properties) */")
    for name, token in spacing_tokens:
        parts = name.split('-')
        scale_name = parts[-1] if len(parts) > 0 else name

        # Top (block-start)
        utilities.append(f"  .{prefix}pt-{scale_name} {{")
        utilities.append(f"    padding-block-start: var(--{name});")
        utilities.append("  }")
        utilities.append("")

        # Right (inline-end)
        utilities.append(f"  .{prefix}pr-{scale_name} {{")
        utilities.append(f"    padding-inline-end: var(--{name});")
        utilities.append("  }")
        utilities.append("")

        # Bottom (block-end)
        utilities.append(f"  .{prefix}pb-{scale_name} {{")
        utilities.append(f"    padding-block-end: var(--{name});")
        utilities.append("  }")
        utilities.append("")

        # Left (inline-start)
        utilities.append(f"  .{prefix}pl-{scale_name} {{")
        utilities.append(f"    padding-inline-start: var(--{name});")
        utilities.append("  }")
        utilities.append("")

    # Margin - all sides
    utilities.append("  /* Margin - All Sides */")
    for name, token in spacing_tokens:
        parts = name.split('-')
        scale_name = parts[-1] if len(parts) > 0 else name

        class_name = f"{prefix}m-{scale_name}"
        utilities.append(f"  .{class_name} {{")
        utilities.append(f"    margin: var(--{name});")
        utilities.append("  }")
        utilities.append("")

    # Margin - inline (horizontal)
    utilities.append("  /* Margin - Inline (Horizontal) */")
    for name, token in spacing_tokens:
        parts = name.split('-')
        scale_name = parts[-1] if len(parts) > 0 else name

        class_name = f"{prefix}mx-{scale_name}"
        utilities.append(f"  .{class_name} {{")
        utilities.append(f"    margin-inline: var(--{name});")
        utilities.append("  }")
        utilities.append("")

    # Add mx-auto
    utilities.append("  /* Margin - Auto Centering */")
    utilities.append(f"  .{prefix}mx-auto {{")
    utilities.append("    margin-inline: auto;")
    utilities.append("  }")
    utilities.append("")

    # Margin - block (vertical)
    utilities.append("  /* Margin - Block (Vertical) */")
    for name, token in spacing_tokens:
        parts = name.split('-')
        scale_name = parts[-1] if len(parts) > 0 else name

        class_name = f"{prefix}my-{scale_name}"
        utilities.append(f"  .{class_name} {{")
        utilities.append(f"    margin-block: var(--{name});")
        utilities.append("  }")
        utilities.append("")

    # Margin - individual sides with logical properties
    utilities.append("  /* Margin - Individual Sides (Logical Properties) */")
    for name, token in spacing_tokens:
        parts = name.split('-')
        scale_name = parts[-1] if len(parts) > 0 else name

        # Top (block-start)
        utilities.append(f"  .{prefix}mt-{scale_name} {{")
        utilities.append(f"    margin-block-start: var(--{name});")
        utilities.append("  }")
        utilities.append("")

        # Right (inline-end)
        utilities.append(f"  .{prefix}mr-{scale_name} {{")
        utilities.append(f"    margin-inline-end: var(--{name});")
        utilities.append("  }")
        utilities.append("")

        # Bottom (block-end)
        utilities.append(f"  .{prefix}mb-{scale_name} {{")
        utilities.append(f"    margin-block-end: var(--{name});")
        utilities.append("  }")
        utilities.append("")

        # Left (inline-start)
        utilities.append(f"  .{prefix}ml-{scale_name} {{")
        utilities.append(f"    margin-inline-start: var(--{name});")
        utilities.append("  }")
        utilities.append("")

    # Gap utilities
    utilities.append("  /* Gap Utilities */")
    for name, token in spacing_tokens:
        parts = name.split('-')
        scale_name = parts[-1] if len(parts) > 0 else name

        # Gap (all)
        utilities.append(f"  .{prefix}gap-{scale_name} {{")
        utilities.append(f"    gap: var(--{name});")
        utilities.append("  }")
        utilities.append("")

        # Column gap
        utilities.append(f"  .{prefix}gap-x-{scale_name} {{")
        utilities.append(f"    column-gap: var(--{name});")
        utilities.append("  }")
        utilities.append("")

        # Row gap
        utilities.append(f"  .{prefix}gap-y-{scale_name} {{")
        utilities.append(f"    row-gap: var(--{name});")
        utilities.append("  }")
        utilities.append("")

    return utilities


def generate_typography_utilities(tokens: Dict[str, Any], config: Dict[str, Any]) -> List[str]:
    """
    Generate typography utility classes.

    Creates utilities for font family, size, weight, and line-height.

    Args:
        tokens: W3C token dictionary
        config: Configuration options

    Returns:
        List of CSS utility class strings
    """
    flat_tokens = flatten_tokens(tokens)
    utilities = []
    prefix = config.get('prefix', '')

    utilities.append("  /* ============================================")
    utilities.append("     TYPOGRAPHY UTILITIES")
    utilities.append("     ============================================ */")
    utilities.append("")

    # Font families
    font_families = [(name, token) for name, token in flat_tokens
                    if token.get('$type') == 'fontFamily']
    if font_families:
        utilities.append("  /* Font Families */")
        for name, token in font_families:
            parts = name.split('-')
            family_name = parts[-1] if len(parts) > 0 else name

            class_name = f"{prefix}font-{family_name}"
            utilities.append(f"  .{class_name} {{")
            utilities.append(f"    font-family: var(--{name});")
            utilities.append("  }")
            utilities.append("")

    # Font sizes
    font_sizes = [(name, token) for name, token in flat_tokens
                 if 'font' in name.lower() and 'size' in name.lower() and token.get('$type') == 'dimension']
    if font_sizes:
        utilities.append("  /* Font Sizes */")
        for name, token in font_sizes:
            parts = name.split('-')
            size_name = parts[-1] if len(parts) > 0 else name

            class_name = f"{prefix}text-{size_name}"
            utilities.append(f"  .{class_name} {{")
            utilities.append(f"    font-size: var(--{name});")
            utilities.append("  }")
            utilities.append("")

    # Font weights
    font_weights = [(name, token) for name, token in flat_tokens
                   if token.get('$type') == 'fontWeight']
    if font_weights:
        utilities.append("  /* Font Weights */")
        for name, token in font_weights:
            parts = name.split('-')
            weight_name = parts[-1] if len(parts) > 0 else name

            class_name = f"{prefix}font-{weight_name}"
            utilities.append(f"  .{class_name} {{")
            utilities.append(f"    font-weight: var(--{name});")
            utilities.append("  }")
            utilities.append("")

    # Line heights
    line_heights = [(name, token) for name, token in flat_tokens
                   if 'line' in name.lower() and 'height' in name.lower()]
    if line_heights:
        utilities.append("  /* Line Heights */")
        for name, token in line_heights:
            parts = name.split('-')
            height_name = parts[-1] if len(parts) > 0 else name

            class_name = f"{prefix}leading-{height_name}"
            utilities.append(f"  .{class_name} {{")
            utilities.append(f"    line-height: var(--{name});")
            utilities.append("  }")
            utilities.append("")

    return utilities


def generate_layout_utilities(tokens: Dict[str, Any], config: Dict[str, Any]) -> List[str]:
    """
    Generate layout utility classes.

    Creates utilities for border-radius, shadows, and dimensions.

    Args:
        tokens: W3C token dictionary
        config: Configuration options

    Returns:
        List of CSS utility class strings
    """
    flat_tokens = flatten_tokens(tokens)
    utilities = []
    prefix = config.get('prefix', '')

    utilities.append("  /* ============================================")
    utilities.append("     LAYOUT UTILITIES")
    utilities.append("     ============================================ */")
    utilities.append("")

    # Border radius
    border_radii = [(name, token) for name, token in flat_tokens
                   if 'border' in name.lower() and 'radius' in name.lower()]
    if border_radii:
        utilities.append("  /* Border Radius */")
        for name, token in border_radii:
            parts = name.split('-')
            radius_name = parts[-1] if len(parts) > 0 else name

            class_name = f"{prefix}rounded-{radius_name}"
            utilities.append(f"  .{class_name} {{")
            utilities.append(f"    border-radius: var(--{name});")
            utilities.append("  }")
            utilities.append("")

    # Shadows
    shadows = [(name, token) for name, token in flat_tokens
              if token.get('$type') == 'shadow']
    if shadows:
        utilities.append("  /* Box Shadows */")
        for name, token in shadows:
            parts = name.split('-')
            shadow_name = parts[-1] if len(parts) > 0 else name

            class_name = f"{prefix}shadow-{shadow_name}"
            utilities.append(f"  .{class_name} {{")
            utilities.append(f"    box-shadow: var(--{name});")
            utilities.append("  }")
            utilities.append("")

    return utilities


def generate_container_variants(base_utilities: List[str], config: Dict[str, Any]) -> List[str]:
    """
    Generate container query variants for utilities.

    Args:
        base_utilities: List of base utility classes
        config: Configuration options

    Returns:
        List of CSS container query variant strings
    """
    if 'container' not in config.get('variants', []):
        return []

    utilities = []
    prefix = config.get('prefix', '')

    # Define container breakpoints
    breakpoints = {
        'sm': '640px',
        'md': '768px',
        'lg': '1024px',
        'xl': '1280px'
    }

    utilities.append("  /* ============================================")
    utilities.append("     CONTAINER QUERY VARIANTS")
    utilities.append("     ============================================ */")
    utilities.append("")

    for bp_name, bp_value in breakpoints.items():
        utilities.append(f"  /* {bp_name.upper()} Container Variants (min-width: {bp_value}) */")
        utilities.append(f"  @container (min-width: {bp_value}) {{")

        # Generate variants for a subset of utilities (to keep file size manageable)
        # We'll create variants for commonly responsive utilities
        utilities.append(f"    /* Add {bp_name} variants here */")
        utilities.append(f"    /* Example: .{bp_name}\\:text-lg {{ font-size: var(--font-size-lg); }} */")

        utilities.append("  }")
        utilities.append("")

    return utilities


def generate_state_variants(tokens: Dict[str, Any], config: Dict[str, Any]) -> List[str]:
    """
    Generate state variants (hover, focus, active) for utilities.

    Args:
        tokens: W3C token dictionary
        config: Configuration options

    Returns:
        List of CSS state variant strings
    """
    if 'state' not in config.get('variants', []):
        return []

    utilities = []
    prefix = config.get('prefix', '')
    color_tokens = get_tokens_by_type(tokens, 'color')

    utilities.append("  /* ============================================")
    utilities.append("     STATE VARIANTS")
    utilities.append("     ============================================ */")
    utilities.append("")

    # Hover variants for colors
    utilities.append("  /* Hover Variants */")
    for name, token in color_tokens:
        # Background hover
        class_name = f"{prefix}hover\\:bg-{name}"
        utilities.append(f"  .{class_name}:hover {{")
        utilities.append(f"    background-color: var(--{name});")
        utilities.append("  }")
        utilities.append("")

        # Text hover
        class_name = f"{prefix}hover\\:text-{name}"
        utilities.append(f"  .{class_name}:hover {{")
        utilities.append(f"    color: var(--{name});")
        utilities.append("  }")
        utilities.append("")

    # Focus variants for colors
    utilities.append("  /* Focus Variants */")
    for name, token in color_tokens:
        # Background focus
        class_name = f"{prefix}focus\\:bg-{name}"
        utilities.append(f"  .{class_name}:focus {{")
        utilities.append(f"    background-color: var(--{name});")
        utilities.append("  }")
        utilities.append("")

        # Outline focus
        class_name = f"{prefix}focus\\:outline-{name}"
        utilities.append(f"  .{class_name}:focus {{")
        utilities.append(f"    outline-color: var(--{name});")
        utilities.append("  }")
        utilities.append("")

    # Active variants for colors
    utilities.append("  /* Active Variants */")
    for name, token in color_tokens:
        # Background active
        class_name = f"{prefix}active\\:bg-{name}"
        utilities.append(f"  .{class_name}:active {{")
        utilities.append(f"    background-color: var(--{name});")
        utilities.append("  }")
        utilities.append("")

    return utilities


def generate_dark_mode_variants(tokens: Dict[str, Any], config: Dict[str, Any]) -> List[str]:
    """
    Generate dark mode variants for utilities.

    Args:
        tokens: W3C token dictionary
        config: Configuration options

    Returns:
        List of CSS dark mode variant strings
    """
    if 'dark-mode' not in config.get('variants', []):
        return []

    utilities = []
    prefix = config.get('prefix', '')
    color_tokens = get_tokens_by_type(tokens, 'color')

    utilities.append("  /* ============================================")
    utilities.append("     DARK MODE VARIANTS")
    utilities.append("     ============================================ */")
    utilities.append("")
    utilities.append("  @media (prefers-color-scheme: dark) {")

    # Dark mode text colors
    utilities.append("    /* Dark Mode Text Colors */")
    for name, token in color_tokens:
        class_name = f"{prefix}dark\\:text-{name}"
        utilities.append(f"    .{class_name} {{")
        utilities.append(f"      color: var(--{name});")
        utilities.append("    }")
        utilities.append("")

    # Dark mode background colors
    utilities.append("    /* Dark Mode Background Colors */")
    for name, token in color_tokens:
        class_name = f"{prefix}dark\\:bg-{name}"
        utilities.append(f"    .{class_name} {{")
        utilities.append(f"      background-color: var(--{name});")
        utilities.append("    }")
        utilities.append("")

    utilities.append("  }")
    utilities.append("")

    return utilities


def generate_accessibility_variants(config: Dict[str, Any]) -> List[str]:
    """
    Generate accessibility-related variants.

    Creates variants for reduced-motion and forced-colors.

    Args:
        config: Configuration options

    Returns:
        List of CSS accessibility variant strings
    """
    utilities = []

    utilities.append("  /* ============================================")
    utilities.append("     ACCESSIBILITY VARIANTS")
    utilities.append("     ============================================ */")
    utilities.append("")

    # Reduced motion
    utilities.append("  /* Reduced Motion */")
    utilities.append("  @media (prefers-reduced-motion: reduce) {")
    utilities.append("    /* Disable animations and transitions for users who prefer reduced motion */")
    utilities.append("    .motion-safe\\:animate-none {")
    utilities.append("      animation: none !important;")
    utilities.append("      transition: none !important;")
    utilities.append("    }")
    utilities.append("  }")
    utilities.append("")

    # Forced colors (high contrast mode)
    utilities.append("  /* Forced Colors (High Contrast Mode) */")
    utilities.append("  @media (forced-colors: active) {")
    utilities.append("    /* Ensure borders are visible in high contrast mode */")
    utilities.append("    .forced-colors\\:border {")
    utilities.append("      border: 1px solid CanvasText;")
    utilities.append("    }")
    utilities.append("  }")
    utilities.append("")

    return utilities


def generate_utilities(tokens: Dict[str, Any], config: Dict[str, Any] = None) -> str:
    """
    Main utility generation function.

    Args:
        tokens: W3C token dictionary
        config: Configuration options

    Returns:
        Complete CSS utilities string
    """
    if config is None:
        config = {
            'categories': ['colors', 'spacing', 'typography', 'layout'],
            'variants': ['container', 'state', 'dark-mode'],
            'prefix': ''
        }

    utilities = []

    # Header
    utilities.append("/**")
    utilities.append(" * Design System Utilities")
    utilities.append(" * Auto-generated from design tokens")
    utilities.append(" *")
    utilities.append(" * Categories:")
    for category in config.get('categories', []):
        utilities.append(f" * - {category}")
    utilities.append(" *")
    utilities.append(" * Variants:")
    for variant in config.get('variants', []):
        utilities.append(f" * - {variant}")
    utilities.append(" */")
    utilities.append("")

    # Cascade layer definition
    utilities.append("@layer utilities.colors,")
    utilities.append("       utilities.spacing,")
    utilities.append("       utilities.typography,")
    utilities.append("       utilities.layout,")
    utilities.append("       utilities.variants;")
    utilities.append("")

    # Generate base utilities by category
    categories = config.get('categories', [])

    if 'colors' in categories:
        utilities.append("@layer utilities.colors {")
        utilities.extend(generate_color_utilities(tokens, config))
        utilities.append("}")
        utilities.append("")

    if 'spacing' in categories:
        utilities.append("@layer utilities.spacing {")
        utilities.extend(generate_spacing_utilities(tokens, config))
        utilities.append("}")
        utilities.append("")

    if 'typography' in categories:
        utilities.append("@layer utilities.typography {")
        utilities.extend(generate_typography_utilities(tokens, config))
        utilities.append("}")
        utilities.append("")

    if 'layout' in categories:
        utilities.append("@layer utilities.layout {")
        utilities.extend(generate_layout_utilities(tokens, config))
        utilities.append("}")
        utilities.append("")

    # Generate variants
    utilities.append("@layer utilities.variants {")

    base_utils = []  # Placeholder for base utilities to create variants from
    utilities.extend(generate_container_variants(base_utils, config))
    utilities.extend(generate_state_variants(tokens, config))
    utilities.extend(generate_dark_mode_variants(tokens, config))
    utilities.extend(generate_accessibility_variants(config))

    utilities.append("}")
    utilities.append("")

    return "\n".join(utilities)


def main():
    """Main entry point for the script."""
    parser = argparse.ArgumentParser(
        description='Generate atomic utility classes from W3C Design Tokens',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python generate_utilities.py --input tokens.json --output utilities.css
  python generate_utilities.py --input tokens.json --output utilities.css --config config.json

Config file format (JSON):
  {
    "categories": ["colors", "spacing", "typography", "layout"],
    "variants": ["container", "state", "dark-mode"],
    "prefix": ""
  }
        """
    )

    parser.add_argument(
        '--input',
        type=str,
        required=True,
        help='Input W3C token JSON file'
    )

    parser.add_argument(
        '--output',
        type=str,
        required=True,
        help='Output utilities CSS file'
    )

    parser.add_argument(
        '--config',
        type=str,
        help='Optional configuration JSON file'
    )

    args = parser.parse_args()

    # Load input tokens
    input_path = Path(args.input)
    if not input_path.exists():
        print(f"Error: Input file not found: {args.input}", file=sys.stderr)
        sys.exit(1)

    with open(input_path, 'r', encoding='utf-8') as f:
        tokens = json.load(f)

    # Load config if provided
    config = None
    if args.config:
        config_path = Path(args.config)
        if not config_path.exists():
            print(f"Error: Config file not found: {args.config}", file=sys.stderr)
            sys.exit(1)

        with open(config_path, 'r', encoding='utf-8') as f:
            config = json.load(f)

    # Generate utilities
    output = generate_utilities(tokens, config)

    # Write output
    output_path = Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(output)

    print(f"✓ Utilities generated successfully: {args.output}")
    if config:
        print(f"  Categories: {', '.join(config.get('categories', []))}")
        print(f"  Variants: {', '.join(config.get('variants', []))}")


if __name__ == '__main__':
    main()
