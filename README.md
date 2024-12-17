# 🖼️ LLiMage

Transform your PDF data for LLM processing—securely, locally, and efficiently.

## 📑 Table of Contents
- [Overview](#-overview)
- [Why LLiMage?](#-why-llimage)
- [Privacy and Security First](#-privacy-and-security-first)
- [Features](#-features)
- [Requirements](#️-requirements)
- [Installation](#-installation)
- [Usage](#-usage)
- [Progress and Capabilities](#-progress-and-capabilities)
- [Future Plans](#-future-plans)
- [Development](#-development)
- [Contributing](#-contributing)
- [License](#-license)

## 🌟 Overview

LLiMage transforms your PDFs into richer, more accessible data streams ready for large language models (LLMs)—even those that don't accept images. By extracting text and intelligently describing embedded images, LLiMage ensures that no valuable information is lost. With a simple web interface and fully local processing, it's designed for both everyday office users and researchers who want to get the most out of their documents, all while respecting privacy and enhancing token efficiency to save on costs.

## 🎯 Why LLiMage?

- **For Office Users**: Seamlessly process reports, presentations, and documents with charts and images. Convert them into detailed text files that free-tier LLMs can interpret, helping you get the most from your data without breaking the bank.
- **For Researchers & Professionals**: Streamline complex PDFs and image-heavy sources into a text-only format, offering maximum flexibility to choose any LLM—no image constraints, no vendor lock-ins. Gain full control over your data for in-depth analysis and unlock new insights in your workflow.

## 🔒 Privacy and Security First

LLiMage runs locally, ensuring your documents never leave your machine. No external calls mean your sensitive data stays under your control, reinforcing good security and compliance practices while demonstrating robust cybersecurity principles.

## ✨ Features

- **Simple, Intuitive Interface**: Drag-and-drop or browse to select a PDF file.
- **Comprehensive Data Extraction**: Extracts all text from the PDF and uses OCR to identify and interpret embedded images.
- **LLM-Ready Output**: Produces a single .txt file with all textual content and image descriptions, allowing an LLM without image-processing capabilities to understand the full context.
- **Local-Only Processing**: No external data sharing by default. Your data never leaves your machine.
- **Advanced Chart Detection and Analysis**:
  - Detects and classifies different chart types (bar, line, pie)
  - Analyzes structural relationships between shapes
  - Extracts data points and relationships from charts
  - Supports radial arrangements and grid patterns
- **Multiple Output Formats**: Text and JSON outputs available
- **Visual Debugging Tools**: Debug output showing detected shapes and patterns
- **Flexible Image Processing** (Coming in Phase 3):
  - Option to save images as separate files with standardized naming
  - Advanced textual descriptions of images and charts
  - Configurable output preferences

## 🛠️ Requirements
- Python 3.x
- Tesseract OCR installed locally (e.g., `brew install tesseract` on macOS)
- OpenCV for image processing and chart detection

## 📦 Installation
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

## 🚀 Usage
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

## 📈 Progress and Capabilities
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

## 🎯 Future Plans
- Advanced Image Output Options (Phase 3):
  * Separate image file extraction with standardized naming
  * Enhanced textual descriptions of visual content
  * User-configurable output preferences
  * Potential hybrid mode combining both approaches
- Support for more complex chart types
- Multiple-page PDFs with better performance
- Support for additional output formats
- Internationalization and multi-language OCR
- UI enhancements with progress bars and image previews
- Direct display of logs and results in browser
- Enhanced security features including HTTPS and user authentication
- Improved scalability for larger and more complex PDFs
- Machine learning integration for improved chart recognition

## 🔧 Development
To run tests:
```bash
# Activate virtual environment if not already activated
source venv/bin/activate  # or .\venv\Scripts\activate on Windows

# Install pytest
pip install pytest

# Run tests
pytest
```

## 🤝 Contributing
Contributions are welcome! Please feel free to submit a Pull Request. For major changes, please open an issue first to discuss what you would like to change.

## 📄 License
This project is licensed under the GNU Affero General Public License v3.0 (AGPL-3.0) with additional non-commercial use restrictions. See the [LICENSE](LICENSE) file for details.

Key points:
- Free for personal and educational use
- Commercial use requires a separate license
- Contact tylerbcrawford@gmail.com for commercial licensing
- Full AGPL-3.0 terms apply to non-commercial use
