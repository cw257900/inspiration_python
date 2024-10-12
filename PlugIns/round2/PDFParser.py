import fitz  # PyMuPDF
import os

import pdfplumber

from dotenv import load_dotenv
# Load environment variables
load_dotenv()

# Directories from environment variables
OUTPUT_DIR = os.getenv("OUTPUT_DIR")
PDF_PATH = os.getenv("PDF_FILE_INPUT_DIR")
VALIDATION_TMP_DIR = os.getenv("VALIDATION_TMP_DIR")



# Ensure that VALIDATION_TMP_DIR is valid
print(VALIDATION_TMP_DIR)
if not VALIDATION_TMP_DIR:
    raise ValueError("VALIDATION_TMP_DIR is not set properly!")
    

class PDFParser:
    """Class responsible for extracting text, tables, and images from a PDF."""
    
    def __init__(self, pdf_path):
        self.pdf_path = pdf_path

    def parse_pdf(self):
        """Parse PDF and return structured content for further processing."""
        doc = fitz.open(self.pdf_path)
        content = []

        for page_number in range(len(doc)):
            page_content = {"page_number": page_number + 1, "content": []}
            page = doc.load_page(page_number)
            text_blocks = page.get_text("dict")["blocks"]

            images = page.get_images(full=True)

            # Extract text blocks
            for block in text_blocks:
                if block['type'] == 0:  # Text block
                    text = "\n".join([line["spans"][0]["text"] for line in block["lines"]])
                    if text:
                        page_content["content"].append({"type": "text", "data": text})

            if text:
                # Save text content to a file
                text_file_path = os.path.join(VALIDATION_TMP_DIR, f"page_{page_number + 1}_text.txt")
                with open(text_file_path, 'w', encoding='utf-8') as text_file:
                    text_file.write(text)

            print(f"PDFParser.py {text_file}  {page_number + 1} saved to {VALIDATION_TMP_DIR}")
            print()

       
            # Extract images
            for img_index, img in enumerate(images):
                xref = img[0]
                base_image = doc.extract_image(xref)
                image_data = base_image["image"]
                image_ext = base_image["ext"]
                image_info = {"data": image_data, "ext": image_ext}
                page_content["content"].append({"type": "image", "data": image_info})

           

            # Extract tables using pdfplumber
            with pdfplumber.open(self.pdf_path) as pdf:
                pdf_page = pdf.pages[page_number]
                tables = pdf_page.extract_tables()
                for table in tables:
                    page_content["content"].append({"type": "table", "data": table})


            content.append(page_content)

        return content


def main_single_file(filename):
    """Main function to parse a single PDF file and return content."""
    pdf_path = os.path.join(PDF_PATH, filename)
    
    # Parse the PDF and get the content (without embedding or saving yet)
    pdf_parser = PDFParser(pdf_path)
    parsed_content = pdf_parser.parse_pdf()

    # Return the parsed content to be used later by the embedder or saving logic
    print ("PDFParser.main_single_file ****   Done")
    return parsed_content





if __name__ == "__main__":
    # Replace 'your_pdf_file.pdf' with the specific filename you want to process
    filename = 'embedded-images-tables.pdf'  # Update this to the actual filename

    content = main_single_file(filename)

    
    #Generate the output filename based on the input filename
    # Extract the base name (without extension) and append "_output.txt"
    base_filename = os.path.splitext(os.path.basename(filename))[0]
    output_filename = f"{base_filename}_output.txt"

    # Full path for the output file
    VALIDATION_TMP_FILE = os.path.join(VALIDATION_TMP_DIR, output_filename)

  
    
    # Writing the content to the output file
    with open(VALIDATION_TMP_FILE, 'w') as file:
        file.write(f"Filename: {filename}\nContent: {content}\n")
