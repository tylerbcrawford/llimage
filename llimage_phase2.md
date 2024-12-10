Below is a proposed plan for the next development phase, focusing on expanding image extraction and chart recognition capabilities. This plan keeps security, privacy, and FOSS principles in mind, and it remains compatible with a local or future web-based deployment. Additionally, it breaks down enhancements into manageable phases to allow incremental improvements.

Next Phase: Advanced Image and Chart Processing

Goals
	•	Enhanced Chart Recognition: Move beyond basic image descriptions to identify chart types and extract structured data (e.g., approximate values, labels).
	•	Improved Image Analysis: Differentiate charts from other images, detect text labels more accurately, and identify visual elements (axes, bars, lines, pie slices).
	•	Configurable Detail Level: Allow the user or configuration settings to determine the level of detail and complexity in the output.

High-Level Approach
	1.	Local Processing with Open-Source Tools:
	•	Integrate computer vision libraries (e.g., OpenCV) and possibly scikit-image to identify geometric shapes, lines, and text regions.
	•	Continue using Tesseract for OCR but consider ways to segment images before running OCR to improve accuracy.
	2.	Chart Type Classification:
	•	Start by classifying chart images into a few major categories: bar charts, line graphs, pie charts, and other/unknown.
	•	This could initially be heuristic-based (e.g., detect horizontal/vertical lines for bar charts, circular shapes for pie charts) and then later incorporate simple ML-based classification.
	3.	Data Extraction Heuristics:
	•	For bar charts: detect the bars by finding rectangular shapes. Estimate bar height relative to the axis using pixel coordinates. Use OCR’d axis labels and tick marks to approximate numeric values.
	•	For line graphs: detect continuous lines between data points. Estimate the y-values at known x-label positions using OCR’d axis information.
	•	For pie charts: detect the presence of a circle or ellipse, identify pie “slices” by color changes or line segments, and use any embedded legend or labels from OCR to map slices to categories.
	4.	Scalability and Modularity:
	•	Wrap chart recognition logic into separate, testable Python modules that can be easily maintained, replaced, or improved later.
	•	Maintain the option to skip advanced analysis for simpler/faster runs.
	5.	Structured Output Option (Phase 2):
	•	Offer a config setting or command-line parameter to output a more structured format (e.g., JSON) that includes detailed chart data, making it more useful for downstream LLM processing. The user can still opt for plain text if preferred.
	6.	Security and Privacy Considerations:
	•	Keep all image processing local to avoid sending images to external services.
	•	Ensure that no additional sensitive data is logged.
	•	Consider testing on sanitized sample PDFs.
	•	Note in documentation how advanced processing may require more dependencies (e.g., OpenCV) and keep these well-maintained and up-to-date.

Detailed Steps & Milestones

Phase 1: Basic Chart Type Detection and Heuristics
	•	Add Dependencies:
	•	Integrate OpenCV (FOSS) for image analysis.
	•	Update requirements.txt and documentation to reflect new dependencies.
	•	Implement Chart Detection Pipeline:
	•	Convert each page’s image(s) to a grayscale or binary representation.
	•	Detect geometric features: lines, rectangles, circles.
	•	Implement simple classification rules:
	•	Bar Chart: Multiple parallel rectangular bars.
	•	Line Chart: One or more continuous lines (thin, elongated shapes).
	•	Pie Chart: A circle divided into segments.
	•	Unknown Chart/Image: None of the above detected.
	•	Extract Basic Text Using OCR:
	•	Run OCR first.
	•	Identify potential axes labels or legends near detected shapes.
	•	For MVP of this phase, just describe the chart type and any detected text labels.
	•	Output Changes:
	•	If a chart is detected, output a section like:

=== Page X Image Y Description ===
Detected a bar chart with the following axis labels: ...
Approximate bar categories: ...


	•	If unsure, fallback to the existing generic description.

	•	Testing and Debugging:
	•	Add new test PDFs specifically containing known chart types (bar, line, pie).
	•	Write unit tests for chart detection methods.
	•	Validate performance with small PDFs.

Phase 2: Approximating Data Points
	•	Bar Chart Data Extraction:
	•	Once a bar chart is detected, find the bar heights by analyzing pixel coordinates.
	•	Use OCR’d axis labels to map pixel coordinates to approximate numeric values.
	•	Include these approximations in the output:

Bar 1: Category "A" ~ 30 units
Bar 2: Category "B" ~ 50 units


	•	Line Chart Data Extraction:
	•	If a line chart is detected, sample points along the line at known x-axis positions (from OCR’d tick labels).
	•	Estimate corresponding y-values and include them in the output.
	•	Pie Chart Data Extraction:
	•	Identify the number of slices by analyzing line segments radiating from the circle’s center.
	•	Approximate slice proportions by measuring arc lengths or angles.
	•	Link slices to legend text (if found) and include approximate percentages.

Phase 3: Structured Output and Configuration
	•	Structured Output:
	•	Introduce a JSON output option via a command-line flag or environment variable.
	•	JSON includes structured data:

{
  "page_1": {
    "text": "...",
    "charts": [
      {
        "type": "bar",
        "x_axis_labels": ["Q1", "Q2", "Q3"],
        "y_axis_range": [0, 100],
        "bars": [
          {"label": "Q1", "value_approx": 30},
          {"label": "Q2", "value_approx": 50}
        ]
      }
    ]
  }
}


	•	Configuration Settings:
	•	Add a configuration file or environment variables to turn advanced analysis on/off.
	•	Allow specifying OCR language (future-ready for multilingual support).
	•	Add verbosity levels for logging related to image analysis steps.

Updated Documentation Guidelines
	•	README Updates:
	•	Document the new dependencies (OpenCV).
	•	Explain how to enable advanced analysis features.
	•	Provide instructions for switching output formats (text vs JSON).
	•	Code Comments & Developer Guide:
	•	Inline comments in the chart processing module explaining detection logic.
	•	A separate DEVELOPER.md guide explaining how to adjust heuristics, add new chart types, or integrate ML models.
	•	Security Considerations:
	•	Emphasize that no external calls are made.
	•	Discuss potential sandboxing of image processing operations.
	•	Highlight that only user-provided PDFs and locally generated images are analyzed.

Timeline and Resource Considerations
	•	Phase 1 (1-2 weeks):
	•	Integrate OpenCV, implement basic chart detection, update output, basic tests.
	•	Phase 2 (2-4 weeks):
	•	Add data extraction heuristics, refine OCR integration with chart detection, more tests.
	•	Phase 3 (1 week):
	•	Introduce JSON output, configuration options, and finalize documentation.

Conclusion

By following the plan above, you can incrementally enhance LLiMage’s capabilities, providing more informative and structured outputs from charts and images. Starting with heuristics and open-source libraries lays a strong foundation for future improvements, such as integrating simple ML models for even more accurate chart classification or data extraction.

These upgrades, combined with rigorous testing and careful documentation, will strengthen the tool’s value for both users and developers, all while maintaining a secure, local-first, and FOSS-compliant approach.