"""
Chart processing package for LLiMage.

This package provides functionality for detecting and analyzing charts in PDF documents.
"""

import logging
from .detector import ChartDetector

logger = logging.getLogger(__name__)

__all__ = ['ChartDetector']

# Version of the chart processing module
__version__ = '0.1.0'

logger.info(f"Initializing chart processing module v{__version__}")

# Initialize default configuration
DEFAULT_CONFIG = {
    'chart_detection': {
        'enabled': True,
        'min_confidence': 0.7,
        'types': ['bar', 'line', 'pie']
    }
}
