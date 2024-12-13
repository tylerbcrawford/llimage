"""
JSON output formatter for chart detection results.
"""

import json
import logging
from typing import Any, Dict, List, Optional, Union
from datetime import datetime

logger = logging.getLogger(__name__)

class JsonFormatter:
    """Formats chart detection results as JSON."""

    def __init__(self, config: Optional[Dict] = None):
        """Initialize the JSON formatter with configuration.
        
        Args:
            config: Optional configuration dictionary with settings like:
                - detail_level: str ('minimal', 'standard', 'detailed')
                - include_metadata: bool
                - include_confidence: bool
                - include_features: bool
                - pretty_print: bool
        """
        self.config = config or {}
        self.detail_level = self.config.get('detail_level', 'standard')
        self.include_metadata = self.config.get('include_metadata', True)
        self.include_confidence = self.config.get('include_confidence', True)
        self.include_features = self.config.get('include_features', False)
        self.pretty_print = self.config.get('pretty_print', True)
        
        logger.info(f"Initialized JsonFormatter with detail level: {self.detail_level}")

    def _format_metadata(self) -> Dict[str, Any]:
        """Create metadata section of the output."""
        return {
            "timestamp": datetime.utcnow().isoformat(),
            "formatter_version": "1.0.0",
            "detail_level": self.detail_level
        }

    def _format_shape(self, shape: Any, shape_type: str, 
                     features: Dict[str, Any]) -> Dict[str, Any]:
        """Format a single shape's data.
        
        Args:
            shape: Shape contour data
            shape_type: Type of the shape (e.g., 'rectangle', 'circle')
            features: Shape features dictionary
        
        Returns:
            Dictionary containing formatted shape data
        """
        # Basic shape information
        shape_data = {
            "type": shape_type,
            "bounds": {
                "x": int(features["bounding_box"][0]),
                "y": int(features["bounding_box"][1]),
                "width": int(features["bounding_box"][2]),
                "height": int(features["bounding_box"][3])
            }
        }

        # Add confidence scores if enabled
        if self.include_confidence:
            confidence_scores = {
                "solidity": float(features["solidity"]),
                "circularity": float(features["circularity"]),
                "extent": float(features["extent"])
            }
            shape_data["confidence_scores"] = confidence_scores

        # Add detailed features if enabled
        if self.include_features:
            detailed_features = {
                "area": float(features["area"]),
                "perimeter": float(features["perimeter"]),
                "aspect_ratio": float(features["aspect_ratio"]),
                "vertices": int(features["vertices"]),
                "center": {
                    "x": int(features["center"][0]),
                    "y": int(features["center"][1])
                }
            }
            # Add arc score for potential pie segments
            if "arc_score" in features:
                detailed_features["arc_score"] = float(features["arc_score"])
            
            shape_data["features"] = detailed_features

        return shape_data

    def format_result(self, detection_result: Dict[str, Any]) -> str:
        """Format chart detection results as JSON string.
        
        Args:
            detection_result: Dictionary containing detection results
        
        Returns:
            JSON formatted string
        """
        try:
            # Start with base structure
            output = {
                "success": detection_result["success"],
                "shape_count": detection_result["shape_count"]
            }

            # Add metadata if enabled
            if self.include_metadata:
                output["metadata"] = self._format_metadata()

            # Add error information if present
            if "error" in detection_result:
                output["error"] = str(detection_result["error"])
                return self._serialize(output)

            # Format shapes based on detail level
            shapes_data = []
            for i, (shape, shape_type, features) in enumerate(
                zip(detection_result["shapes"],
                    detection_result["shape_types"],
                    detection_result["features"])
            ):
                shape_data = self._format_shape(shape, shape_type, features)
                shapes_data.append(shape_data)

            # Add shapes to output
            output["shapes"] = shapes_data

            # Add chart type inference if available
            if len(shapes_data) > 0:
                chart_type = self._infer_chart_type(
                    detection_result["shape_types"]
                )
                if chart_type:
                    output["chart_type"] = chart_type

            return self._serialize(output)

        except Exception as e:
            logger.error(f"Error formatting JSON output: {str(e)}")
            error_output = {
                "success": False,
                "error": f"JSON formatting error: {str(e)}"
            }
            if self.include_metadata:
                error_output["metadata"] = self._format_metadata()
            return self._serialize(error_output)

    def _infer_chart_type(self, shape_types: List[str]) -> Optional[str]:
        """Infer the overall chart type based on detected shapes.
        
        Args:
            shape_types: List of detected shape types
        
        Returns:
            Inferred chart type or None if undetermined
        """
        # Count shape types
        type_counts = {}
        for shape_type in shape_types:
            type_counts[shape_type] = type_counts.get(shape_type, 0) + 1

        # Inference rules
        if "segment" in type_counts:
            return "pie_chart"
        elif "rectangle" in type_counts and type_counts["rectangle"] > 1:
            return "bar_chart"
        elif "point" in type_counts and type_counts["point"] > 2:
            return "line_chart"
        elif "circle" in type_counts and type_counts["circle"] == 1:
            return "pie_chart"  # Empty or unprocessed pie chart
        
        return None

    def _serialize(self, data: Dict[str, Any]) -> str:
        """Serialize data to JSON string.
        
        Args:
            data: Dictionary to serialize
        
        Returns:
            JSON formatted string
        """
        if self.pretty_print:
            return json.dumps(data, indent=2, sort_keys=True)
        return json.dumps(data, sort_keys=True)
