"""
Tests for the chart detection module.
"""

import pytest
import cv2
import numpy as np
from llimage.chart.detector import ChartDetector

@pytest.fixture
def chart_detector():
    """Create a ChartDetector instance for testing."""
    return ChartDetector()

@pytest.fixture
def sample_bar_chart():
    """Create a simple bar chart image for testing."""
    # Create a white image
    image = np.ones((300, 400), dtype=np.uint8) * 255
    
    # Draw some bars
    cv2.rectangle(image, (50, 200), (100, 250), 0, -1)  # First bar
    cv2.rectangle(image, (150, 150), (200, 250), 0, -1)  # Second bar
    cv2.rectangle(image, (250, 100), (300, 250), 0, -1)  # Third bar
    
    return image

@pytest.fixture
def sample_pie_chart():
    """Create a simple pie chart image for testing."""
    # Create a white image
    image = np.ones((300, 300), dtype=np.uint8) * 255
    
    # Draw a circle
    cv2.circle(image, (150, 150), 100, 0, 2)
    
    # Draw some lines to create pie segments
    cv2.line(image, (150, 150), (250, 150), 0, 2)  # Horizontal line
    cv2.line(image, (150, 150), (150, 50), 0, 2)   # Vertical line
    
    return image

def test_chart_detector_initialization():
    """Test ChartDetector initialization."""
    detector = ChartDetector()
    assert detector is not None
    assert detector.min_confidence == 0.7

def test_preprocess_image(chart_detector, sample_bar_chart):
    """Test image preprocessing."""
    processed = chart_detector.preprocess_image(sample_bar_chart)
    assert processed is not None
    assert processed.shape == sample_bar_chart.shape
    assert processed.dtype == np.uint8

def test_detect_shapes(chart_detector, sample_bar_chart):
    """Test shape detection."""
    processed = chart_detector.preprocess_image(sample_bar_chart)
    shapes, shape_types, _ = chart_detector.detect_shapes(processed)
    
    assert len(shapes) > 0
    assert len(shapes) == len(shape_types)
    assert "rectangle" in shape_types

def test_classify_bar_chart(chart_detector, sample_bar_chart):
    """Test bar chart classification."""
    result = chart_detector.detect(sample_bar_chart)
    
    assert result["success"] is True
    assert result["shape_count"] > 0
    assert "rectangle" in result["shape_types"]

def test_classify_pie_chart(chart_detector, sample_pie_chart):
    """Test pie chart classification."""
    result = chart_detector.detect(sample_pie_chart)
    
    assert result["success"] is True
    assert result["shape_count"] > 0

def test_error_handling(chart_detector):
    """Test error handling with invalid input."""
    # Create an invalid image (wrong type)
    invalid_image = "not an image"
    
    result = chart_detector.detect(invalid_image)
    assert result["success"] is False
    assert result["shape_count"] == 0
    assert "error" in result

def test_confidence_threshold():
    """Test confidence threshold configuration."""
    # Create detector with high confidence threshold
    detector = ChartDetector({"min_confidence": 0.95})
    
    # Create a simple image that might be ambiguous
    image = np.ones((100, 100), dtype=np.uint8) * 255
    cv2.line(image, (0, 0), (100, 100), 0, 2)
    
    result = detector.detect(image)
    assert result["success"] is False  # Should fail due to high confidence threshold
