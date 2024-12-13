"""
Text output formatter for chart detection results.
"""

import logging
from typing import Any, Dict, List, Optional
from datetime import datetime

logger = logging.getLogger(__name__)

class TextFormatter:
    """Formats chart detection results as human-readable text."""

    def __init__(self, config: Optional[Dict] = None):
        """Initialize the text formatter with configuration.
        
        Args:
            config: Optional configuration dictionary with settings like:
                - detail_level: str ('minimal', 'standard', 'detailed')
                - include_metadata: bool
                - include_measurements: bool
                - include_confidence: bool
        """
        self.config = config or {}
        self.detail_level = self.config.get('detail_level', 'standard')
        self.include_metadata = self.config.get('include_metadata', True)
        self.include_measurements = self.config.get('include_measurements', True)
        self.include_confidence = self.config.get('include_confidence', True)
        
        logger.info(f"Initialized TextFormatter with detail level: {self.detail_level}")

    def _format_metadata(self) -> str:
        """Create metadata section of the output."""
        return (
            f"Analysis Time: {datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S UTC')}\n"
            f"Detail Level: {self.detail_level}\n"
        )

    def _format_shape_description(self, shape_type: str, features: Dict[str, Any],
                                index: int) -> str:
        """Format a description of a single shape.
        
        Args:
            shape_type: Type of the shape (e.g., 'rectangle', 'circle')
            features: Shape features dictionary
            index: Shape index number
        
        Returns:
            Formatted shape description
        """
        # Basic shape information
        x, y, w, h = features["bounding_box"]
        description = [f"Shape {index + 1}: {shape_type.capitalize()}"]
        description.append(f"Location: ({x}, {y})")
        
        # Add measurements if enabled
        if self.include_measurements:
            description.extend([
                f"Dimensions: {w}x{h} pixels",
                f"Area: {features['area']:.1f} square pixels"
            ])
            
            # Add shape-specific measurements
            if shape_type == "circle":
                description.append(
                    f"Estimated Radius: {(features['area'] / 3.14159)**0.5:.1f} pixels"
                )
            elif shape_type == "segment":
                description.append(
                    f"Arc Score: {features['arc_score']:.2f}"
                )
        
        # Add confidence scores if enabled
        if self.include_confidence:
            confidence_scores = [
                f"Solidity: {features['solidity']:.2f}",
                f"Circularity: {features['circularity']:.2f}",
                f"Extent: {features['extent']:.2f}"
            ]
            description.append("Confidence Scores:")
            description.extend(f"  - {score}" for score in confidence_scores)
        
        return "\n".join(description)

    def _infer_chart_description(self, shape_types: List[str]) -> str:
        """Create a description of the overall chart type.
        
        Args:
            shape_types: List of detected shape types
        
        Returns:
            Chart description string
        """
        # Count shape types
        type_counts = {}
        for shape_type in shape_types:
            type_counts[shape_type] = type_counts.get(shape_type, 0) + 1
        
        # Generate description based on shape combinations
        if "segment" in type_counts:
            return (f"Pie Chart with {type_counts['segment']} segments")
        elif "rectangle" in type_counts and type_counts["rectangle"] > 1:
            return (f"Bar Chart with {type_counts['rectangle']} bars")
        elif "point" in type_counts and type_counts["point"] > 2:
            return (f"Line Chart with {type_counts['point']} data points")
        elif "circle" in type_counts and type_counts["circle"] == 1:
            return "Empty or unprocessed Pie Chart"
        
        return "Unrecognized Chart Type"

    def format_result(self, detection_result: Dict[str, Any]) -> str:
        """Format chart detection results as human-readable text.
        
        Args:
            detection_result: Dictionary containing detection results
        
        Returns:
            Formatted text string
        """
        try:
            output = []
            
            # Add metadata if enabled
            if self.include_metadata:
                output.append("=== Analysis Metadata ===")
                output.append(self._format_metadata())
            
            # Add error information if present
            if not detection_result["success"] or "error" in detection_result:
                output.append("=== Error Information ===")
                output.append(detection_result.get("error", "Unknown error occurred"))
                output.append("\n=== Analysis Summary ===")
                output.append("Processing Status: Failed")
                output.append(f"Total Elements: {detection_result['shape_count']}")
                return "\n".join(output)
            
            # Add chart type inference
            if detection_result["shape_count"] > 0:
                output.append("=== Chart Analysis ===")
                output.append(
                    self._infer_chart_description(detection_result["shape_types"])
                )
                output.append(f"Total Shapes Detected: {detection_result['shape_count']}")
            
            # Add shape details based on detail level
            if detection_result["shape_count"] > 0:
                output.append("\n=== Shape Details ===")
                for i, (shape_type, features) in enumerate(
                    zip(detection_result["shape_types"],
                        detection_result["features"])
                ):
                    output.append("")  # Add spacing between shapes
                    output.append(
                        self._format_shape_description(shape_type, features, i)
                    )
            
            # Add summary
            output.extend([
                "",
                "=== Analysis Summary ===",
                f"Processing Status: {'Successful' if detection_result['success'] else 'Failed'}",
                f"Total Elements: {detection_result['shape_count']}"
            ])
            
            return "\n".join(output)

        except Exception as e:
            logger.error(f"Error formatting text output: {str(e)}")
            error_output = [
                "=== Error Information ===",
                f"Text formatting error: {str(e)}",
                "\n=== Analysis Summary ===",
                "Processing Status: Failed",
                "Total Elements: 0"
            ]
            return "\n".join(error_output)
