# LLiMage Documentation

## 1. Project Overview

LLiMage is a Python-based web application designed for efficient PDF processing and analysis. It provides local processing capabilities for extracting text, performing OCR on images, and analyzing charts within PDF documents.

### Key Features
- PDF text extraction with high accuracy
- Image OCR processing for embedded images
- Basic chart recognition and description
- Web-based interface with drag-and-drop functionality
- Local processing for enhanced security
- Text-based output for extracted information
- Test suite with sample PDFs

## 2. Tech Stack

### Core Technologies
- **Python 3.x**
  - Primary development language
  - Chosen for extensive library support and ease of development

### Framework
- **Flask**
  - Lightweight web framework
  - Perfect for MVP development
  - Easy to extend
  - Minimal setup requirements

### PDF Processing Libraries
- **pdfplumber**
  - Reliable PDF parsing
  - Accurate text extraction
  - Chosen for its robust PDF handling capabilities

### OCR Technology
- **pytesseract**
  - OCR functionality
  - Integration with Tesseract OCR engine
  - Supports multiple languages
- **pdf2image with poppler**
  - PDF to image conversion
  - Required for OCR processing

### Frontend
- **HTML/CSS/JavaScript**
  - Modern drag-and-drop interface
  - Responsive design
  - Client-side file handling

## 3. Installation and Setup

### Prerequisites
1. Python 3.x
2. Tesseract OCR
3. Poppler Utils

### System-Specific Installation

#### macOS
```bash
# Install system dependencies
brew install tesseract
brew install poppler

# Clone repository
git clone https://github.com/tylerbcrawford/llimage.git
cd llimage

# Create and activate virtual environment
python3 -m venv venv
source venv/bin/activate

# Install Python dependencies
pip install -r requirements.txt
```

#### Linux (Ubuntu/Debian)
```bash
# Install system dependencies
sudo apt-get update
sudo apt-get install tesseract-ocr
sudo apt-get install poppler-utils

# Clone and setup (same as macOS)
git clone https://github.com/tylerbcrawford/llimage.git
cd llimage
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

#### Windows
1. Download and install Tesseract from: http://blog.alivate.com.au/poppler-windows/
2. Add Tesseract to system PATH
3. Follow similar Python setup steps as above

## 4. Code Structure

```
llimage/
├── app.py                 # Main Flask application
├── create_test_pdfs.py    # Test PDF generation
├── requirements.txt       # Python dependencies
├── static/               # Static assets
│   ├── script.js         # Frontend JavaScript
│   └── style.css         # CSS styles
├── templates/            # Flask templates
│   └── index.html        # Main web interface
├── test_pdfs/           # Test PDF files
│   ├── chart.pdf         # Chart test file
│   ├── text_and_image.pdf# Mixed content test
│   └── text_only.pdf     # Text test file
├── tests/               # Test suite
│   └── test_basic.py     # Basic tests
└── cline_docs/          # Project documentation
    ├── projectRoadmap.md # Project goals
    ├── currentTask.md    # Current status
    ├── techStack.md      # Technology details
    └── codebaseSummary.md# Code overview
```

## 5. Functionality

### PDF Processing Pipeline
1. **File Upload**
   - Drag-and-drop or file selection
   - Initial validation
   - Temporary storage

2. **Text Extraction**
   - PDF parsing using pdfplumber
   - Text content extraction
   - Structure preservation

3. **Image Processing**
   - Image identification
   - Conversion to processable format
   - OCR processing

4. **Chart Recognition**
   - Basic chart detection
   - Simple description generation
   - Data extraction where possible

5. **Result Generation**
   - Compilation of extracted data
   - Text file generation
   - Download link provision

### Usage Example
1. Access web interface at `http://127.0.0.1:5000`
2. Upload PDF through drag-and-drop or file selection
3. Wait for processing completion
4. Download results as text file

## 6. Documentation

### Environment Variables
- No environment variables required for basic setup
- All configuration is handled through Python files

### Configuration Files
- `requirements.txt`: Python package dependencies
- `.gitignore`: Version control exclusions

## 7. Testing

### Running Tests
```bash
# Activate virtual environment
source venv/bin/activate

# Run test suite
pytest
```

### Test Files
- Located in `test_pdfs/` directory
- Cover different use cases:
  - Text extraction (text_only.pdf)
  - Image processing (text_and_image.pdf)
  - Chart recognition (chart.pdf)

## 8. Known Issues and Limitations

- Limited to single-page PDFs in current version
- Basic chart recognition capabilities
- Memory-intensive for large PDFs
- No persistent storage of results
- Limited error handling for complex PDFs

## 9. Future Enhancements

- Multi-page PDF support
- Advanced chart recognition
- Multiple output formats (JSON, XML)
- Progress bar implementation
- Enhanced error handling
- User authentication
- Result history
- Batch processing
- API development

## 10. Contributing

1. Fork the repository
2. Create a feature branch
3. Implement changes
4. Add/update tests
5. Submit pull request

### Development Guidelines
- Follow PEP 8 style guide
- Add tests for new features
- Update documentation
- Maintain security focus

## 11. Acknowledgments

- Flask framework community
- Tesseract OCR project
- PDF processing libraries:
  - pdfplumber
  - pdf2image
  - pytesseract
- Open source community

## 12. License

MIT License

Copyright (c) 2024

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
