from fpdf import FPDF
import base64
from PIL import Image
from io import BytesIO
import json
import os

# Function to fix base64 padding
def fix_base64_padding(base64_string):
    # Add padding if necessary (base64 string length should be a multiple of 4)
    return base64_string + "=" * (-len(base64_string) % 4)

# Function to convert JSON to PDF
def convert_json_to_pdf(json_file_path, output_pdf_path):
    # Load JSON data from file
    with open(json_file_path, 'r') as json_file:
        json_data = json.load(json_file)

    # Initialize PDF object
    pdf = FPDF()

    # Add a Unicode font that supports special characters
    pdf.add_font("DejaVu", "", "lib/dejavu-sans/DejaVuSans.ttf")
    pdf.set_font("DejaVu", size=12)

    # Loop through the JSON structure and add each page to the PDF
    for page in json_data["pages"]:
        pdf.add_page()

        # Add the text from the JSON data
        pdf.multi_cell(0, 10, page["text"])

        # Loop through the images in the page and add them to the PDF
        for image_data in page["images"]:
            try:
                # Fix the padding issue
                base64_image = fix_base64_padding(image_data["base64"])

                # Decode the base64 image data
                image_content = base64.b64decode(base64_image)

                # Create an image from the base64 string
                image_stream = BytesIO(image_content)
                image = Image.open(image_stream)

                # Insert the image into the PDF
                pdf.image(image, x=10, y=pdf.get_y(), w=image_data["width"] / 10, h=image_data["height"] / 10)

            except (OSError, base64.binascii.Error) as e:
                print(f"Error processing image in {json_file_path}: {e}")

        # Add some space between images
        pdf.ln(10)

    # Output the generated PDF
    pdf.output(output_pdf_path)
    print(f"PDF created: {output_pdf_path}")

# Function to process all JSON files in a folder
def process_all_json_files(input_folder, output_folder):
    # Ensure the output folder exists
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # Process each JSON file in the input folder
    for filename in os.listdir(input_folder):
        if filename.endswith(".json"):  # Only process JSON files
            input_file_path = os.path.join(input_folder, filename)
            output_file_path = os.path.join(output_folder, f"{os.path.splitext(filename)[0]}.pdf")

            # Convert JSON to PDF
            convert_json_to_pdf(input_file_path, output_file_path)

# Set input and output folders
input_json_folder = "data/output_json"
output_pdf_folder = "data/revert_pdf_pymupdf"

# Process all JSON files in the input folder
process_all_json_files(input_json_folder, output_pdf_folder)
