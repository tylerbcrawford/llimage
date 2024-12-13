"""
Enhanced chart detection module with improved shape analysis and classification.
"""

import logging
import cv2
import numpy as np
from typing import Dict, List, Optional, Tuple, Any

logger = logging.getLogger(__name__)

class ChartDetector:
    """Detects and classifies different types of charts in images."""

    def __init__(self, config: Optional[Dict] = None):
        """Initialize the chart detector with configuration."""
        self.config = config or {}
        self.min_confidence = self.config.get('min_confidence', 0.7)
        self.min_shape_area = self.config.get('min_shape_area', 100)
        self.shape_similarity_threshold = self.config.get('shape_similarity_threshold', 0.85)
        logger.info("Initializing ChartDetector with enhanced detection")

    def preprocess_image(self, image: np.ndarray) -> np.ndarray:
        """Preprocess image for enhanced chart detection."""
        # Convert to grayscale if needed
        if len(image.shape) == 3:
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        else:
            gray = image

        # Apply binary threshold
        _, binary = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY)

        # Clean up noise
        kernel = np.ones((3,3), np.uint8)
        cleaned = cv2.morphologyEx(binary, cv2.MORPH_CLOSE, kernel)
        cleaned = cv2.morphologyEx(cleaned, cv2.MORPH_OPEN, kernel)

        return cleaned

    def detect_shapes(self, image: np.ndarray) -> Tuple[List[np.ndarray], List[str], List[Dict[str, Any]]]:
        """Detect shapes with enhanced accuracy and feature extraction."""
        # Find contours
        contours, _ = cv2.findContours(
            image, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE
        )

        shapes = []
        shape_types = []
        shape_features = []

        # Sort contours by area (largest first)
        contours = sorted(contours, key=cv2.contourArea, reverse=True)

        for contour in contours:
            # Filter small contours
            area = cv2.contourArea(contour)
            if area < self.min_shape_area:
                continue

            # Extract features with different epsilon values
            features = self._extract_shape_features(contour)
            shape_type = self._classify_shape(features)
            
            if shape_type != "unknown":
                shapes.append(contour)
                shape_types.append(shape_type)
                shape_features.append(features)

        return shapes, shape_types, shape_features

    def _extract_shape_features(self, contour: np.ndarray) -> Dict[str, Any]:
        """Extract comprehensive features from a shape contour."""
        # Basic measurements
        area = cv2.contourArea(contour)
        perimeter = cv2.arcLength(contour, True)
        x, y, w, h = cv2.boundingRect(contour)
        
        # Advanced features
        hull = cv2.convexHull(contour)
        hull_area = cv2.contourArea(hull)
        solidity = float(area) / hull_area if hull_area > 0 else 0
        
        # Aspect ratio and extent
        aspect_ratio = float(w) / h if h != 0 else 0
        rect_area = w * h
        extent = float(area) / rect_area if rect_area > 0 else 0
        
        # Minimum enclosing circle
        (x_c, y_c), radius = cv2.minEnclosingCircle(contour)
        circle_area = np.pi * radius * radius
        circularity = float(area) / circle_area if circle_area > 0 else 0

        # Try different epsilon values for vertex detection
        epsilons = [0.01, 0.02, 0.03, 0.04, 0.05]
        best_approx = None
        best_vertices = 0
        best_epsilon = 0

        for epsilon in epsilons:
            approx = cv2.approxPolyDP(contour, epsilon * perimeter, True)
            vertices = len(approx)
            
            # Prefer approximations with 3-4 vertices
            if vertices in [3, 4]:
                best_approx = approx
                best_vertices = vertices
                best_epsilon = epsilon
                break
            
            # Otherwise take the first reasonable approximation
            if best_approx is None and 3 <= vertices <= 6:
                best_approx = approx
                best_vertices = vertices
                best_epsilon = epsilon

        if best_approx is None:
            best_approx = cv2.approxPolyDP(contour, 0.02 * perimeter, True)
            best_vertices = len(best_approx)
            best_epsilon = 0.02

        print(f"Best epsilon: {best_epsilon}, vertices: {best_vertices}")

        return {
            "area": area,
            "perimeter": perimeter,
            "bounding_box": (x, y, w, h),
            "center": (x + w//2, y + h//2),
            "solidity": solidity,
            "aspect_ratio": aspect_ratio,
            "extent": extent,
            "circularity": circularity,
            "vertices": best_vertices,
            "approx": best_approx,
            "epsilon": best_epsilon
        }

    def _classify_shape(self, features: Dict[str, Any]) -> str:
        """Classify shape type based on geometric properties."""
        vertices = features["vertices"]
        solidity = features["solidity"]
        circularity = features["circularity"]
        extent = features["extent"]
        aspect_ratio = features["aspect_ratio"]
        epsilon = features["epsilon"]

        # Print debug info for shape classification
        print(f"\nClassifying shape with features:")
        print(f"  Vertices: {vertices}")
        print(f"  Solidity: {solidity:.2f}")
        print(f"  Circularity: {circularity:.2f}")
        print(f"  Extent: {extent:.2f}")
        print(f"  Aspect Ratio: {aspect_ratio:.2f}")
        print(f"  Epsilon: {epsilon:.3f}")

        # Circle detection - high circularity and solidity
        if circularity > 0.80 and solidity > 0.90:
            print("  -> Classified as circle")
            return "circle"
        
        # Rectangle/Square detection - 4 vertices and high extent
        if vertices == 4 and extent > 0.90:
            if 0.95 <= aspect_ratio <= 1.05:
                print("  -> Classified as square")
                return "square"
            else:
                print("  -> Classified as rectangle")
                return "rectangle"
        
        # Triangle detection - exactly 3 vertices and good solidity
        if vertices == 3 and solidity > 0.85:
            print("  -> Classified as triangle")
            return "triangle"

        print("  -> Classified as unknown")
        return "unknown"

    def detect(self, image: np.ndarray) -> Dict[str, Any]:
        """Main detection method with enhanced chart analysis."""
        try:
            processed = self.preprocess_image(image)
            shapes, shape_types, shape_features = self.detect_shapes(processed)
            
            result = {
                "success": len(shapes) > 0,
                "shape_count": len(shapes),
                "shape_types": shape_types,
                "shapes": shapes,
                "features": shape_features
            }

            logger.info(f"Shape detection complete: found {len(shapes)} shapes")
            return result

        except Exception as e:
            logger.error(f"Error during shape detection: {str(e)}")
            return {
                "success": False,
                "shape_count": 0,
                "shape_types": [],
                "shapes": [],
                "features": [],
                "error": str(e)
            }
