"""
Tests for OpenCV integration and basic image processing functionality.
"""

import pytest
import cv2
import numpy as np
from pathlib import Path
from pdf2image import convert_from_path

@pytest.fixture
def test_pdfs_dir():
    """Get the test PDFs directory."""
    return Path(__file__).parent.parent.parent.parent / 'test_pdfs'

@pytest.fixture
def sample_chart_pdf(test_pdfs_dir):
    """Load and convert the chart PDF to image."""
    pdf_path = test_pdfs_dir / 'chart.pdf'
    assert pdf_path.exists(), f"Test PDF not found: {pdf_path}"
    
    # Convert first page of PDF to image
    images = convert_from_path(pdf_path)
    # Convert PIL image to OpenCV format
    img = cv2.cvtColor(np.array(images[0]), cv2.COLOR_RGB2BGR)
    return img

def test_opencv_installation():
    """Verify OpenCV is properly installed and can be imported."""
    assert cv2.__version__ is not None, "OpenCV version should be available"
    
def test_basic_image_operations(sample_chart_pdf):
    """Test basic OpenCV operations on a real chart image."""
    assert sample_chart_pdf is not None
    assert isinstance(sample_chart_pdf, np.ndarray)
    
    # Test grayscale conversion
    gray = cv2.cvtColor(sample_chart_pdf, cv2.COLOR_BGR2GRAY)
    assert len(gray.shape) == 2, "Grayscale image should be 2D"
    
    # Test thresholding
    _, thresh = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY)
    assert thresh.dtype == np.uint8
    
    # Test edge detection
    edges = cv2.Canny(gray, 100, 200)
    assert edges.dtype == np.uint8
    assert np.any(edges > 0), "Should detect some edges in the chart"

def test_contour_detection(sample_chart_pdf):
    """Test contour detection on chart image."""
    # Convert to grayscale
    gray = cv2.cvtColor(sample_chart_pdf, cv2.COLOR_BGR2GRAY)
    
    # Apply threshold
    _, thresh = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY)
    
    # Find contours
    contours, hierarchy = cv2.findContours(
        thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE
    )
    
    assert len(contours) > 0, "Should detect some contours in the chart"
    
    # Test contour properties
    for contour in contours:
        assert len(contour.shape) == 3, "Contour should be a 3D array"
        assert contour.shape[2] == 2, "Each point should have x,y coordinates"

def test_shape_detection(sample_chart_pdf):
    """Test basic shape detection capabilities."""
    # Convert to grayscale
    gray = cv2.cvtColor(sample_chart_pdf, cv2.COLOR_BGR2GRAY)
    
    # Apply threshold
    _, thresh = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY)
    
    # Find contours
    contours, _ = cv2.findContours(
        thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE
    )
    
    shapes_found = []
    for contour in contours:
        # Approximate the contour
        peri = cv2.arcLength(contour, True)
        approx = cv2.approxPolyDP(contour, 0.04 * peri, True)
        
        # Classify shape based on vertices
        vertices = len(approx)
        if vertices == 3:
            shapes_found.append("triangle")
        elif vertices == 4:
            shapes_found.append("rectangle")
        elif vertices > 8:
            shapes_found.append("circle")
    
    assert len(shapes_found) > 0, "Should detect some shapes in the chart"

def test_text_region_detection(sample_chart_pdf):
    """Test detection of potential text regions."""
    # Convert to grayscale
    gray = cv2.cvtColor(sample_chart_pdf, cv2.COLOR_BGR2GRAY)
    
    # Apply adaptive threshold
    thresh = cv2.adaptiveThreshold(
        gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 11, 2
    )
    
    # Find contours
    contours, _ = cv2.findContours(
        thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE
    )
    
    # Filter contours that might be text
    text_regions = []
    for contour in contours:
        x, y, w, h = cv2.boundingRect(contour)
        aspect_ratio = w / float(h)
        
        # Text regions typically have specific aspect ratios
        if 0.1 < aspect_ratio < 15:  # Adjust these values based on your needs
            text_regions.append((x, y, w, h))
    
    assert len(text_regions) > 0, "Should detect potential text regions in the chart"
