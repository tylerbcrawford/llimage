# LLiMage 🖼️

## Overview 🌟
LLiMage is a local tool for extracting text and analyzing images from PDFs, with advanced capabilities for chart detection and analysis. The MVP uses a simple web interface built with Flask and runs entirely on your machine.

## Features ✨
- Drag-and-drop or file upload your PDF
- Extracts all text from the PDF
- Identifies images and runs OCR to extract any readable text from them
- Advanced chart detection and analysis:
  - Detects and classifies different chart types (bar, line, pie)
  - Analyzes structural relationships between shapes
  - Extracts data points and relationships from charts
  - Supports radial arrangements and grid patterns
- Provides detailed descriptions for images and charts
- Outputs in multiple formats (text, JSON)
- Fully local: no external data sharing unless you choose to add it later

## Requirements 🛠️
- Python 3.x
- Tesseract OCR installed locally (e.g., `brew install tesseract` on macOS)
- OpenCV for image processing and chart detection

## Installation 📦
1. Clone this repository
2. Create and activate virtual environment:
   ```bash
   # Create virtual environment
   python3 -m venv venv
   
   # Activate virtual environment
   # On macOS/Linux:
   source venv/bin/activate
   # On Windows:
   .\venv\Scripts\activate
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Ensure Tesseract is installed and accessible in your system's PATH

## Usage 🚀
1. Activate virtual environment (if not already activated):
   ```bash
   # On macOS/Linux:
   source venv/bin/activate
   # On Windows:
   .\venv\Scripts\activate
   ```
2. Run the Flask app:
   ```bash
   python app.py
   ```
3. Open `http://127.0.0.1:5000` in your browser
4. Drag and drop or select a PDF file
5. Once processed, you'll receive:
   - A text file with extracted text and descriptions
   - JSON output with structured data from charts
   - Visual debug output showing detected shapes and patterns

## License 📄
MIT License

## Security and Privacy 🔒
- All processing is done locally by default
- No external calls unless explicitly added later
- Logs are stored locally. Secure and monitor these logs if working with sensitive documents

## Progress and Capabilities 📈
- ✅ Basic text extraction and OCR
- ✅ Chart detection and classification
- ✅ Shape analysis and feature extraction
- ✅ Structural pattern recognition
- ✅ JSON output format
- ✅ Visual debugging tools
- ✅ Comprehensive test suite (52 tests)
- 🔄 Enhanced chart data extraction
- 🔄 Multiple output formats
- ⏳ UI enhancements
- ⏳ Performance optimizations

## Future Plans 🎯
- Support for more complex chart types
- Multiple-page PDFs with better performance
- Support for additional output formats
- Internationalization and multi-language OCR
- UI enhancements with progress bars and image previews
- Direct display of logs and results in browser
- Enhanced security features including HTTPS and user authentication
- Improved scalability for larger and more complex PDFs
- Machine learning integration for improved chart recognition

## Development 🔧
To run tests:
```bash
# Activate virtual environment if not already activated
source venv/bin/activate  # or .\venv\Scripts\activate on Windows

# Install pytest
pip install pytest

# Run tests
pytest
```

## Contributing 🤝
Contributions are welcome! Please feel free to submit a Pull Request. For major changes, please open an issue first to discuss what you would like to change.
