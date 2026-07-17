"""Output formatting for CLI."""

import json
from typing import Any


def format_json(data: Any, indent: int = 2) -> str:
    """Format data as JSON string."""
    return json.dumps(data, indent=indent, default=str)


def print_json(data: Any, indent: int = 2) -> None:
    """Print data as JSON to stdout."""
    print(format_json(data, indent=indent))
