"""
Output formatting module for chart detection results.

This module provides formatters for converting chart detection results into
different output formats (JSON and text).
"""

from typing import Dict, Optional, Union
from .json import JsonFormatter
from .text import TextFormatter

__all__ = ['JsonFormatter', 'TextFormatter', 'create_formatter']

def create_formatter(
    format_type: str,
    config: Optional[Dict] = None
) -> Union[JsonFormatter, TextFormatter]:
    """Create a formatter instance of the specified type.
    
    Args:
        format_type: Type of formatter to create ('json' or 'text')
        config: Optional configuration dictionary for the formatter
    
    Returns:
        Instance of JsonFormatter or TextFormatter
    
    Raises:
        ValueError: If format_type is not 'json' or 'text'
    """
    if format_type.lower() == 'json':
        return JsonFormatter(config)
    elif format_type.lower() == 'text':
        return TextFormatter(config)
    else:
        raise ValueError(
            f"Invalid format type: {format_type}. Must be 'json' or 'text'."
        )

# Version of the output module
__version__ = '1.0.0'

# Default configuration for formatters
DEFAULT_CONFIG = {
    'detail_level': 'standard',
    'include_metadata': True,
    'include_confidence': True,
    'pretty_print': True  # Only used by JsonFormatter
}
