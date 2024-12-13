"""
Chart data extraction module for extracting numerical data and labels from detected charts.
"""

import cv2
import numpy as np
from typing import Dict, List, Optional, Tuple, Any
import logging

logger = logging.getLogger(__name__)

class ChartDataExtractor:
    """Extracts data from detected charts."""

    def __init__(self, config: Optional[Dict] = None):
        """Initialize the chart data extractor."""
        self.config = config or {}
        self.min_text_area = self.config.get('min_text_area', 50)
        self.text_detection_threshold = self.config.get('text_detection_threshold', 0.5)
        logger.info("Initializing ChartDataExtractor")

    def extract_data(self, image: np.ndarray, chart_type: str, 
                    shapes: List[np.ndarray], features: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Extract data from a chart based on its type."""
        try:
            if not shapes:
                return {
                    "success": False,
                    "error": "No shapes detected",
                    "type": chart_type,
                    "data": {}
                }

            if chart_type == "bar":
                data = self._extract_bar_chart_data(image, shapes, features)
            elif chart_type == "pie":
                data = self._extract_pie_chart_data(image, shapes, features)
            elif chart_type == "line":
                data = self._extract_line_chart_data(image, shapes, features)
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

    def _extract_bar_chart_data(self, image: np.ndarray, shapes: List[np.ndarray], 
                              features: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Extract data from a bar chart."""
        # Get image dimensions
        height, width = image.shape[:2]
        
        # Sort shapes by x-coordinate (left to right)
        shapes_with_features = list(zip(shapes, features))
        shapes_with_features.sort(key=lambda x: x[1]["center"][0])
        
        # Extract bar data
        bars = []
        for shape, feature in shapes_with_features:
            x, y, w, h = feature["bounding_box"]
            bar_height = height - y  # Height from bottom
            
            bar_data = {
                "x": x,
                "width": w,
                "height": bar_height,
                "center": feature["center"],
                "area": feature["area"]
            }
            bars.append(bar_data)
        
        return {
            "bars": bars,
            "count": len(bars)
        }

    def _extract_pie_chart_data(self, image: np.ndarray, shapes: List[np.ndarray], 
                               features: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Extract data from a pie chart."""
        # Calculate center as average of all shape centers
        centers = [feature["center"] for feature in features]
        center_x = int(np.mean([x for x, _ in centers]))
        center_y = int(np.mean([y for _, y in centers]))
        
        # Extract segment data
        segments = []
        total_area = sum(feature["area"] for feature in features)
        
        for shape, feature in zip(shapes, features):
            # Calculate angle from center to shape center
            cx, cy = feature["center"]
            angle = np.degrees(np.arctan2(cy - center_y, cx - center_x)) % 360
            
            segment_data = {
                "angle": angle,
                "area": feature["area"],
                "center": (cx, cy),
                "percentage": (feature["area"] / total_area) * 100
            }
            segments.append(segment_data)
        
        # Sort segments by angle
        segments.sort(key=lambda x: x["angle"])
        
        return {
            "segments": segments,
            "count": len(segments),
            "center": (center_x, center_y)
        }

    def _extract_line_chart_data(self, image: np.ndarray, shapes: List[np.ndarray], 
                                features: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Extract data from a line chart."""
        # Extract point data
        points = []
        for shape, feature in zip(shapes, features):
            x, y = feature["center"]
            point_data = {
                "x": x,
                "y": y,
                "area": feature["area"]
            }
            points.append(point_data)
        
        # Sort points by x-coordinate
        points.sort(key=lambda x: x["x"])
        
        return {
            "points": points,
            "count": len(points)
        }
