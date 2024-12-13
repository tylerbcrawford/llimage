"""
Test for shape classification accuracy.
"""

import cv2
import numpy as np
from llimage.chart.detector import ChartDetector

def test_individual_shapes():
    """Test each shape individually first."""
    detector = ChartDetector({
        'min_shape_area': 100,
        'min_confidence': 0.5,
        'shape_similarity_threshold': 0.85,
    })
    
    # Test rectangle
    rect_img = np.zeros((200, 200), dtype=np.uint8)
    cv2.rectangle(rect_img, (50, 50), (150, 150), 255, -1)
    cv2.imwrite('test_rectangle.png', rect_img)
    
    processed = detector.preprocess_image(rect_img)
    shapes, types, _ = detector.detect_shapes(processed)
    assert len(shapes) == 1, "Should detect one rectangle"
    assert types[0] in ["rectangle", "square"], f"Should classify as rectangle/square, got {types[0]}"
    
    # Test circle
    circle_img = np.zeros((200, 200), dtype=np.uint8)
    cv2.circle(circle_img, (100, 100), 50, 255, -1)
    cv2.imwrite('test_circle.png', circle_img)
    
    processed = detector.preprocess_image(circle_img)
    shapes, types, _ = detector.detect_shapes(processed)
    assert len(shapes) == 1, "Should detect one circle"
    assert types[0] == "circle", f"Should classify as circle, got {types[0]}"
    
    # Test triangle
    triangle_img = np.zeros((200, 200), dtype=np.uint8)
    pts = np.array([[100, 50], [50, 150], [150, 150]], dtype=np.int32)
    cv2.fillPoly(triangle_img, [pts], 255)
    cv2.imwrite('test_triangle.png', triangle_img)
    
    processed = detector.preprocess_image(triangle_img)
    shapes, types, _ = detector.detect_shapes(processed)
    assert len(shapes) == 1, "Should detect one triangle"
    assert types[0] == "triangle", f"Should classify as triangle, got {types[0]}"

def test_combined_shapes():
    """Test all shapes together only after individual tests pass."""
    detector = ChartDetector({
        'min_shape_area': 100,
        'min_confidence': 0.5,
        'shape_similarity_threshold': 0.85,
    })
    
    # Create test image with all shapes
    img = np.zeros((400, 400), dtype=np.uint8)
    
    # Draw rectangle with good spacing
    cv2.rectangle(img, (50, 50), (150, 150), 255, -1)
    
    # Draw circle with good spacing
    cv2.circle(img, (250, 250), 50, 255, -1)
    
    # Draw triangle with good spacing
    triangle_pts = np.array([
        [300, 50],
        [250, 150],
        [350, 150]
    ], dtype=np.int32)
    cv2.fillPoly(img, [triangle_pts], 255)
    
    # Save original image
    cv2.imwrite('test_all_shapes.png', img)
    
    # Process and detect shapes
    processed = detector.preprocess_image(img)
    cv2.imwrite('test_all_shapes_processed.png', processed)
    
    shapes, types, features = detector.detect_shapes(processed)
    
    # Print debug information
    print("\nShape Detection Results:")
    print(f"Number of shapes detected: {len(shapes)}")
    print(f"Shape types detected: {types}")
    
    for i, (shape_type, feature) in enumerate(zip(types, features)):
        print(f"\nShape {i+1} ({shape_type}):")
        print(f"  Area: {feature['area']}")
        print(f"  Extent: {feature['extent']:.2f}")
        print(f"  Solidity: {feature['solidity']:.2f}")
        print(f"  Circularity: {feature['circularity']:.2f}")
        print(f"  Aspect Ratio: {feature['aspect_ratio']:.2f}")
        print(f"  Vertices: {feature['vertices']}")
    
    # Save debug image
    debug_img = img.copy()
    for i, shape in enumerate(shapes):
        # Draw each shape in a different gray level for visibility
        gray_level = 50 + (i * 50)  # 50, 100, 150 for different shapes
        cv2.drawContours(debug_img, [shape], -1, gray_level, 2)
    cv2.imwrite('test_all_shapes_detected.png', debug_img)
    
    # Verify results
    assert len(shapes) == 3, f"Expected 3 shapes, but found {len(shapes)}: {types}"
    assert any(t in ["rectangle", "square"] for t in types), \
        f"No rectangle/square found in shapes: {types}"
    assert "circle" in types, f"No circle found in shapes: {types}"
    assert "triangle" in types, f"No triangle found in shapes: {types}"
