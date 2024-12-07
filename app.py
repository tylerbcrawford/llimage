import os
import logging
from flask import Flask, render_template, request, send_file
import pdfplumber
from pdf2image import convert_from_path
from PIL import Image
import pytesseract
import io
import uuid

# === Logging Setup ===
if not os.path.exists('logs'):
    os.makedirs('logs', exist_ok=True)

logging.basicConfig(
    filename='logs/LLiMage.log',
    filemode='a',
    format='%(asctime)s - %(levelname)s - %(message)s',
    level=logging.DEBUG
)

console_handler = logging.StreamHandler()
console_handler.setLevel(logging.DEBUG)
logging.getLogger('').addHandler(console_handler)

logging.info("LLiMage application started.")

app = Flask(__name__)

# === Configuration ===
TESSERACT_CMD = "tesseract"  # Ensure it's in PATH or update path if needed
pytesseract.pytesseract.tesseract_cmd = TESSERACT_CMD

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@app.route('/process', methods=['POST'])
def process_pdf():
    # Check if a file is uploaded
    if 'file' not in request.files:
        logging.error("No file part in request.")
        return "No file uploaded.", 400

    pdf_file = request.files['file']
    if pdf_file.filename == '':
        logging.error("Empty filename received.")
        return "No file selected.", 400

    # Save PDF temporarily
    pdf_filename = f"temp_{uuid.uuid4()}.pdf"
    pdf_file.save(pdf_filename)
    logging.info(f"PDF saved as {pdf_filename}")

    # Extract text and images
    try:
        output_text = process_document(pdf_filename)
    except Exception as e:
        logging.exception("Error processing the PDF.")
        return f"Error processing the PDF: {e}", 500
    finally:
        # Clean up temporary file
        if os.path.exists(pdf_filename):
            os.remove(pdf_filename)

    # Create a text file to send back
    result_filename = f"result_{uuid.uuid4()}.txt"
    with open(result_filename, 'w', encoding='utf-8') as f:
        f.write(output_text)

    logging.info(f"Processing complete. Result saved in {result_filename}")

    return send_file(result_filename, as_attachment=True, mimetype='text/plain', download_name='LLiMage_output.txt')

def process_document(pdf_path):
    """
    Process the PDF:
    1. Extract text from pages
    2. Extract images from pages
    3. For each image, run OCR and produce a basic description
    4. Combine all text + image descriptions into a single text output
    """
    logging.debug("Starting document processing.")
    text_output = []
    with pdfplumber.open(pdf_path) as pdf:
        num_pages = len(pdf.pages)
        for i, page in enumerate(pdf.pages, start=1):
            logging.debug(f"Processing page {i}/{num_pages}")
            # Extract text
            page_text = page.extract_text() or ""
            text_output.append(f"=== Page {i} Text ===\n{page_text}\n")

            # Convert page to image(s)
            page_images = convert_from_path(pdf_path, first_page=i, last_page=i)
            for img_index, img in enumerate(page_images, start=1):
                logging.debug(f"OCR on page image {i}-{img_index}")
                # Convert to a pillow image in RGB
                img = img.convert('RGB')

                # OCR the image
                ocr_text = pytesseract.image_to_string(img).strip()

                if ocr_text:
                    description = f"=== Page {i} Image {img_index} Description ===\nThis image contains text:\n{ocr_text}\n"
                else:
                    description = f"=== Page {i} Image {img_index} Description ===\nThis appears to be an image or chart, but no readable text was found.\n"

                text_output.append(description)

    full_text = "\n".join(text_output)
    logging.debug("Document processing complete.")
    return full_text

if __name__ == '__main__':
    app.run(debug=True)
