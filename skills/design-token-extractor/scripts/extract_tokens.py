#!/usr/bin/env python3
"""
Extract design tokens from image analysis.

This script takes extracted design elements and converts them into
W3C Design Tokens Community Group (DTCG) compliant JSON format.

Usage:
    python extract_tokens.py --input-image <path> --output tokens.json
    python extract_tokens.py --input-data <json> --output tokens.json
    python extract_tokens.py --help
"""

import argparse
import json
import sys
from pathlib import Path
from typing import Dict, Any, List


def create_token(value: str, token_type: str, description: str = "") -> Dict[str, Any]:
    """
    Create a W3C DTCG compliant token object.

    Args:
        value: The token value
        token_type: The W3C token type (color, dimension, fontFamily, etc.)
        description: Optional description of the token's usage

    Returns:
        Dictionary with $value, $type, and optional $description
    """
    token = {
        "$value": value,
        "$type": token_type
    }
    if description:
        token["$description"] = description
    return token


def extract_color_tokens(colors: List[Dict[str, str]]) -> Dict[str, Any]:
    """
    Extract and organize color tokens.

    Args:
        colors: List of color dictionaries with 'name', 'value', and 'role'

    Returns:
        Nested dictionary of color tokens organized by role
    """
    tokens = {}

    for color in colors:
        name = color.get('name', 'unnamed')
        value = color.get('value', '#000000')
        role = color.get('role', 'neutral')
        description = color.get('description', '')

        # Organize by role (primary, secondary, neutral, etc.)
        if role not in tokens:
            tokens[role] = {}

        tokens[role][name] = create_token(value, "color", description)

    return tokens


def extract_typography_tokens(typography: List[Dict[str, Any]]) -> Dict[str, Any]:
    """
    Extract and organize typography tokens.

    Args:
        typography: List of typography dictionaries

    Returns:
        Nested dictionary of typography tokens
    """
    tokens = {
        "fontFamily": {},
        "fontSize": {},
        "fontWeight": {},
        "lineHeight": {}
    }

    for typo in typography:
        name = typo.get('name', 'unnamed')

        if 'fontFamily' in typo:
            tokens["fontFamily"][name] = create_token(
                typo['fontFamily'],
                "fontFamily",
                typo.get('description', '')
            )

        if 'fontSize' in typo:
            tokens["fontSize"][name] = create_token(
                typo['fontSize'],
                "dimension",
                typo.get('description', '')
            )

        if 'fontWeight' in typo:
            tokens["fontWeight"][name] = create_token(
                typo['fontWeight'],
                "fontWeight",
                typo.get('description', '')
            )

        if 'lineHeight' in typo:
            tokens["lineHeight"][name] = create_token(
                typo['lineHeight'],
                "number",
                typo.get('description', '')
            )

    # Remove empty categories
    return {k: v for k, v in tokens.items() if v}


def extract_spacing_tokens(spacing: List[Dict[str, str]]) -> Dict[str, Any]:
    """
    Extract and organize spacing tokens.

    Args:
        spacing: List of spacing dictionaries

    Returns:
        Nested dictionary of spacing tokens
    """
    tokens = {"scale": {}}

    for space in spacing:
        name = space.get('name', 'unnamed')
        value = space.get('value', '0')
        description = space.get('description', '')

        tokens["scale"][name] = create_token(value, "dimension", description)

    return tokens


def extract_dimension_tokens(dimensions: List[Dict[str, str]]) -> Dict[str, Any]:
    """
    Extract and organize dimension tokens (border radius, shadows, etc.).

    Args:
        dimensions: List of dimension dictionaries

    Returns:
        Nested dictionary of dimension tokens
    """
    tokens = {
        "borderRadius": {},
        "shadow": {},
        "other": {}
    }

    for dim in dimensions:
        name = dim.get('name', 'unnamed')
        value = dim.get('value', '0')
        category = dim.get('category', 'other')
        description = dim.get('description', '')

        if category in tokens:
            tokens[category][name] = create_token(value, "dimension", description)
        else:
            tokens["other"][name] = create_token(value, "dimension", description)

    # Remove empty categories
    return {k: v for k, v in tokens.items() if v}


def extract_motion_tokens(motion: List[Dict[str, str]]) -> Dict[str, Any]:
    """
    Extract and organize motion/animation tokens.

    Args:
        motion: List of motion dictionaries

    Returns:
        Nested dictionary of motion tokens
    """
    tokens = {
        "duration": {},
        "easing": {}
    }

    for anim in motion:
        name = anim.get('name', 'unnamed')

        if 'duration' in anim:
            tokens["duration"][name] = create_token(
                anim['duration'],
                "duration",
                anim.get('description', '')
            )

        if 'easing' in anim:
            tokens["easing"][name] = create_token(
                anim['easing'],
                "cubicBezier",
                anim.get('description', '')
            )

    # Remove empty categories
    return {k: v for k, v in tokens.items() if v}


def extract_tokens(input_data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Main extraction function that processes input data and creates W3C tokens.

    Args:
        input_data: Dictionary containing extracted design elements

    Returns:
        W3C DTCG compliant token structure
    """
    tokens = {}

    # Extract different token categories
    if 'colors' in input_data:
        tokens['color'] = extract_color_tokens(input_data['colors'])

    if 'typography' in input_data:
        typo_tokens = extract_typography_tokens(input_data['typography'])
        tokens.update(typo_tokens)

    if 'spacing' in input_data:
        tokens['spacing'] = extract_spacing_tokens(input_data['spacing'])

    if 'dimensions' in input_data:
        dimension_tokens = extract_dimension_tokens(input_data['dimensions'])
        for category, values in dimension_tokens.items():
            tokens[category] = values

    if 'motion' in input_data:
        motion_tokens = extract_motion_tokens(input_data['motion'])
        tokens['motion'] = motion_tokens

    return tokens


def main():
    """Main entry point for the script."""
    parser = argparse.ArgumentParser(
        description='Extract design tokens from image analysis',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python extract_tokens.py --input-data colors.json --output tokens.json
  python extract_tokens.py --input-data design.json --output tokens.json --pretty
        """
    )

    parser.add_argument(
        '--input-data',
        type=str,
        help='Path to JSON file containing extracted design elements'
    )

    parser.add_argument(
        '--output',
        type=str,
        required=True,
        help='Output path for W3C token JSON file'
    )

    parser.add_argument(
        '--pretty',
        action='store_true',
        help='Pretty-print JSON output with indentation'
    )

    args = parser.parse_args()

    # Load input data
    if args.input_data:
        input_path = Path(args.input_data)
        if not input_path.exists():
            print(f"Error: Input file not found: {args.input_data}", file=sys.stderr)
            sys.exit(1)

        with open(input_path, 'r', encoding='utf-8') as f:
            input_data = json.load(f)
    else:
        print("Error: --input-data is required", file=sys.stderr)
        sys.exit(1)

    # Extract tokens
    tokens = extract_tokens(input_data)

    # Write output
    output_path = Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    with open(output_path, 'w', encoding='utf-8') as f:
        if args.pretty:
            json.dump(tokens, f, indent=2, ensure_ascii=False)
        else:
            json.dump(tokens, f, ensure_ascii=False)

    print(f"✓ Tokens extracted successfully to {args.output}")
    print(f"  Total token categories: {len(tokens)}")


if __name__ == '__main__':
    main()
