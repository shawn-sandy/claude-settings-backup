#!/usr/bin/env python3
"""
Validate design tokens against W3C Design Tokens Community Group specification.

Checks token structure, required fields, valid types, and value formats
according to the W3C DTCG specification.

Usage:
    python validate_tokens.py --input tokens.json
    python validate_tokens.py --input tokens.json --strict
    python validate_tokens.py --help
"""

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Dict, Any, List, Tuple


# W3C DTCG valid token types
VALID_TOKEN_TYPES = {
    'color',
    'dimension',
    'fontFamily',
    'fontWeight',
    'duration',
    'cubicBezier',
    'number',
    'strokeStyle',
    'border',
    'transition',
    'shadow',
    'gradient',
    'typography'
}


class ValidationError:
    """Represents a validation error."""

    def __init__(self, path: str, message: str, severity: str = 'error'):
        self.path = path
        self.message = message
        self.severity = severity

    def __str__(self):
        symbol = '✗' if self.severity == 'error' else '⚠'
        return f"{symbol} {self.path}: {self.message}"


def validate_token_structure(token: Any, path: str) -> List[ValidationError]:
    """
    Validate that a token has the correct structure.

    Args:
        token: Token object to validate
        path: Current path for error reporting

    Returns:
        List of validation errors
    """
    errors = []

    if not isinstance(token, dict):
        errors.append(ValidationError(path, "Token must be an object"))
        return errors

    # Check for required $value field
    if '$value' not in token:
        errors.append(ValidationError(path, "Missing required $value field"))

    # Check for $type field (recommended but not always required)
    if '$type' not in token:
        errors.append(ValidationError(
            path,
            "Missing $type field (recommended for clarity)",
            severity='warning'
        ))
    else:
        token_type = token['$type']
        if token_type not in VALID_TOKEN_TYPES:
            errors.append(ValidationError(
                path,
                f"Invalid $type '{token_type}'. Valid types: {', '.join(sorted(VALID_TOKEN_TYPES))}"
            ))

    return errors


def validate_color_value(value: str, path: str) -> List[ValidationError]:
    """Validate color value format."""
    errors = []

    # Support hex colors (#RGB, #RRGGBB, #RRGGBBAA)
    hex_pattern = r'^#([0-9a-fA-F]{3}|[0-9a-fA-F]{6}|[0-9a-fA-F]{8})$'

    # Support rgb/rgba
    rgb_pattern = r'^rgba?\([^)]+\)$'

    # Support hsl/hsla
    hsl_pattern = r'^hsla?\([^)]+\)$'

    # Support oklch
    oklch_pattern = r'^oklch\([^)]+\)$'

    # Support token reference
    ref_pattern = r'^\{[^}]+\}$'

    if not any([
        re.match(hex_pattern, value),
        re.match(rgb_pattern, value),
        re.match(hsl_pattern, value),
        re.match(oklch_pattern, value),
        re.match(ref_pattern, value)
    ]):
        errors.append(ValidationError(
            path,
            f"Invalid color value '{value}'. Must be hex, rgb, hsl, oklch, or token reference"
        ))

    return errors


def validate_dimension_value(value: str, path: str) -> List[ValidationError]:
    """Validate dimension value format."""
    errors = []

    # Support CSS units (px, rem, em, %, etc.)
    dimension_pattern = r'^-?[\d.]+(?:px|rem|em|%|vw|vh|vmin|vmax|cqi|cqb|cqw|cqh|cqmin|cqmax)?$'

    # Support token reference
    ref_pattern = r'^\{[^}]+\}$'

    # Support calc() expressions
    calc_pattern = r'^calc\([^)]+\)$'

    # Support clamp() expressions
    clamp_pattern = r'^clamp\([^)]+\)$'

    if not any([
        re.match(dimension_pattern, value),
        re.match(ref_pattern, value),
        re.match(calc_pattern, value),
        re.match(clamp_pattern, value)
    ]):
        errors.append(ValidationError(
            path,
            f"Invalid dimension value '{value}'. Must be number with unit, calc(), clamp(), or token reference"
        ))

    return errors


def validate_token_value(token: Dict[str, Any], path: str) -> List[ValidationError]:
    """
    Validate token value based on its type.

    Args:
        token: Token object
        path: Current path for error reporting

    Returns:
        List of validation errors
    """
    errors = []

    if '$value' not in token:
        return errors  # Already reported by structure validation

    value = token['$value']
    token_type = token.get('$type', '')

    # Type-specific validation
    if token_type == 'color' and isinstance(value, str):
        errors.extend(validate_color_value(value, path))

    elif token_type == 'dimension' and isinstance(value, str):
        errors.extend(validate_dimension_value(value, path))

    elif token_type == 'fontFamily':
        if not isinstance(value, (str, list)):
            errors.append(ValidationError(
                path,
                "fontFamily value must be string or array of strings"
            ))

    elif token_type == 'fontWeight':
        if isinstance(value, str):
            valid_weights = {'100', '200', '300', '400', '500', '600', '700', '800', '900', 'normal', 'bold'}
            if value not in valid_weights and not re.match(r'^\{[^}]+\}$', value):
                errors.append(ValidationError(
                    path,
                    f"Invalid fontWeight '{value}'. Must be 100-900, 'normal', 'bold', or token reference"
                ))
        elif not isinstance(value, int):
            errors.append(ValidationError(path, "fontWeight must be string or number"))

    elif token_type == 'duration' and isinstance(value, str):
        duration_pattern = r'^-?[\d.]+(?:ms|s)$'
        ref_pattern = r'^\{[^}]+\}$'
        if not (re.match(duration_pattern, value) or re.match(ref_pattern, value)):
            errors.append(ValidationError(
                path,
                f"Invalid duration '{value}'. Must be number with ms/s unit or token reference"
            ))

    return errors


def validate_tokens(tokens: Dict[str, Any], path: str = "") -> List[ValidationError]:
    """
    Recursively validate token structure.

    Args:
        tokens: Token dictionary or group
        path: Current path for error reporting

    Returns:
        List of validation errors
    """
    errors = []

    for key, value in tokens.items():
        current_path = f"{path}.{key}" if path else key

        if isinstance(value, dict):
            # Check if this is a token (has $value) or a group
            if '$value' in value:
                # This is a token - validate it
                errors.extend(validate_token_structure(value, current_path))
                errors.extend(validate_token_value(value, current_path))
            else:
                # This is a group - recurse
                errors.extend(validate_tokens(value, current_path))

    return errors


def main():
    """Main entry point for the script."""
    parser = argparse.ArgumentParser(
        description='Validate design tokens against W3C DTCG specification',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python validate_tokens.py --input tokens.json
  python validate_tokens.py --input tokens.json --strict
        """
    )

    parser.add_argument(
        '--input',
        type=str,
        required=True,
        help='Input W3C token JSON file to validate'
    )

    parser.add_argument(
        '--strict',
        action='store_true',
        help='Treat warnings as errors'
    )

    args = parser.parse_args()

    # Load tokens
    input_path = Path(args.input)
    if not input_path.exists():
        print(f"Error: Input file not found: {args.input}", file=sys.stderr)
        sys.exit(1)

    try:
        with open(input_path, 'r', encoding='utf-8') as f:
            tokens = json.load(f)
    except json.JSONDecodeError as e:
        print(f"Error: Invalid JSON in {args.input}: {e}", file=sys.stderr)
        sys.exit(1)

    # Validate tokens
    errors = validate_tokens(tokens)

    # Filter errors based on strict mode
    if args.strict:
        all_errors = errors
    else:
        all_errors = [e for e in errors if e.severity == 'error']
        warnings = [e for e in errors if e.severity == 'warning']

    # Print results
    if all_errors or (not args.strict and warnings):
        if all_errors:
            print(f"\nFound {len(all_errors)} error(s):")
            for error in all_errors:
                print(f"  {error}")

        if not args.strict and warnings:
            print(f"\nFound {len(warnings)} warning(s):")
            for warning in warnings:
                print(f"  {warning}")

        print()

        if all_errors:
            sys.exit(1)
    else:
        print(f"✓ All tokens valid according to W3C DTCG specification")
        sys.exit(0)


if __name__ == '__main__':
    main()
