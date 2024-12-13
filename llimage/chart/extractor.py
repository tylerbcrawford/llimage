"""
Data extraction module for chart analysis.
"""

import logging
import cv2
import numpy as np
from typing import Dict, List, Any, Optional, Tuple

logger = logging.getLogger(__name__)

class ChartDataExtractor:
    """Extracts data from detected charts."""

    def __init__(self, config: Optional[Dict] = None):
        """Initialize the data extractor with configuration."""
        self.config = config or {}
        logger.info("Initializing ChartDataExtractor")

    def extract_data(self, image: np.ndarray, chart_type: str,
                    shapes: List[np.ndarray],
                    features: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Extract data from detected chart shapes."""
        if not shapes or not features:
            return {
                "success": False,
                "error": "No shapes detected",
                "type": chart_type,
                "data": {}
            }

        try:
            if chart_type == "bar":
                data = self._extract_bar_data(shapes, features)
            elif chart_type == "line":
                data = self._extract_line_data(shapes, features)
            elif chart_type == "pie":
                data = self._extract_pie_data(shapes, features)
            else:
                return {
                    "success": False,
                    "error": f"Unsupported chart type: {chart_type}",
                    "type": chart_type,
                    "data": {}
                }

            return {
                "success": True,
                "type": chart_type,
                "data": data
            }

        except Exception as e:
            logger.error(f"Error extracting data: {str(e)}")
            return {
                "success": False,
                "error": str(e),
                "type": chart_type,
                "data": {}
            }

    def _extract_bar_data(self, shapes: List[np.ndarray],
                         features: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Extract data from bar chart shapes."""
        bars = []
        for shape, feature in zip(shapes, features):
            if feature.get("vertices", 0) == 4:  # Rectangle
                x, y, w, h = [int(v) for v in feature["bounding_box"]]
                bars.append({
                    "x": x,
                    "width": w,
                    "height": h,
                    "area": float(feature["area"])
                })

        # Sort bars by x-coordinate
        bars.sort(key=lambda b: b["x"])

        return {
            "type": "bar",
            "bars": bars
        }

    def _extract_line_data(self, shapes: List[np.ndarray],
                          features: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Extract data from line chart shapes."""
        points = []
        for shape, feature in zip(shapes, features):
            # Match detector's point detection criteria
            area = feature.get("area", 0)
            solidity = feature.get("solidity", 0)
            circularity = feature.get("circularity", 0)
            vertices = feature.get("vertices", 0)
            extent = feature.get("extent", 0)

            # Point detection criteria matching detector
            if area < 1000 and solidity > 0.9:
                if (circularity > 0.45 or  # High circularity
                    (vertices >= 5 and vertices <= 8 and extent > 0.6) or  # Octagonal-like
                    (area < 400 and extent > 0.6 and solidity > 0.95) or  # Small, solid points
                    (solidity > 0.95 and extent > 0.7) or  # Very solid and well-filled
                    (circularity > 0.4 and extent > 0.65 and solidity > 0.95) or  # Combined criteria
                    (area < 400 and solidity > 0.95 and extent > 0.65) or  # Small area with good extent
                    (area < 500 and vertices <= 6 and solidity > 0.95)):  # Small with few vertices
                    cx, cy = [int(v) for v in feature["center"]]
                    points.append({
                        "x": cx,
                        "y": cy,
                        "size": float(feature["area"])
                    })

        # Sort points by x-coordinate
        points.sort(key=lambda p: p["x"])

        return {
            "type": "line",
            "points": points
        }

    def _extract_pie_data(self, shapes: List[np.ndarray],
                         features: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Extract data from pie chart shapes."""
        segments = []
        total_area = 0
        center_x = 0
        center_y = 0
        
        # First pass: calculate total area and average center
        for shape, feature in zip(shapes, features):
            if feature.get("arc_score", 0) > 0.3:  # Segment
                area = float(feature["area"])
                cx, cy = [int(v) for v in feature["center"]]
                total_area += area
                center_x += cx * area
                center_y += cy * area

        # Calculate weighted center
        if total_area > 0:
            center_x = int(center_x / total_area)
            center_y = int(center_y / total_area)
        elif shapes:
            # Fallback: use average of segment centers
            centers = [feature["center"] for feature in features]
            center_x = int(sum(x for x, _ in centers) / len(centers))
            center_y = int(sum(y for _, y in centers) / len(centers))

        # Second pass: calculate angles and percentages
        for shape, feature in zip(shapes, features):
            if feature.get("arc_score", 0) > 0.3:  # Segment
                # Calculate angle from center to segment center
                cx, cy = [int(v) for v in feature["center"]]
                dx = cx - center_x
                dy = cy - center_y
                angle = np.degrees(np.arctan2(dy, dx)) % 360
                
                # Calculate percentage
                percentage = (feature["area"] / total_area * 100) if total_area > 0 else 0
                
                segments.append({
                    "center": [cx, cy],
                    "area": float(feature["area"]),
                    "percentage": float(percentage),
                    "angle": float(angle),
                    "arc_score": float(feature["arc_score"])
                })

        # Sort segments by angle
        segments.sort(key=lambda s: s["angle"])

        return {
            "type": "pie",
            "center": [center_x, center_y],
            "segments": segments,
            "total_area": total_area
        }

    def draw_debug_visualization(self, image: np.ndarray,
                               chart_type: str,
                               data: Dict[str, Any]) -> np.ndarray:
        """Draw debug visualization of extracted data."""
        debug_img = image.copy()

        if chart_type == "bar":
            for bar in data.get("bars", []):
                x = int(bar["x"])
                w = int(bar["width"])
                h = int(bar["height"])
                y = image.shape[0] - h  # Assuming height from bottom
                cv2.rectangle(debug_img, (x, y), (x + w, image.shape[0]), (128, 128, 128), 2)
                cv2.putText(debug_img, f"H:{h}", (x, y-10),
                           cv2.FONT_HERSHEY_SIMPLEX, 0.5, (128, 128, 128), 1)

        elif chart_type == "line":
            points = data.get("points", [])
            for i in range(len(points) - 1):
                p1 = (int(points[i]["x"]), int(points[i]["y"]))
                p2 = (int(points[i+1]["x"]), int(points[i+1]["y"]))
                cv2.line(debug_img, p1, p2, (128, 128, 128), 2)
                cv2.circle(debug_img, p1, 5, (64, 64, 64), -1)
                cv2.putText(debug_img, f"({p1[0]},{p1[1]})",
                           (p1[0]-30, p1[1]-10), cv2.FONT_HERSHEY_SIMPLEX,
                           0.4, (128, 128, 128), 1)
            if points:
                last = points[-1]
                last_point = (int(last["x"]), int(last["y"]))
                cv2.circle(debug_img, last_point, 5, (64, 64, 64), -1)
                cv2.putText(debug_img, f"({last_point[0]},{last_point[1]})",
                           (last_point[0]-30, last_point[1]-10),
                           cv2.FONT_HERSHEY_SIMPLEX, 0.4, (128, 128, 128), 1)

        elif chart_type == "pie":
            if "center" in data:
                center = tuple(int(v) for v in data["center"])
                cv2.circle(debug_img, center, 5, (128, 128, 128), -1)
                for segment in data.get("segments", []):
                    angle_rad = np.radians(segment["angle"])
                    radius = 170  # Fixed radius for visualization
                    end_x = int(center[0] + radius * np.cos(angle_rad))
                    end_y = int(center[1] + radius * np.sin(angle_rad))
                    cv2.line(debug_img, center, (end_x, end_y), (128, 128, 128), 1)
                    
                    # Draw percentage
                    text_radius = radius - 30
                    text_x = int(center[0] + text_radius * np.cos(angle_rad))
                    text_y = int(center[1] + text_radius * np.sin(angle_rad))
                    cv2.putText(debug_img, f"{segment['percentage']:.1f}%",
                              (text_x, text_y), cv2.FONT_HERSHEY_SIMPLEX,
                              0.5, (128, 128, 128), 1)

        return debug_img
