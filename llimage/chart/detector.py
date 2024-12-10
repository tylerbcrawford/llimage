"""
Chart detection module for identifying and classifying different types of charts in images.
"""

import logging
import cv2
import numpy as np
from typing import Dict, List, Optional, Tuple

logger = logging.getLogger(__name__)

class ChartDetector:
    """Detects and classifies different types of charts in images."""

    def __init__(self, config: Optional[Dict] = None):
        """Initialize the chart detector with configuration.
        
        Args:
            config: Configuration dictionary for chart detection parameters.
        """
        self.config = config or {}
        self.min_confidence = self.config.get('min_confidence', 0.7)
        logger.info("Initializing ChartDetector")

    def preprocess_image(self, image: np.ndarray) -> np.ndarray:
        """Preprocess the image for chart detection.
        
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
        """Detect basic shapes in the image that might indicate chart elements.
        
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

    def classify_chart(self, image: np.ndarray) -> Tuple[str, float]:
        """Classify the type of chart in the image.
        
        Args:
            image: Input image as numpy array.
            
        Returns:
            Tuple of (chart_type, confidence).
        """
        processed = self.preprocess_image(image)
        shapes, shape_types = self.detect_shapes(processed)

        # Count shape types
        shape_counts = {
            "rectangle": shape_types.count("rectangle"),
            "circle": shape_types.count("circle"),
            "line": shape_types.count("unknown")  # Lines often detected as unknown
        }

        # Basic classification logic
        if shape_counts["rectangle"] > 3:
            # Multiple rectangles suggest bar chart
            return "bar", 0.8
        elif shape_counts["circle"] > 0:
            # Presence of circle suggests pie chart
            return "pie", 0.9
        elif shape_counts["line"] > shape_counts["rectangle"]:
            # More lines than rectangles suggest line chart
            return "line", 0.7
        else:
            return "unknown", 0.0

    def detect(self, image: np.ndarray) -> Dict:
        """Main detection method for identifying charts in images.
        
        Args:
            image: Input image as numpy array.
            
        Returns:
            Dictionary containing detection results.
        """
        try:
            chart_type, confidence = self.classify_chart(image)
            
            result = {
                "type": chart_type,
                "confidence": confidence,
                "success": confidence >= self.min_confidence
            }

            logger.info(f"Chart detection complete: {result}")
            return result

        except Exception as e:
            logger.error(f"Error during chart detection: {str(e)}")
            return {
                "type": "unknown",
                "confidence": 0.0,
                "success": False,
                "error": str(e)
            }
