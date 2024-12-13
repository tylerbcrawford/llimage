"""
Tests for chart data extraction functionality.
"""

import cv2
import numpy as np
import pytest
from llimage.chart.extractor import ChartDataExtractor
from llimage.chart.detector import ChartDetector

def create_bar_chart() -> np.ndarray:
    """Create a test bar chart with known values."""
    img = np.zeros((400, 400), dtype=np.uint8)
    
    # Draw bars with different heights
    bar_heights = [100, 150, 200, 125]
    bar_width = 40
    spacing = 60
    start_x = 100
    
    for i, height in enumerate(bar_heights):
        x = start_x + (i * spacing)
        cv2.rectangle(img, (x, 400-height), (x+bar_width, 400), 255, -1)
        
        # Add label below bar
        label_y = 420  # Below the bar
        cv2.putText(img, f"Bar{i+1}", (x, label_y), 
                   cv2.FONT_HERSHEY_SIMPLEX, 0.5, 255, 1)
    
    return img

def create_pie_chart() -> np.ndarray:
    """Create a test pie chart with known segments."""
    img = np.zeros((400, 400), dtype=np.uint8)
    center = (200, 200)
    radius = 150
    
    # Draw pie segments with different angles and larger gaps
    start_angles = [5, 95, 185, 275]  # 5-degree gaps
    end_angles = [85, 175, 265, 355]
    
    # Draw each segment separately with clear gaps
    for i, (start_angle, end_angle) in enumerate(zip(start_angles, end_angles)):
        # Create a separate image for each segment
        segment_img = np.zeros((400, 400), dtype=np.uint8)
        
        # Draw filled segment
        cv2.ellipse(segment_img, center, (radius, radius), 0, 
                   start_angle, end_angle, 255, -1)
        
        # Add a border by eroding
        kernel = np.ones((5,5), np.uint8)  # Larger kernel for bigger gaps
        segment_img = cv2.erode(segment_img, kernel, iterations=1)
        
        # Add the segment to the main image
        img = cv2.bitwise_or(img, segment_img)
        
        # Add label
        angle = np.radians((start_angle + end_angle) / 2)
        label_x = int(center[0] + (radius + 30) * np.cos(angle))
        label_y = int(center[1] + (radius + 30) * np.sin(angle))
        cv2.putText(img, f"Seg{i+1}", (label_x, label_y), 
                   cv2.FONT_HERSHEY_SIMPLEX, 0.5, 255, 1)
    
    return img

def create_line_chart() -> np.ndarray:
    """Create a test line chart with known points."""
    img = np.zeros((400, 400), dtype=np.uint8)
    
    # Draw points with good spacing
    points = [
        (100, 200),
        (200, 150),
        (300, 250),
        (400, 100)
    ]
    
    # Draw points first as filled circles with borders
    for x, y in points:
        # Draw white filled circle with padding
        cv2.circle(img, (x, y), 15, 255, -1)  # Larger radius
        # Draw gray border
        cv2.circle(img, (x, y), 15, 128, 2)
        
        # Add label below point
        label_y = y + 30  # More space for label
        cv2.putText(img, f"P{points.index((x,y))+1}", (x-10, label_y), 
                   cv2.FONT_HERSHEY_SIMPLEX, 0.5, 255, 1)
    
    # Draw connecting lines in gray (128) - thinner and less prominent
    for i in range(len(points)-1):
        cv2.line(img, points[i], points[i+1], 128, 1)
    
    return img

def test_bar_chart_extraction():
    """Test extraction of data from bar charts."""
    # Create test image
    img = create_bar_chart()
    cv2.imwrite('test_bar_chart.png', img)
    
    # Initialize detector and extractor
    detector = ChartDetector()
    extractor = ChartDataExtractor()
    
    # Process image
    processed = detector.preprocess_image(img)
    cv2.imwrite('test_bar_chart_processed.png', processed)
    
    shapes, _, features = detector.detect_shapes(processed)
    
    # Extract data
    result = extractor.extract_data(img, "bar", shapes, features)
    
    # Save debug visualization
    debug_img = img.copy()
    for i, bar in enumerate(result["data"]["bars"]):
        # Draw bounding box
        x, w = bar["x"], bar["width"]
        y = 400 - bar["height"]
        cv2.rectangle(debug_img, (x, y), (x+w, 400), 128, 2)
        
        # Draw height value
        cv2.putText(debug_img, f"H:{bar['height']}", (x, y-10),
                   cv2.FONT_HERSHEY_SIMPLEX, 0.5, 128, 1)
    
    cv2.imwrite('test_bar_chart_debug.png', debug_img)
    
    # Verify results
    assert result["success"], "Bar chart extraction should succeed"
    assert result["type"] == "bar", "Should identify as bar chart"
    assert len(result["data"]["bars"]) == 4, "Should detect 4 bars"
    
    # Verify bar heights are in expected order
    heights = [bar["height"] for bar in result["data"]["bars"]]
    assert heights[0] < heights[1] < heights[2] > heights[3], \
        "Bar heights should match expected pattern"

def test_pie_chart_extraction():
    """Test extraction of data from pie charts."""
    # Create test image
    img = create_pie_chart()
    cv2.imwrite('test_pie_chart.png', img)
    
    # Initialize detector and extractor
    detector = ChartDetector()
    extractor = ChartDataExtractor()
    
    # Process image
    processed = detector.preprocess_image(img)
    cv2.imwrite('test_pie_chart_processed.png', processed)
    
    shapes, _, features = detector.detect_shapes(processed)
    
    # Extract data
    result = extractor.extract_data(img, "pie", shapes, features)
    
    # Save debug visualization
    debug_img = img.copy()
    if result["success"]:
        center = result["data"]["center"]
        for i, segment in enumerate(result["data"]["segments"]):
            # Draw radius line at segment angle
            angle_rad = np.radians(segment["angle"])
            end_x = int(center[0] + 170 * np.cos(angle_rad))
            end_y = int(center[1] + 170 * np.sin(angle_rad))
            cv2.line(debug_img, center, (end_x, end_y), 128, 1)
            
            # Draw percentage
            text_x = int(center[0] + 140 * np.cos(angle_rad))
            text_y = int(center[1] + 140 * np.sin(angle_rad))
            cv2.putText(debug_img, f"{segment['percentage']:.1f}%", 
                       (text_x, text_y), cv2.FONT_HERSHEY_SIMPLEX, 0.5, 128, 1)
    
    cv2.imwrite('test_pie_chart_debug.png', debug_img)
    
    # Verify results
    assert result["success"], "Pie chart extraction should succeed"
    assert result["type"] == "pie", "Should identify as pie chart"
    assert len(result["data"]["segments"]) == 4, "Should detect 4 segments"
    
    # Verify segment percentages sum to approximately 100%
    total = sum(segment["percentage"] for segment in result["data"]["segments"])
    assert 99.0 <= total <= 101.0, f"Segment percentages should sum to ~100%, got {total}"

def test_line_chart_extraction():
    """Test extraction of data from line charts."""
    # Create test image
    img = create_line_chart()
    cv2.imwrite('test_line_chart.png', img)
    
    # Initialize detector and extractor
    detector = ChartDetector()
    extractor = ChartDataExtractor()
    
    # Process image
    processed = detector.preprocess_image(img)
    cv2.imwrite('test_line_chart_processed.png', processed)
    
    shapes, _, features = detector.detect_shapes(processed)
    
    # Extract data
    result = extractor.extract_data(img, "line", shapes, features)
    
    # Save debug visualization
    debug_img = img.copy()
    if result["success"] and len(result["data"]["points"]) > 0:
        points = result["data"]["points"]
        for i in range(len(points)-1):
            # Draw line between points
            p1 = (points[i]["x"], points[i]["y"])
            p2 = (points[i+1]["x"], points[i+1]["y"])
            cv2.line(debug_img, p1, p2, 128, 2)
            
            # Draw point coordinates
            cv2.putText(debug_img, f"({p1[0]},{p1[1]})", 
                       (p1[0]-30, p1[1]-10), cv2.FONT_HERSHEY_SIMPLEX, 0.4, 128, 1)
        
        # Draw last point coordinates
        last = points[-1]
        cv2.putText(debug_img, f"({last['x']},{last['y']})", 
                   (last['x']-30, last['y']-10), cv2.FONT_HERSHEY_SIMPLEX, 0.4, 128, 1)
    
    cv2.imwrite('test_line_chart_debug.png', debug_img)
    
    # Verify results
    assert result["success"], "Line chart extraction should succeed"
    assert result["type"] == "line", "Should identify as line chart"
    assert len(result["data"]["points"]) == 4, "Should detect 4 points"
    
    # Verify points are in expected order
    x_coords = [point["x"] for point in result["data"]["points"]]
    assert all(x_coords[i] < x_coords[i+1] for i in range(len(x_coords)-1)), \
        "Points should be ordered by x-coordinate"
