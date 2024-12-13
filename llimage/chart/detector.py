"""
Enhanced chart detection module with improved shape analysis and classification.
"""

import logging
import cv2
import numpy as np
from typing import Dict, List, Optional, Tuple, Any, Union, overload

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

    def _detect_shapes_internal(self, image: np.ndarray) -> Tuple[List[np.ndarray], List[str], List[Dict[str, float]]]:
        """Internal method for shape detection with full feature extraction."""
        # Find all contours, including inner ones
        contours, hierarchy = cv2.findContours(
            image, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE
        )

        shapes = []
        shape_types = []
        shape_features = []

        # Sort contours by x-coordinate for consistent ordering
        contours = sorted(contours, key=lambda c: cv2.boundingRect(c)[0])

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

            # Extract features and classify
            features = self._extract_shape_features(contour)
            shape_type = self._classify_shape(features)
            
            if shape_type != "unknown":
                shapes.append(contour)
                shape_types.append(shape_type)
                shape_features.append(features)
                processed_areas.add(bbox)

        return shapes, shape_types, shape_features

    @overload
    def detect_shapes(self, image: np.ndarray, include_features: bool = True) -> Tuple[List[np.ndarray], List[str], List[Dict[str, float]]]: ...

    @overload
    def detect_shapes(self, image: np.ndarray, include_features: bool = False) -> Tuple[List[np.ndarray], List[str]]: ...

    def detect_shapes(self, image: np.ndarray, include_features: bool = True) -> Union[
        Tuple[List[np.ndarray], List[str], List[Dict[str, float]]],
        Tuple[List[np.ndarray], List[str]]
    ]:
        """Detect shapes with optional feature extraction."""
        shapes, types, features = self._detect_shapes_internal(image)
        return (shapes, types, features) if include_features else (shapes, types)

    def _extract_shape_features(self, contour: np.ndarray) -> Dict[str, float]:
        """Extract comprehensive features from a shape contour."""
        # Basic measurements
        area = float(cv2.contourArea(contour))
        perimeter = float(cv2.arcLength(contour, True))
        x, y, w, h = cv2.boundingRect(contour)
        
        # Advanced features
        hull = cv2.convexHull(contour)
        hull_area = float(cv2.contourArea(hull))
        solidity = area / hull_area if hull_area > 0 else 0.0
        
        # Aspect ratio and extent
        aspect_ratio = float(w) / h if h != 0 else 0.0
        rect_area = float(w * h)
        extent = area / rect_area if rect_area > 0 else 0.0
        
        # Minimum enclosing circle
        (x_c, y_c), radius = cv2.minEnclosingCircle(contour)
        circle_area = float(np.pi * radius * radius)
        circularity = area / circle_area if circle_area > 0 else 0.0

        # Calculate center of mass
        M = cv2.moments(contour)
        if M["m00"] != 0:
            cx = float(M["m10"] / M["m00"])
            cy = float(M["m01"] / M["m00"])
        else:
            cx, cy = float(x + w/2), float(y + h/2)

        # Vertex detection with adaptive epsilon
        if area < 500:  # Small shapes like points
            epsilon = 0.02 * perimeter
        elif area < 2000:  # Medium shapes
            epsilon = 0.03 * perimeter
        else:  # Large shapes like pie segments
            epsilon = 0.04 * perimeter

        approx = cv2.approxPolyDP(contour, epsilon, True)
        vertices = float(len(approx))

        # Calculate ellipse features
        if len(contour) >= 5:  # Need at least 5 points to fit ellipse
            ellipse = cv2.fitEllipse(contour)
            major_axis = float(max(ellipse[1]))
            minor_axis = float(min(ellipse[1]))
            ellipse_eccentricity = float(np.sqrt(1 - (minor_axis/major_axis)**2)) if major_axis > 0 else 0.0
        else:
            ellipse_eccentricity = 0.0

        # Calculate arc features for pie segments
        arc_score = 0.0
        if area > 1000:  # Only for larger shapes
            # Calculate distances from center of mass to contour points
            points = contour.reshape(-1, 2)
            distances = np.sqrt(np.sum((points - [cx, cy]) ** 2, axis=1))
            angles = np.arctan2(points[:, 1] - cy, points[:, 0] - cx)
            angles = np.degrees(angles) % 360
            
            # Sort angles and find largest gap
            angles.sort()
            gaps = np.diff(angles)
            max_gap = float(np.max(gaps)) if len(gaps) > 0 else 0.0
            
            # Calculate scores
            distance_score = 1.0 - float(np.std(distances)) / float(np.mean(distances))
            gap_score = max_gap / 360.0
            
            # Weight distance score more heavily for arc detection
            arc_score = (0.7 * distance_score + 0.3 * gap_score)

        # Print debug info
        print(f"Shape features - Area: {area:.1f}, Vertices: {vertices}, "
              f"Circularity: {circularity:.2f}, Arc Score: {arc_score:.2f}")

        return {
            "area": area,
            "perimeter": perimeter,
            "bounding_box": (float(x), float(y), float(w), float(h)),
            "center": (cx, cy),
            "solidity": solidity,
            "aspect_ratio": aspect_ratio,
            "extent": extent,
            "circularity": circularity,
            "vertices": vertices,
            "arc_score": arc_score,
            "ellipse_eccentricity": ellipse_eccentricity
        }

    def _classify_shape(self, features: Dict[str, float]) -> str:
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
            # More lenient point detection with multiple criteria
            if (circularity > 0.45 or  # High circularity
                (vertices >= 5 and vertices <= 8 and extent > 0.6) or  # Octagonal-like
                (area < 400 and extent > 0.6 and solidity > 0.95) or  # Small, solid points
                (solidity > 0.95 and extent > 0.7) or  # Very solid and well-filled
                (circularity > 0.4 and extent > 0.65 and solidity > 0.95) or  # Combined criteria
                # Additional criteria for smaller points
                (area < 400 and solidity > 0.95 and extent > 0.65) or  # Small area with good extent
                (area < 500 and vertices <= 6 and solidity > 0.95)):  # Small with few vertices
                print("  -> Classified as point")
                return "point"

        # Bar chart rectangles (high extent, 4 vertices)
        if vertices == 4 and extent > 0.85 and solidity > 0.9:
            print("  -> Classified as rectangle")
            return "rectangle"

        # Triangle detection (3 vertices, moderate extent)
        if vertices == 3 and solidity > 0.9:
            print("  -> Classified as triangle")
            return "triangle"

        # Circle detection (high circularity, not a point)
        if circularity > 0.8 and solidity > 0.9 and area >= 1000:
            print("  -> Classified as circle")
            return "circle"

        # Pie chart segments (large, sector-shaped)
        if area > 1000 and arc_score > 0.3 and solidity > 0.8:  # Relaxed criteria
            if 0.2 <= circularity <= 0.9:  # More lenient range
                print("  -> Classified as segment")
                return "segment"

        print("  -> Classified as unknown")
        return "unknown"

    def analyze_chart_structure(self, shapes: List[np.ndarray], 
                              shape_types: List[str]) -> Dict[str, Any]:
        """Analyze the structural relationships between shapes."""
        if not shapes:
            return {
                "analysis": {
                    "vertical_alignment": 0.0,
                    "horizontal_alignment": 0.0,
                    "radial_arrangement": 0.0,
                    "grid_pattern": 0.0
                },
                "type": None
            }

        # Get centers of all shapes
        centers = []
        for shape in shapes:
            M = cv2.moments(shape)
            if M["m00"] != 0:
                cx = float(M["m10"] / M["m00"])
                cy = float(M["m01"] / M["m00"])
            else:
                x, y, w, h = cv2.boundingRect(shape)
                cx, cy = float(x + w/2), float(y + h/2)
            centers.append((cx, cy))

        # Analyze vertical alignment
        x_coords = [x for x, _ in centers]
        x_range = float(max(x_coords) - min(x_coords)) if len(x_coords) > 1 else 1.0
        x_mean = float(np.mean(x_coords))
        # Handle case where all x coordinates are the same
        if x_range == 0:
            vertical_alignment = 1.0  # Perfect vertical alignment
        else:
            x_deviations = [abs(x - x_mean) / x_range for x in x_coords]
            vertical_alignment = 1.0 - float(np.mean(x_deviations))

        # Analyze horizontal alignment
        y_coords = [y for _, y in centers]
        y_range = float(max(y_coords) - min(y_coords)) if len(y_coords) > 1 else 1.0
        y_mean = float(np.mean(y_coords))
        # Handle case where all y coordinates are the same
        if y_range == 0:
            horizontal_alignment = 1.0  # Perfect horizontal alignment
        else:
            y_deviations = [abs(y - y_mean) / y_range for y in y_coords]
            horizontal_alignment = 1.0 - float(np.mean(y_deviations))

        # Analyze radial arrangement
        radial_arrangement = 0.0
        if len(centers) > 2:
            # Find the center point (might be one of the shapes or the average)
            center_x = float(np.mean(x_coords))
            center_y = float(np.mean(y_coords))
            
            # Calculate distances and angles from center
            distances = [np.sqrt((x - center_x)**2 + (y - center_y)**2) 
                        for x, y in centers]
            angles = [np.arctan2(y - center_y, x - center_x) 
                     for x, y in centers]
            
            # Convert angles to degrees and normalize to [0, 360)
            angles = np.array([np.degrees(a) % 360 for a in angles])
            angles.sort()
            
            # Calculate angle differences
            angle_diffs = np.diff(angles)
            # Add the difference between last and first angle to complete the circle
            if len(angles) > 1:
                angle_diffs = np.append(angle_diffs, 360 - (angles[-1] - angles[0]))
            
            # Calculate expected angle difference for uniform distribution
            expected_angle = 360.0 / len(centers)
            
            # Calculate angle uniformity based on deviation from expected angle
            angle_deviations = [abs(diff - expected_angle) / expected_angle 
                              for diff in angle_diffs]
            angle_uniformity = 1.0 - float(np.mean(angle_deviations))
            
            # Calculate distance uniformity
            dist_mean = float(np.mean(distances))
            dist_uniformity = 1.0 - float(np.std(distances)) / dist_mean if dist_mean > 0 else 0.0
            
            # Weight angle uniformity more heavily for radial arrangements
            radial_arrangement = (0.95 * angle_uniformity + 0.05 * dist_uniformity)

        # Calculate grid pattern score
        grid_pattern = min(vertical_alignment, horizontal_alignment)

        # Determine chart type based on shapes and arrangement
        chart_type = None
        if "segment" in shape_types or ("circle" in shape_types and radial_arrangement > 0.7):
            chart_type = "pie"
        elif "rectangle" in shape_types and vertical_alignment > 0.7:
            chart_type = "bar"
        elif "point" in shape_types and len([t for t in shape_types if t == "point"]) > 2:
            chart_type = "line"

        return {
            "analysis": {
                "vertical_alignment": vertical_alignment,
                "horizontal_alignment": horizontal_alignment,
                "radial_arrangement": radial_arrangement,
                "grid_pattern": grid_pattern
            },
            "type": chart_type
        }

    def detect(self, image: np.ndarray) -> Dict[str, Any]:
        """Main detection method with enhanced chart analysis."""
        try:
            processed = self.preprocess_image(image)
            shapes, shape_types, shape_features = self._detect_shapes_internal(processed)
            
            # Calculate overall confidence
            if shapes:
                confidences = [
                    features["solidity"] * features["extent"]
                    for features in shape_features
                ]
                confidence = float(np.mean(confidences))
            else:
                confidence = 0.0

            # Analyze structure and determine chart type
            structure_analysis = self.analyze_chart_structure(shapes, shape_types)
            
            result = {
                "success": bool(len(shapes) > 0 and confidence >= self.min_confidence),
                "shape_count": len(shapes),
                "shape_types": shape_types,
                "shapes": shapes,
                "features": shape_features,
                "confidence": confidence,
                "type": structure_analysis["type"],
                "details": structure_analysis
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
                "confidence": 0.0,
                "type": None,
                "details": {
                    "analysis": {
                        "vertical_alignment": 0.0,
                        "horizontal_alignment": 0.0,
                        "radial_arrangement": 0.0,
                        "grid_pattern": 0.0
                    },
                    "type": None
                },
                "error": str(e)
            }
