import fitz  # PyMuPDF
import json
import base64
import os

def extract_pdf_to_json(file_path):
    doc = fitz.open(file_path)
    pdf_data = {"pages": []}

    print(f"Processing {file_path}, Total pages: {doc.page_count}")

    for page_num in range(doc.page_count):
        page = doc.load_page(page_num)
        text = page.get_text("text")

        print(f"Page {page_num + 1}: {text[:100]}...")  # Print first 100 characters as a preview

        images = []

        # Extract images from the page
        for img in page.get_images(full=True):
            xref = img[0]  # XREF index of the image
            base_image = doc.extract_image(xref)
            image_bytes = base_image["image"]
            image_base64 = base64.b64encode(image_bytes).decode('utf-8')

            # Append image data with useful info
            images.append({
                "width": base_image["width"],
                "height": base_image["height"],
                "color_space": base_image["colorspace"],
                "base64": image_base64,
                "ext": base_image["ext"]
            })

        pdf_data["pages"].append({
            "page_number": page_num + 1,
            "text": text,
            "images": images
        })

    return pdf_data  # Return the dictionary, not a JSON string

def process_all_pdfs_in_folder(input_folder, output_folder):
    # Ensure output folder exists
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # Process each file in the input folder
    for filename in os.listdir(input_folder):
        if filename.endswith(".pdf"):  # Only process PDF files
            input_file_path = os.path.join(input_folder, filename)
            output_file_path = os.path.join(output_folder, f"{os.path.splitext(filename)[0]}.json")

            # Extract PDF content
            pdf_data = extract_pdf_to_json(input_file_path)

            # Save the extracted data to a JSON file
            with open(output_file_path, 'w', encoding='utf-8') as json_file:
                json.dump(pdf_data, json_file, indent=4)

            print(f"PDF content from {filename} has been extracted and saved to {output_file_path}")

# Set input and output folders
input_pdf_folder = "data/input_pdf"
output_json_folder = "data/output_json"

# Process all PDFs in the input folder
process_all_pdfs_in_folder(input_pdf_folder, output_json_folder)
