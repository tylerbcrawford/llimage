# Codebase Summary

## Current Project Structure
```
llimage/
├── app.py                 # Main Flask application
├── create_test_pdfs.py    # Test PDF generation script
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
├── test_images/         # Test image outputs
│   ├── test_bar_chart*.png    # Bar chart test images
│   ├── test_pie_chart*.png    # Pie chart test images
│   ├── test_line_chart*.png   # Line chart test images
│   └── test_shapes*.png       # Shape detection tests
├── config/               # Configuration files
│   ├── default.json      # Default settings
│   └── logging.json      # Logging configuration
├── llimage/              # Core package directory
│   ├── __init__.py       # Package initialization
│   ├── chart/            # Chart processing modules
│   │   ├── __init__.py
│   │   ├── detector.py   # Chart type detection
│   │   ├── extractor.py  # Data extraction
│   │   ├── classifier.py # Chart classification
│   │   └── tests/        # Chart-specific tests
│   ├── image/            # Image processing
│   │   ├── __init__.py
│   │   ├── opencv.py     # OpenCV operations
│   │   ├── processor.py  # Image preprocessing
│   │   └── tests/        # Image-specific tests
│   └── output/           # Output formatting
│       ├── __init__.py
│       ├── json.py       # JSON formatter
│       ├── text.py       # Text formatter
│       └── tests/        # Output-specific tests
└── tests/               # Basic test suite
    └── test_basic.py     # Basic functionality tests
```

## Key Components

### Current Implementation
- Flask application setup
- PDF processing routes
- File handling logic
- OCR integration
- Basic frontend interface
- Advanced chart detection system
- Shape classification and analysis
- Data extraction from charts
- Multiple output formats (JSON, text)

### Implemented Phase 2 Features
#### Chart Processing Module ✅
- Chart type detection system
  - Bar chart detection
  - Pie chart detection
  - Line chart detection
- Shape classification
  - Rectangle detection
  - Circle detection
  - Triangle detection
  - Point detection
- Structural analysis
  - Vertical alignment
  - Horizontal alignment
  - Radial arrangement
  - Grid pattern detection
- Data extraction algorithms
- OpenCV integration

#### Enhanced Image Processing ✅
- OpenCV operations wrapper
- Image preprocessing pipeline
- Feature detection system
- Text region identification
- Shape feature extraction
- Noise handling

#### Output Formatting ✅
- Structured JSON output
- Enhanced text descriptions
- Configuration-based formatting
- Debug visualization outputs

## Data Flow

### Current Flow
1. User uploads PDF
2. Server processes file:
   - Text extraction
   - Image identification
   - Chart detection
   - Shape classification
   - Feature extraction
   - Data point analysis
3. Results compiled in multiple formats
4. Download options provided

### Planned Phase 3 Flow
1. User uploads PDF
2. User selects output preferences:
   - Image handling mode (separate files or textual descriptions)
   - Output format preferences
   - Additional configuration options
3. Server processes file:
   - Text extraction
   - Image identification and processing
   - Chart detection and analysis
   - Shape classification
   - Feature extraction
   - Data point analysis
4. Based on selected mode:
   - Option 1: Separate Image Files
     - Images extracted and saved separately
     - Standardized naming scheme applied
     - References included in text output
   - Option 2: Textual Descriptions
     - ML-based image descriptions generated
     - Descriptions integrated into text output
     - No separate image files created
   - Hybrid Mode (when configured)
     - Both separate files and descriptions provided
5. Results compiled according to preferences
6. Download options provided

## Recent Changes
- Implemented chart detection module
- Added shape classification system
- Enhanced feature extraction
- Added test image organization
- Improved documentation structure
- Added comprehensive test suite

## Planned Improvements
- Enhanced chart data extraction
- Multiple output format support
- UI enhancements
- Performance optimizations
- Batch processing capabilities
- Advanced image output options:
  - Separate image file extraction system
    - Dedicated output directory structure
    - Standardized naming conventions
    - Image reference system
  - Enhanced textual descriptions
    - ML-based description generation
    - Context-aware descriptions
    - Chart-specific interpretations
  - Configurable output modes
    - User interface controls
    - Environment variable support
    - Command-line options
  - Hybrid mode support
    - Combined output capabilities
    - Flexible configuration options
    - Performance optimizations

## External Dependencies
### Current
- OpenCV for image processing
- NumPy for numerical operations
- pytest for testing
- Flask for web interface
- PDF processing libraries

## Development Guidelines
- Modular code structure
- Comprehensive testing
- Clear documentation
- Security-first approach
- Configuration-driven features
- Test-driven development
- Organized test assets
