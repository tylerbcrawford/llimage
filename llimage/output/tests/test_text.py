"""
Tests for text output formatter.
"""

import pytest
from datetime import datetime
from llimage.output.text import TextFormatter

@pytest.fixture
def sample_detection_result():
    """Create a sample detection result for testing."""
    return {
        "success": True,
        "shape_count": 2,
        "shape_types": ["rectangle", "rectangle"],
        "shapes": [
            [[100, 200], [150, 200], [150, 300], [100, 300]],  # First rectangle
            [[200, 150], [250, 150], [250, 300], [200, 300]]   # Second rectangle
        ],
        "features": [
            {
                "area": 15000.0,
                "perimeter": 500.0,
                "bounding_box": (100, 200, 50, 100),
                "center": (125, 250),
                "solidity": 0.95,
                "aspect_ratio": 0.5,
                "extent": 0.98,
                "circularity": 0.85,
                "vertices": 4
            },
            {
                "area": 18750.0,
                "perimeter": 550.0,
                "bounding_box": (200, 150, 50, 150),
                "center": (225, 225),
                "solidity": 0.96,
                "aspect_ratio": 0.33,
                "extent": 0.97,
                "circularity": 0.82,
                "vertices": 4
            }
        ]
    }

def test_formatter_initialization():
    """Test TextFormatter initialization with default config."""
    formatter = TextFormatter()
    assert formatter.detail_level == "standard"
    assert formatter.include_metadata is True
    assert formatter.include_measurements is True
    assert formatter.include_confidence is True

def test_formatter_custom_config():
    """Test TextFormatter initialization with custom config."""
    config = {
        "detail_level": "detailed",
        "include_metadata": False,
        "include_measurements": False,
        "include_confidence": False
    }
    formatter = TextFormatter(config)
    assert formatter.detail_level == "detailed"
    assert formatter.include_metadata is False
    assert formatter.include_measurements is False
    assert formatter.include_confidence is False

def test_basic_formatting(sample_detection_result):
    """Test basic text formatting with minimal configuration."""
    formatter = TextFormatter({
        "include_metadata": False,
        "include_measurements": False,
        "include_confidence": False
    })
    result = formatter.format_result(sample_detection_result)
    
    # Check basic content
    assert "Chart Analysis" in result
    assert "Bar Chart with 2 bars" in result
    assert "Total Shapes Detected: 2" in result
    assert "Shape 1: Rectangle" in result
    assert "Shape 2: Rectangle" in result
    
    # Check that disabled sections are not included
    assert "Analysis Time:" not in result
    assert "square pixels" not in result
    assert "Confidence Scores:" not in result

def test_detailed_formatting(sample_detection_result):
    """Test detailed text formatting with all features enabled."""
    formatter = TextFormatter({
        "detail_level": "detailed",
        "include_metadata": True,
        "include_measurements": True,
        "include_confidence": True
    })
    result = formatter.format_result(sample_detection_result)
    
    # Check metadata
    assert "Analysis Time:" in result
    assert "Detail Level:" in result
    
    # Check measurements
    assert "Dimensions:" in result
    assert "Area:" in result
    assert "square pixels" in result
    
    # Check confidence scores
    assert "Confidence Scores:" in result
    assert "Solidity:" in result
    assert "Circularity:" in result
    assert "Extent:" in result

def test_error_handling():
    """Test error handling in text formatting."""
    formatter = TextFormatter()
    result = formatter.format_result({
        "success": False,
        "shape_count": 0,
        "error": "Test error message"
    })
    
    assert "Error Information" in result
    assert "Test error message" in result
    assert "Processing Status: Failed" in result

def test_chart_type_descriptions():
    """Test different chart type descriptions."""
    formatter = TextFormatter({"include_metadata": False})
    
    # Test bar chart
    result = formatter.format_result({
        "success": True,
        "shape_count": 3,
        "shape_types": ["rectangle", "rectangle", "rectangle"],
        "shapes": [],
        "features": []
    })
    assert "Bar Chart with 3 bars" in result
    
    # Test pie chart
    result = formatter.format_result({
        "success": True,
        "shape_count": 4,
        "shape_types": ["segment", "segment", "segment", "segment"],
        "shapes": [],
        "features": []
    })
    assert "Pie Chart with 4 segments" in result
    
    # Test line chart
    result = formatter.format_result({
        "success": True,
        "shape_count": 5,
        "shape_types": ["point", "point", "point", "point", "point"],
        "shapes": [],
        "features": []
    })
    assert "Line Chart with 5 data points" in result

def test_shape_specific_measurements(sample_detection_result):
    """Test shape-specific measurement formatting."""
    formatter = TextFormatter({"include_metadata": False})
    
    # Test circle measurements
    circle_result = {
        **sample_detection_result,
        "shape_types": ["circle"],
        "shape_count": 1,
        "shapes": [sample_detection_result["shapes"][0]],
        "features": [sample_detection_result["features"][0]]
    }
    result = formatter.format_result(circle_result)
    assert "Estimated Radius:" in result
    
    # Test pie segment measurements
    segment_result = {
        **sample_detection_result,
        "shape_types": ["segment"],
        "shape_count": 1,
        "shapes": [sample_detection_result["shapes"][0]],
        "features": [{
            **sample_detection_result["features"][0],
            "arc_score": 0.85
        }]
    }
    result = formatter.format_result(segment_result)
    assert "Arc Score:" in result
