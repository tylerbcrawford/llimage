"""
Image processing package for LLiMage.

This package provides functionality for image processing and analysis using OpenCV.
"""

import logging
from .opencv import OpenCVWrapper
from .processor import ImageProcessor

logger = logging.getLogger(__name__)

__all__ = ['OpenCVWrapper', 'ImageProcessor']

# Version of the image processing module
__version__ = '0.1.0'

logger.info(f"Initializing image processing module v{__version__}")

# Initialize default configuration
DEFAULT_CONFIG = {
    'preprocessing': {
        'grayscale': True,
        'denoise': True,
        'threshold': 'adaptive'
    },
    'text_detection': {
        'min_area': 100,
        'aspect_ratio_range': (0.1, 15)
    }
}
