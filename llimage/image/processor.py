"""
Image processing module using OpenCV for chart analysis.
"""

import cv2
import numpy as np
import logging
from typing import Dict, List, Optional, Tuple

logger = logging.getLogger(__name__)

class ImageProcessor:
    """Handles image processing operations using OpenCV."""

    def __init__(self, config: Optional[Dict] = None):
        """Initialize the image processor.
        
        Args:
            config: Configuration dictionary for image processing parameters.
        """
        self.config = config or {}
        logger.info("Initializing ImageProcessor")

    def preprocess(self, image: np.ndarray) -> np.ndarray:
        """Preprocess image for analysis.
        
        Args:
            image: Input image as numpy array.
            
        Returns:
            Preprocessed image.
        """
        # Convert to grayscale if needed
        if len(image.shape) == 3:
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        else:
            gray = image

        # Apply adaptive thresholding
        thresh = cv2.adaptiveThreshold(
            gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 11, 2
        )

        # Noise reduction
        denoised = cv2.fastNlMeansDenoising(thresh)

        logger.debug("Image preprocessing completed")
        return denoised

    def detect_shapes(self, image: np.ndarray) -> Tuple[List[np.ndarray], List[str]]:
        """Detect shapes in the preprocessed image.
        
        Args:
            image: Preprocessed image.
            
        Returns:
            Tuple of (contours, shape_types).
        """
        # Find contours
        contours, _ = cv2.findContours(
            image, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE
        )

        shapes = []
        shape_types = []

        for contour in contours:
            # Approximate the contour
            peri = cv2.arcLength(contour, True)
            approx = cv2.approxPolyDP(contour, 0.04 * peri, True)
            
            # Identify shape based on vertices
            vertices = len(approx)
            if vertices == 3:
                shape_types.append("triangle")
            elif vertices == 4:
                shape_types.append("rectangle")
            elif vertices > 8:
                shape_types.append("circle")
            else:
                shape_types.append("unknown")
            
            shapes.append(approx)

        logger.debug(f"Detected {len(shapes)} shapes")
        return shapes, shape_types

    def detect_text_regions(self, image: np.ndarray) -> List[Tuple[int, int, int, int]]:
        """Detect potential text regions in the image.
        
        Args:
            image: Input image.
            
        Returns:
            List of text region bounding boxes (x, y, w, h).
        """
        # Convert to grayscale if needed
        if len(image.shape) == 3:
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        else:
            gray = image

        # Apply adaptive threshold
        thresh = cv2.adaptiveThreshold(
            gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 11, 2
        )

        # Find contours
        contours, _ = cv2.findContours(
            thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE
        )

        # Filter contours that might be text
        text_regions = []
        for contour in contours:
            x, y, w, h = cv2.boundingRect(contour)
            aspect_ratio = w / float(h)
            area = w * h
            
            # Filter based on aspect ratio and area
            if 0.1 < aspect_ratio < 15 and area > 100:
                text_regions.append((x, y, w, h))

        logger.debug(f"Detected {len(text_regions)} potential text regions")
        return text_regions

    def extract_features(self, image: np.ndarray) -> Dict:
        """Extract features from the image for chart analysis.
        
        Args:
            image: Input image.
            
        Returns:
            Dictionary containing extracted features.
        """
        processed = self.preprocess(image)
        shapes, shape_types = self.detect_shapes(processed)
        text_regions = self.detect_text_regions(image)

        features = {
            "shapes": {
                "count": len(shapes),
                "types": shape_types
            },
            "text_regions": {
                "count": len(text_regions),
                "boxes": text_regions
            }
        }

        logger.info("Feature extraction completed")
        return features
