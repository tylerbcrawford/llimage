from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.graphics.shapes import Drawing, Rect
from reportlab.graphics.charts.linecharts import HorizontalLineChart
from reportlab.lib import colors
import os

def create_text_only_pdf():
    """Create a simple PDF with only text content."""
    c = canvas.Canvas("test_pdfs/text_only.pdf", pagesize=letter)
    c.drawString(100, 750, "Test PDF - Text Only")
    c.drawString(100, 700, "This is a simple text-only PDF document.")
    c.drawString(100, 650, "It contains multiple lines of text")
    c.drawString(100, 600, "to test the text extraction capabilities")
    c.drawString(100, 550, "of the LLiMage application.")
    c.save()

def create_text_and_image_pdf():
    """Create a PDF with both text and a simple shape as an image."""
    c = canvas.Canvas("test_pdfs/text_and_image.pdf", pagesize=letter)
    
    # Add text
    c.drawString(100, 750, "Test PDF - Text and Image")
    c.drawString(100, 700, "This PDF contains both text and an image.")
    
    # Draw a simple shape as an image
    c.setFillColor(colors.blue)
    c.rect(100, 400, 200, 200, fill=1)
    
    # Add more text below the image
    c.setFillColor(colors.black)
    c.drawString(100, 350, "The blue square above is a test image.")
    c.drawString(100, 300, "This tests mixed content processing.")
    
    c.save()

def create_chart_pdf():
    """Create a PDF with text and a simple chart."""
    c = canvas.Canvas("test_pdfs/chart.pdf", pagesize=letter)
    
    # Add text
    c.drawString(100, 750, "Test PDF - Chart Example")
    c.drawString(100, 700, "This PDF contains a simple line chart.")
    
    # Create and draw a simple line chart
    drawing = Drawing(400, 200)
    
    chart = HorizontalLineChart()
    chart.x = 50
    chart.y = 50
    chart.width = 300
    chart.height = 150
    
    # Add some data
    chart.data = [[1, 2, 3, 4, 5], [2, 4, 6, 8, 10]]
    
    # Add axis labels
    chart.categoryAxis.categoryNames = ['A', 'B', 'C', 'D', 'E']
    chart.valueAxis.valueMin = 0
    chart.valueAxis.valueMax = 12
    
    drawing.add(chart)
    drawing.drawOn(c, 100, 400)
    
    # Add description below the chart
    c.drawString(100, 350, "This is a simple line chart showing two data series.")
    c.drawString(100, 300, "It tests the chart recognition capabilities.")
    
    c.save()

def main():
    # Create test_pdfs directory if it doesn't exist
    os.makedirs("test_pdfs", exist_ok=True)
    
    # Create all test PDFs
    create_text_only_pdf()
    create_text_and_image_pdf()
    create_chart_pdf()
    
    print("Test PDFs have been created in the test_pdfs directory:")
    print("1. text_only.pdf - Contains only text")
    print("2. text_and_image.pdf - Contains text and a blue square")
    print("3. chart.pdf - Contains text and a line chart")

if __name__ == "__main__":
    main()
