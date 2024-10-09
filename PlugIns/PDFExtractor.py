
import fitz  # PyMuPDF

# Extract text using PyMuPDF
def extract_text_pymupdf(pdf_file):
    document = fitz.open(pdf_file)
    text = ''
    for page in document:
        text += page.get_text("text")
    return text

# Extract images using PyMuPDF
def extract_images_pymupdf(pdf_file):
    images = []
    document = fitz.open(pdf_file)
    for page_num in range(len(document)):
        page = document[page_num]
        image_list = page.get_images(full=True)
        for image in image_list:
            xref = image[0]
            base_image = document.extract_image(xref)
            image_bytes = base_image["image"]
            images.append(image_bytes)
    return images

pdf_file = 'pdf-sample.pdf'
text = extract_text_pymupdf(pdf_file)
images = extract_images_pymupdf(pdf_file)

print(text)
# Optionally, save the images
