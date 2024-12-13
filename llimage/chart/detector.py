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
        self.min_shape_area = self.config.get('min_shape_area', 50)
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

        # Clean up noise and separate shapes
        kernel = np.ones((3,3), np.uint8)
        cleaned = cv2.morphologyEx(binary, cv2.MORPH_OPEN, kernel)  # Remove small noise
        
        # Dilate to separate touching shapes
        cleaned = cv2.dilate(cleaned, kernel, iterations=1)
        # Erode back to original size while maintaining separation
        cleaned = cv2.erode(cleaned, kernel, iterations=1)
        
        # Additional morphological operations for better separation
        cleaned = cv2.morphologyEx(cleaned, cv2.MORPH_CLOSE, kernel)

        return cleaned

    def detect_shapes(self, image: np.ndarray) -> Tuple[List[np.ndarray], List[str], List[Dict[str, Any]]]:
        """Detect shapes with enhanced accuracy and feature extraction."""
        # Find all contours, including inner ones
        contours, hierarchy = cv2.findContours(
            image, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE
        )

        shapes = []
        shape_types = []
        shape_features = []

        # Sort contours by area (largest first)
        contours = sorted(contours, key=cv2.contourArea, reverse=True)

        # Keep track of processed areas to avoid duplicates
        processed_areas = set()

        for contour in contours:
            # Filter small contours
            area = cv2.contourArea(contour)
            if area < self.min_shape_area:
                continue

            # Check if this area overlaps with already processed ones
            x, y, w, h = cv2.boundingRect(contour)
            bbox = (x, y, w, h)
            
            # Skip if too similar to already processed shape
            overlap = False
            for other_bbox in processed_areas:
                ox, oy, ow, oh = other_bbox
                # Check for significant overlap
                if (x < ox + ow and x + w > ox and
                    y < oy + oh and y + h > oy):
                    intersection = (min(x + w, ox + ow) - max(x, ox)) * \
                                 (min(y + h, oy + oh) - max(y, oy))
                    union = w * h + ow * oh - intersection
                    if intersection / union > 0.5:  # More than 50% overlap
                        overlap = True
                        break
            
            if overlap:
                continue

            # Extract features
            features = self._extract_shape_features(contour)
            shape_type = self._classify_shape(features)
            
            if shape_type != "unknown":
                shapes.append(contour)
                shape_types.append(shape_type)
                shape_features.append(features)
                processed_areas.add(bbox)

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

        # Calculate center of mass
        M = cv2.moments(contour)
        if M["m00"] != 0:
            cx = int(M["m10"] / M["m00"])
            cy = int(M["m01"] / M["m00"])
        else:
            cx, cy = x + w//2, y + h//2

        # Vertex detection with adaptive epsilon
        if area < 500:  # Small shapes like points
            epsilon = 0.02 * perimeter
        elif area < 2000:  # Medium shapes
            epsilon = 0.03 * perimeter
        else:  # Large shapes like pie segments
            epsilon = 0.04 * perimeter

        approx = cv2.approxPolyDP(contour, epsilon, True)
        vertices = len(approx)

        # Calculate arc features for pie segments
        arc_score = 0
        if area > 1000:  # Only for larger shapes
            # Calculate distances from center of mass to contour points
            points = contour.reshape(-1, 2)
            distances = np.sqrt(np.sum((points - [cx, cy]) ** 2, axis=1))
            angles = np.arctan2(points[:, 1] - cy, points[:, 0] - cx)
            angles = np.degrees(angles) % 360
            
            # Sort angles and find largest gap
            angles.sort()
            gaps = np.diff(angles)
            max_gap = np.max(gaps) if len(gaps) > 0 else 0
            
            # Calculate scores
            distance_score = 1.0 - np.std(distances) / np.mean(distances)
            gap_score = max_gap / 360.0
            
            arc_score = (distance_score + gap_score) / 2

        # Print debug info
        print(f"Shape features - Area: {area:.1f}, Vertices: {vertices}, "
              f"Circularity: {circularity:.2f}, Arc Score: {arc_score:.2f}")

        return {
            "area": area,
            "perimeter": perimeter,
            "bounding_box": (x, y, w, h),
            "center": (cx, cy),
            "solidity": solidity,
            "aspect_ratio": aspect_ratio,
            "extent": extent,
            "circularity": circularity,
            "vertices": vertices,
            "approx": approx,
            "arc_score": arc_score
        }

    def _classify_shape(self, features: Dict[str, Any]) -> str:
        """Classify shape type based on geometric properties."""
        area = features["area"]
        vertices = features["vertices"]
        solidity = features["solidity"]
        circularity = features["circularity"]
        extent = features["extent"]
        aspect_ratio = features["aspect_ratio"]
        arc_score = features["arc_score"]

        # Print debug info
        print(f"\nClassifying shape with features:")
        print(f"  Area: {area:.2f}")
        print(f"  Vertices: {vertices}")
        print(f"  Solidity: {solidity:.2f}")
        print(f"  Circularity: {circularity:.2f}")
        print(f"  Extent: {extent:.2f}")
        print(f"  Aspect Ratio: {aspect_ratio:.2f}")
        print(f"  Arc Score: {arc_score:.2f}")

        # Line chart points (small, circular or near-circular)
        if area < 1000 and solidity > 0.9:
            # Either highly circular or octagonal (8 vertices)
            if circularity > 0.45 or (vertices == 8 and extent > 0.7):
                print("  -> Classified as point")
                return "point"

        # Pie chart segments (large, sector-shaped)
        if area > 5000 and arc_score > 0.3 and solidity > 0.8:
            print("  -> Classified as segment")
            return "segment"

        # Bar chart rectangles (high extent, 4 vertices)
        if vertices == 4 and extent > 0.85:
            if 0.95 <= aspect_ratio <= 1.05:
                print("  -> Classified as square")
                return "square"
            else:
                print("  -> Classified as rectangle")
                return "rectangle"

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
