#!/usr/bin/env python3
"""
Transform W3C Design Tokens to various output formats.

Converts W3C DTCG JSON tokens to CSS custom properties, SCSS variables,
iOS Swift, Android Kotlin, atomic utilities, and other platform-specific formats.

Usage:
    python transform_tokens.py --input tokens.json --format css --output tokens.css
    python transform_tokens.py --input tokens.json --format scss --output tokens.scss
    python transform_tokens.py --input tokens.json --format swift --output Tokens.swift
    python transform_tokens.py --input tokens.json --format utilities --output utilities.css
    python transform_tokens.py --help
"""

import argparse
import json
import sys
from pathlib import Path
from typing import Dict, Any, List, Tuple

# Import utility generator
try:
    from generate_utilities import generate_utilities
except ImportError:
    # If running from different directory, try importing from same directory
    import sys
    sys.path.append(str(Path(__file__).parent))
    from generate_utilities import generate_utilities


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


def to_css_custom_properties(tokens: Dict[str, Any]) -> str:
    """
    Transform tokens to CSS custom properties.

    Args:
        tokens: W3C token dictionary

    Returns:
        CSS string with custom properties
    """
    flat_tokens = flatten_tokens(tokens)

    css_lines = [":root {"]

    for name, token in flat_tokens:
        value = token['$value']
        description = token.get('$description', '')

        # Add comment if description exists
        if description:
            css_lines.append(f"  /* {description} */")

        css_lines.append(f"  --{name}: {value};")

    css_lines.append("}")

    return "\n".join(css_lines)


def to_css_with_layers(tokens: Dict[str, Any]) -> str:
    """
    Transform tokens to CSS with cascade layers.

    Args:
        tokens: W3C token dictionary

    Returns:
        CSS string with @layer organization
    """
    flat_tokens = flatten_tokens(tokens)

    css_lines = [
        "@layer reset, tokens, components, utilities;",
        "",
        "@layer tokens {",
        "  :root {"
    ]

    for name, token in flat_tokens:
        value = token['$value']
        description = token.get('$description', '')

        if description:
            css_lines.append(f"    /* {description} */")

        css_lines.append(f"    --{name}: {value};")

    css_lines.extend([
        "  }",
        "}"
    ])

    return "\n".join(css_lines)


def to_scss_variables(tokens: Dict[str, Any]) -> str:
    """
    Transform tokens to SCSS variables.

    Args:
        tokens: W3C token dictionary

    Returns:
        SCSS string with variables
    """
    flat_tokens = flatten_tokens(tokens)

    scss_lines = []

    for name, token in flat_tokens:
        value = token['$value']
        description = token.get('$description', '')

        if description:
            scss_lines.append(f"// {description}")

        # Convert kebab-case to SCSS variable
        scss_lines.append(f"${name}: {value};")

    return "\n".join(scss_lines)


def to_swift(tokens: Dict[str, Any]) -> str:
    """
    Transform tokens to iOS Swift code.

    Args:
        tokens: W3C token dictionary

    Returns:
        Swift struct definition
    """
    flat_tokens = flatten_tokens(tokens, separator="_")

    swift_lines = [
        "import UIKit",
        "",
        "/// Design tokens generated from W3C DTCG specification",
        "struct DesignTokens {"
    ]

    for name, token in flat_tokens:
        value = token['$value']
        token_type = token.get('$type', '')
        description = token.get('$description', '')

        # Convert to Swift naming (camelCase)
        swift_name = ''.join(word.capitalize() for word in name.split('_'))
        swift_name = swift_name[0].lower() + swift_name[1:]

        if description:
            swift_lines.append(f"  /// {description}")

        if token_type == 'color':
            # Convert hex to UIColor
            swift_lines.append(f'  static let {swift_name} = UIColor(hex: "{value}")')
        elif token_type == 'dimension':
            # Convert to CGFloat
            unit_value = value.replace('rem', '').replace('px', '').replace('em', '')
            try:
                float_val = float(unit_value) * 16  # Assume 1rem = 16px
                swift_lines.append(f"  static let {swift_name}: CGFloat = {float_val}")
            except ValueError:
                swift_lines.append(f'  static let {swift_name} = "{value}"')
        else:
            swift_lines.append(f'  static let {swift_name} = "{value}"')

    swift_lines.append("}")

    return "\n".join(swift_lines)


def to_kotlin(tokens: Dict[str, Any]) -> str:
    """
    Transform tokens to Android Kotlin code.

    Args:
        tokens: W3C token dictionary

    Returns:
        Kotlin object definition
    """
    flat_tokens = flatten_tokens(tokens, separator="_")

    kotlin_lines = [
        "import androidx.compose.ui.graphics.Color",
        "import androidx.compose.ui.unit.dp",
        "",
        "/** Design tokens generated from W3C DTCG specification */",
        "object DesignTokens {"
    ]

    for name, token in flat_tokens:
        value = token['$value']
        token_type = token.get('$type', '')
        description = token.get('$description', '')

        # Convert to Kotlin naming (camelCase)
        kotlin_name = ''.join(word.capitalize() for word in name.split('_'))
        kotlin_name = kotlin_name[0].lower() + kotlin_name[1:]

        if description:
            kotlin_lines.append(f"  /** {description} */")

        if token_type == 'color':
            # Convert hex to Compose Color
            hex_value = value.replace('#', '0xFF')
            kotlin_lines.append(f"  val {kotlin_name} = Color({hex_value})")
        elif token_type == 'dimension':
            # Convert to dp
            unit_value = value.replace('rem', '').replace('px', '').replace('em', '')
            try:
                float_val = float(unit_value) * 16  # Assume 1rem = 16px
                kotlin_lines.append(f"  val {kotlin_name} = {float_val}.dp")
            except ValueError:
                kotlin_lines.append(f'  val {kotlin_name} = "{value}"')
        else:
            kotlin_lines.append(f'  val {kotlin_name} = "{value}"')

    kotlin_lines.append("}")

    return "\n".join(kotlin_lines)


def to_utilities(tokens: Dict[str, Any], config: Dict[str, Any] = None) -> str:
    """
    Transform tokens to atomic utility classes.

    Args:
        tokens: W3C token dictionary
        config: Optional configuration for utility generation

    Returns:
        CSS string with atomic utilities
    """
    return generate_utilities(tokens, config)


def to_css_layers_with_utilities(tokens: Dict[str, Any], template_path: Path = None) -> str:
    """
    Transform tokens to CSS with cascade layers including generated utilities.

    Args:
        tokens: W3C token dictionary
        template_path: Optional path to css-layers template

    Returns:
        CSS string with layers and utilities
    """
    # Generate utilities
    config = {
        'categories': ['colors', 'spacing', 'typography', 'layout'],
        'variants': ['container', 'state', 'dark-mode'],
        'prefix': ''
    }
    utilities_css = generate_utilities(tokens, config)

    # Load template
    if template_path is None:
        template_path = Path(__file__).parent.parent / 'templates' / 'css-layers.template.css'

    if not template_path.exists():
        # Fallback: generate basic CSS with layers
        base_css = to_css_with_layers(tokens)
        return f"{base_css}\n\n/* Generated Utilities */\n{utilities_css}"

    with open(template_path, 'r', encoding='utf-8') as f:
        template = f.read()

    # Replace {{GENERATED_UTILITIES}} placeholder
    output = template.replace('{{GENERATED_UTILITIES}}', utilities_css)

    # Note: Other template variables would need to be replaced by the full extraction process
    # For now, we're just adding utilities support
    return output


def transform_tokens(tokens: Dict[str, Any], output_format: str, config: Dict[str, Any] = None) -> str:
    """
    Main transformation function.

    Args:
        tokens: W3C token dictionary
        output_format: Target format (css, scss, swift, kotlin, utilities, etc.)
        config: Optional configuration (used for utilities format)

    Returns:
        Transformed token string
    """
    formats = {
        'css': to_css_custom_properties,
        'css-layers': to_css_with_layers,
        'scss': to_scss_variables,
        'swift': to_swift,
        'kotlin': to_kotlin,
        'utilities': lambda t: to_utilities(t, config),
        'css-layers-full': to_css_layers_with_utilities
    }

    if output_format not in formats:
        raise ValueError(f"Unsupported format: {output_format}. Supported: {', '.join(formats.keys())}")

    return formats[output_format](tokens)


def main():
    """Main entry point for the script."""
    parser = argparse.ArgumentParser(
        description='Transform W3C Design Tokens to various formats',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Supported formats:
  css              - CSS custom properties in :root
  css-layers       - CSS with @layer organization
  css-layers-full  - CSS with @layer organization + generated atomic utilities
  utilities        - Standalone atomic utility classes (Tailwind-style)
  scss             - SCSS variables
  swift            - iOS Swift struct
  kotlin           - Android Kotlin object

Examples:
  python transform_tokens.py --input tokens.json --format css --output tokens.css
  python transform_tokens.py --input tokens.json --format utilities --output utilities.css
  python transform_tokens.py --input tokens.json --format css-layers-full --output design-system.css
  python transform_tokens.py --input tokens.json --format scss --output _tokens.scss
  python transform_tokens.py --input tokens.json --format swift --output Tokens.swift

Utility Generation:
  The 'utilities' format generates comprehensive atomic utility classes including:
  - Color utilities (text, background, border, fill, stroke)
  - Spacing utilities with logical properties
  - Typography utilities
  - Layout utilities (border-radius, shadows)
  - Responsive variants (container queries)
  - State variants (hover, focus, active)
  - Dark mode support

  Use 'css-layers-full' to get a complete design system with tokens + utilities.
        """
    )

    parser.add_argument(
        '--input',
        type=str,
        required=True,
        help='Input W3C token JSON file'
    )

    parser.add_argument(
        '--format',
        type=str,
        required=True,
        choices=['css', 'css-layers', 'css-layers-full', 'utilities', 'scss', 'swift', 'kotlin'],
        help='Output format'
    )

    parser.add_argument(
        '--output',
        type=str,
        required=True,
        help='Output file path'
    )

    parser.add_argument(
        '--config',
        type=str,
        help='Optional configuration JSON file (for utilities format)'
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

    # Transform tokens
    try:
        output = transform_tokens(tokens, args.format, config)
    except ValueError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)

    # Write output
    output_path = Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(output)

    print(f"✓ Tokens transformed successfully to {args.output}")
    print(f"  Format: {args.format}")
    if args.format in ['utilities', 'css-layers-full']:
        print("  ✓ Atomic utilities generated")
        if config:
            print(f"  Categories: {', '.join(config.get('categories', []))}")
            print(f"  Variants: {', '.join(config.get('variants', []))}")


if __name__ == '__main__':
    main()
