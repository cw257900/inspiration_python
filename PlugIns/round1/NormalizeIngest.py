import fitz  # PyMuPDF
import json
import base64
import os

# Extract text using PyMuPDF
def extract_text_pymupdf(page):
    return page.get_text("text")

# Extract images using PyMuPDF
def extract_images_pymupdf(document, page_num):
    images = []
    page = document.load_page(page_num)  # Load the page
    image_list = page.get_images(full=True)  # Get a list of images
    
    for img in image_list:
        xref = img[0]  # The image reference number
        base_image = document.extract_image(xref)
        image_bytes = base_image["image"]
        image_ext = base_image["ext"]  # Get image extension (png, jpeg, etc.)
        
        # Encode image in base64 for JSON serialization
        image_base64 = base64.b64encode(image_bytes).decode("utf-8")
        
        images.append({
            "page": page_num + 1,  # Page number (1-based)
            "image_data": image_base64,
            "image_ext": image_ext  # Image format
        })
    
    return images

# Extract metadata from the PDF
def extract_metadata_pymupdf(document):
    return document.metadata

# Extract text, images, and metadata, and structure as JSON
def extract_pdf_pymupdf(file_path):
    document = fitz.open(file_path)
    num_pages = document.page_count
    
    # Extract metadata
    metadata = extract_metadata_pymupdf(document)
    
    # Initialize JSON structure
    pdf_data = {
        "metadata": metadata,
        "pages": []
    }
    
    # Loop through each page and extract text and images
    for page_num in range(num_pages):
        page = document.load_page(page_num)  # Load the current page
        
        # Extract text
        text = extract_text_pymupdf(page)
        
        # Extract images
        images = extract_images_pymupdf(document, page_num)
        
        # Append the data for the current page
        pdf_data["pages"].append({
            "page_number": page_num + 1,
            "text": text,
            "images": images
        })
    
    return pdf_data

# Save extracted PDF content as JSON
def save_pdf_as_json(data, output_file):
    with open(output_file, 'w', encoding='utf-8') as json_file:
        json.dump(data, json_file, indent=4)

# Main process
def main():
    file_name = 'input_pdf/all-number-table.pdf'  # Replace with your PDF file
    output_json_file = 'output_json/all-number-table.json'  # Output JSON file
    
    # Extract data from PDF
    extracted_data = extract_pdf_pymupdf(file_name)
    
    # Save extracted data to JSON
    save_pdf_as_json(extracted_data, output_json_file)
    
    print(f"PDF content extracted and saved as {output_json_file}")

# Run the script
if __name__ == "__main__":
    main()
