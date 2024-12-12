"""
Tests for chart detection using real chart PDFs.
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
    return ChartDetector()

@pytest.fixture
def image_processor():
    """Create an ImageProcessor instance for testing."""
    return ImageProcessor()

@pytest.fixture
def sample_chart_image(test_pdfs_dir):
    """Load and convert the chart PDF to image."""
    pdf_path = test_pdfs_dir / 'chart.pdf'
    assert pdf_path.exists(), f"Test PDF not found: {pdf_path}"
    
    # Convert first page of PDF to image
    images = convert_from_path(pdf_path)
    # Convert PIL image to OpenCV format
    img = cv2.cvtColor(np.array(images[0]), cv2.COLOR_RGB2BGR)
    return img

def test_chart_detection_pipeline(chart_detector, image_processor, sample_chart_image):
    """Test the complete chart detection pipeline with a real chart."""
    # Process the image
    processed_image = image_processor.preprocess(sample_chart_image)
    
    # Detect chart type
    result = chart_detector.detect(processed_image)
    
    # Verify detection
    assert result["success"], "Chart detection should succeed"
    assert result["type"] in ["bar", "line", "pie"], f"Unexpected chart type: {result['type']}"
    assert result["confidence"] >= 0.7, "Confidence should be at least 0.7"

def test_shape_detection_real_chart(chart_detector, image_processor, sample_chart_image):
    """Test shape detection on real chart."""
    # Process the image
    processed_image = image_processor.preprocess(sample_chart_image)
    
    # Detect shapes
    shapes, shape_types = chart_detector.detect_shapes(processed_image)
    
    # Verify shapes were detected
    assert len(shapes) > 0, "Should detect shapes in the chart"
    assert len(shape_types) > 0, "Should identify shape types"

def test_text_region_detection_real_chart(image_processor, sample_chart_image):
    """Test text region detection on real chart."""
    # Detect text regions
    text_regions = image_processor.detect_text_regions(sample_chart_image)
    
    # Verify text regions were detected
    assert len(text_regions) > 0, "Should detect text regions in the chart"
    
    # Verify text region properties
    for x, y, w, h in text_regions:
        assert w > 0 and h > 0, "Text regions should have positive dimensions"
        assert 0 <= x < sample_chart_image.shape[1], "X coordinate should be within image bounds"
        assert 0 <= y < sample_chart_image.shape[0], "Y coordinate should be within image bounds"

def test_feature_extraction_real_chart(image_processor, sample_chart_image):
    """Test feature extraction on real chart."""
    # Extract features
    features = image_processor.extract_features(sample_chart_image)
    
    # Verify feature extraction results
    assert "shapes" in features, "Should extract shape features"
    assert "text_regions" in features, "Should extract text region features"
    assert features["shapes"]["count"] > 0, "Should detect some shapes"
    assert features["text_regions"]["count"] > 0, "Should detect some text regions"

def test_chart_confidence_levels(chart_detector, image_processor, sample_chart_image):
    """Test confidence levels for chart detection."""
    # Process the image
    processed_image = image_processor.preprocess(sample_chart_image)
    
    # Detect chart with different confidence thresholds
    detector_high_conf = ChartDetector({"min_confidence": 0.9})
    detector_low_conf = ChartDetector({"min_confidence": 0.5})
    
    result_high = detector_high_conf.detect(processed_image)
    result_low = detector_low_conf.detect(processed_image)
    
    # Verify confidence behavior
    assert result_low["success"], "Should succeed with low confidence threshold"
    assert result_low["confidence"] >= 0.5, "Should meet low confidence threshold"
    
    # Note: High confidence test may or may not succeed depending on the chart
    if result_high["success"]:
        assert result_high["confidence"] >= 0.9, "Should meet high confidence threshold if successful"
