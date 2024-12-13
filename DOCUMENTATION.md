# LLiMage Documentation

[Previous content remains unchanged until Code Structure section...]

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
├── test_images/         # Test image outputs
│   ├── test_bar_chart.png       # Bar chart test images
│   ├── test_pie_chart.png       # Pie chart test images
│   ├── test_line_chart.png      # Line chart test images
│   └── test_shapes.png          # Basic shape test images
├── tests/               # Test suite
│   └── test_basic.py     # Basic tests
├── llimage/             # Main package
│   ├── chart/           # Chart processing
│   │   ├── detector.py   # Shape detection
│   │   ├── extractor.py  # Data extraction
│   │   └── tests/        # Chart-specific tests
│   ├── image/           # Image processing
│   │   ├── opencv.py     # OpenCV utilities
│   │   ├── processor.py  # Image processing
│   │   └── tests/        # Image-specific tests
│   └── output/          # Output formatting
│       ├── json.py       # JSON output
│       ├── text.py       # Text output
│       └── tests/        # Output-specific tests
└── cline_docs/          # Project documentation
    ├── projectRoadmap.md # Project goals
    ├── currentTask.md    # Current status
    ├── techStack.md      # Technology details
    └── codebaseSummary.md# Code overview
```

[Rest of the file remains unchanged...]
