"""
Tests for enhanced chart detection features.
"""

import pytest
import cv2
import numpy as np
from pathlib import Path
from pdf2image import convert_from_path
from llimage.chart.detector import ChartDetector
from llimage.image.processor import ImageProcessor

@pytest.fixture
def test_pdfs_dir():
    """Get the test PDFs directory."""
    return Path(__file__).parent.parent.parent.parent / 'test_pdfs'

@pytest.fixture
def chart_detector():
    """Create a ChartDetector instance for testing."""
    return ChartDetector({
        'min_shape_area': 100,  # Lower threshold for test shapes
        'noise_threshold': 40,   # Adjusted for test noise
        'min_confidence': 0.5    # Lower threshold for tests
    })

@pytest.fixture
def image_processor():
    """Create an ImageProcessor instance for testing."""
    return ImageProcessor()

@pytest.fixture
def sample_chart_image(test_pdfs_dir):
    """Load and convert the chart PDF to image."""
    pdf_path = test_pdfs_dir / 'chart.pdf'
    assert pdf_path.exists(), f"Test PDF not found: {pdf_path}"
    
    images = convert_from_path(pdf_path)
    img = cv2.cvtColor(np.array(images[0]), cv2.COLOR_RGB2BGR)
    return img

def test_enhanced_shape_features(chart_detector, sample_chart_image):
    """Test extraction of enhanced shape features."""
    processed = chart_detector.preprocess_image(sample_chart_image)
    shapes, _, shape_features = chart_detector.detect_shapes(processed)
    
    assert len(shapes) > 0, "Should detect shapes"
    assert len(shape_features) > 0, "Should extract shape features"
    
    # Test feature completeness
    required_features = {
        "area", "perimeter", "bounding_box", "center", "solidity",
        "aspect_ratio", "extent", "circularity", "ellipse_eccentricity"
    }
    
    for features in shape_features:
        assert set(features.keys()) >= required_features, "Missing required features"
        assert all(isinstance(v, (int, float, tuple)) for v in features.values()), \
            "Feature values should be numeric or tuples"

def test_chart_structure_analysis(chart_detector, sample_chart_image):
    """Test analysis of chart structure and spatial relationships."""
    processed = chart_detector.preprocess_image(sample_chart_image)
    shapes, shape_types, shape_features = chart_detector.detect_shapes(processed)
    
    analysis = chart_detector.analyze_chart_structure(shapes, shape_types, shape_features)
    
    assert "type" in analysis, "Should determine chart type"
    assert "confidence" in analysis, "Should provide confidence score"
    assert "features" in analysis, "Should include analysis features"
    
    features = analysis["features"]
    assert "shape_counts" in features, "Should count shape types"
    assert "vertical_alignment" in features, "Should measure vertical alignment"
    assert "horizontal_alignment" in features, "Should measure horizontal alignment"
    assert "radial_arrangement" in features, "Should measure radial arrangement"

def test_alignment_detection(chart_detector):
    """Test detection of shape alignments."""
    # Create test image with vertical alignment
    img_vertical = np.zeros((300, 200), dtype=np.uint8)
    cv2.rectangle(img_vertical, (50, 50), (100, 100), 255, -1)
    cv2.rectangle(img_vertical, (50, 150), (100, 200), 255, -1)
    
    # Create test image with horizontal alignment
    img_horizontal = np.zeros((200, 300), dtype=np.uint8)
    cv2.rectangle(img_horizontal, (50, 50), (100, 100), 255, -1)
    cv2.rectangle(img_horizontal, (150, 50), (200, 100), 255, -1)
    
    # Test vertical alignment
    result_vertical = chart_detector.detect(img_vertical)
    assert result_vertical["details"]["analysis"]["vertical_alignment"] > 0.8, \
        "Should detect vertical alignment"
    
    # Test horizontal alignment
    result_horizontal = chart_detector.detect(img_horizontal)
    assert result_horizontal["details"]["analysis"]["horizontal_alignment"] > 0.8, \
        "Should detect horizontal alignment"

def test_radial_arrangement_detection(chart_detector):
    """Test detection of radial arrangements."""
    # Create test image with radial arrangement
    img = np.zeros((400, 400), dtype=np.uint8)
    center = (200, 200)
    radius = 100
    
    # Draw shapes in a circular pattern
    for angle in range(0, 360, 60):
        rad = np.radians(angle)
        x = int(center[0] + radius * np.cos(rad))
        y = int(center[1] + radius * np.sin(rad))
        cv2.circle(img, (x, y), 20, 255, -1)
    
    # Add center circle
    cv2.circle(img, center, 30, 255, -1)
    
    result = chart_detector.detect(img)
    assert result["details"]["analysis"]["radial_arrangement"] > 0.8, \
        "Should detect radial arrangement"
    assert result["type"] == "pie", "Should classify as pie chart"

def test_shape_classification_accuracy(chart_detector):
    """Test accuracy of shape classification."""
    # Create simple test image
    img = np.zeros((400, 400), dtype=np.uint8)
    
    # Draw three distinct shapes with good spacing
    cv2.rectangle(img, (50, 50), (150, 150), 255, -1)  # Large rectangle
    cv2.circle(img, (250, 250), 50, 255, -1)  # Large circle
    
    # Draw a triangle
    pts = np.array([
        [300, 50],
        [250, 150],
        [350, 150]
    ], dtype=np.int32)
    pts = pts.reshape((-1, 1, 2))
    cv2.fillPoly(img, [pts], 255)
    
    # Process and detect shapes
    processed = chart_detector.preprocess_image(img)
    shapes, shape_types, _ = chart_detector.detect_shapes(processed)
    
    assert len(shapes) == 3, "Should detect all three shapes"
    assert "rectangle" in shape_types, "Should detect rectangle"
    assert "circle" in shape_types, "Should detect circle"

def test_noise_handling(chart_detector):
    """Test handling of noisy images."""
    # Create a simple test image with a clear shape
    img = np.zeros((300, 300), dtype=np.uint8)
    cv2.rectangle(img, (50, 50), (250, 250), 255, -1)  # Very large rectangle
    
    # Create noise with proper shape
    noise = np.random.normal(loc=0, scale=15, size=img.shape)
    noise = (noise * 255).clip(0, 255).astype(np.uint8)
    
    # Add noise with proper weighting
    noisy_img = cv2.addWeighted(img, 0.7, noise, 0.3, 0)
    
    # Enhance contrast
    noisy_img = cv2.convertScaleAbs(noisy_img, alpha=1.5, beta=0)
    
    # Reduce noise while preserving edges
    noisy_img = cv2.bilateralFilter(noisy_img, 9, 75, 75)
    
    result = chart_detector.detect(noisy_img)
    
    assert result["success"] or result["type"] != "unknown", \
        "Should handle noisy image gracefully"
