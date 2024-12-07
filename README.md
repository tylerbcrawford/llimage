# LLiMage

## Overview
LLiMage is a local tool for extracting text and basic descriptions of images from PDFs, outputting the results as plain text. The MVP uses a simple web interface built with Flask and runs entirely on your machine.

## Features
- Drag-and-drop or file upload your PDF
- Extracts all text from the PDF
- Identifies images and runs OCR to extract any readable text from them
- Provides a simplistic description for images (fallback if it's unclear)
- Outputs a single `.txt` file containing all extracted information
- Fully local: no external data sharing unless you choose to add it later

## Requirements
- Python 3.x
- Tesseract OCR installed locally (e.g., `brew install tesseract` on macOS)

## Installation
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

## Usage
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
5. Once processed, a download link for the `.txt` file will be provided

## License
MIT License

## Security and Privacy
- All processing is done locally by default
- No external calls unless explicitly added later
- Logs are stored locally. Secure and monitor these logs if working with sensitive documents

## Future Plans
- Support for more detailed chart descriptions
- Multiple-page PDFs with better performance
- Support for more output formats (JSON, structured data)
- Internationalization and multi-language OCR
- UI enhancements with progress bars and image previews
- Direct display of logs and results in browser
- Enhanced security features including HTTPS and user authentication
- Improved scalability for larger and more complex PDFs

## Development
To run tests:
```bash
# Activate virtual environment if not already activated
source venv/bin/activate  # or .\venv\Scripts\activate on Windows

# Install pytest
pip install pytest

# Run tests
pytest
