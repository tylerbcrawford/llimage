"""
Tests for JSON output formatter.
"""

import pytest
import json
from datetime import datetime
from llimage.output.json import JsonFormatter

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
    """Test JsonFormatter initialization with default config."""
    formatter = JsonFormatter()
    assert formatter.detail_level == "standard"
    assert formatter.include_metadata is True
    assert formatter.include_confidence is True
    assert formatter.include_features is False
    assert formatter.pretty_print is True

def test_formatter_custom_config():
    """Test JsonFormatter initialization with custom config."""
    config = {
        "detail_level": "detailed",
        "include_metadata": False,
        "include_confidence": False,
        "include_features": True,
        "pretty_print": False
    }
    formatter = JsonFormatter(config)
    assert formatter.detail_level == "detailed"
    assert formatter.include_metadata is False
    assert formatter.include_confidence is False
    assert formatter.include_features is True
    assert formatter.pretty_print is False

def test_basic_formatting(sample_detection_result):
    """Test basic JSON formatting with minimal configuration."""
    formatter = JsonFormatter({
        "include_metadata": False,
        "include_confidence": False,
        "include_features": False
    })
    result = formatter.format_result(sample_detection_result)
    data = json.loads(result)
    
    assert data["success"] is True
    assert data["shape_count"] == 2
    assert len(data["shapes"]) == 2
    assert "chart_type" in data
    assert data["chart_type"] == "bar_chart"

def test_detailed_formatting(sample_detection_result):
    """Test detailed JSON formatting with all features enabled."""
    formatter = JsonFormatter({
        "detail_level": "detailed",
        "include_metadata": True,
        "include_confidence": True,
        "include_features": True
    })
    result = formatter.format_result(sample_detection_result)
    data = json.loads(result)
    
    # Check metadata
    assert "metadata" in data
    assert "timestamp" in data["metadata"]
    assert "formatter_version" in data["metadata"]
    assert "detail_level" in data["metadata"]
    
    # Check shape details
    shape = data["shapes"][0]
    assert "type" in shape
    assert "bounds" in shape
    assert "confidence_scores" in shape
    assert "features" in shape
    
    # Check specific feature values
    features = shape["features"]
    assert "area" in features
    assert "perimeter" in features
    assert "aspect_ratio" in features
    assert "vertices" in features
    assert "center" in features

def test_error_handling():
    """Test error handling in JSON formatting."""
    formatter = JsonFormatter()
    result = formatter.format_result({
        "success": False,
        "shape_count": 0,
        "error": "Test error message"
    })
    data = json.loads(result)
    
    assert data["success"] is False
    assert "error" in data
    assert data["error"] == "Test error message"

def test_chart_type_inference(sample_detection_result):
    """Test chart type inference for different shape combinations."""
    formatter = JsonFormatter()
    
    # Test bar chart detection
    result = formatter.format_result(sample_detection_result)
    data = json.loads(result)
    assert data["chart_type"] == "bar_chart"
    
    # Test pie chart detection
    pie_result = {
        **sample_detection_result,
        "shape_types": ["segment", "segment", "segment"],
        "shape_count": 3
    }
    result = formatter.format_result(pie_result)
    data = json.loads(result)
    assert data["chart_type"] == "pie_chart"
    
    # Test line chart detection
    line_result = {
        **sample_detection_result,
        "shape_types": ["point", "point", "point", "point"],
        "shape_count": 4
    }
    result = formatter.format_result(line_result)
    data = json.loads(result)
    assert data["chart_type"] == "line_chart"

def test_serialization_options():
    """Test different serialization options."""
    formatter = JsonFormatter({"pretty_print": True})
    result = formatter.format_result({
        "success": True,
        "shape_count": 0,
        "shapes": [],
        "shape_types": [],
        "features": []
    })
    # Pretty printed JSON should have newlines
    assert "\n" in result
    
    formatter = JsonFormatter({"pretty_print": False})
    result = formatter.format_result({
        "success": True,
        "shape_count": 0,
        "shapes": [],
        "shape_types": [],
        "features": []
    })
    # Non-pretty printed JSON should not have newlines
    assert "\n" not in result
