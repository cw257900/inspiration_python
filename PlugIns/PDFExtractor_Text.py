import re
import PyPDF2

from pdfminer.high_level import extract_pages, extract_text 


text = extract_text("example_files/pdf-sample.pdf")
print(text)
