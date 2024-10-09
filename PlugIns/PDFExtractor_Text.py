import re
import PyPDF2

from pdfminer.high_level import extract_pages, extract_text 


text = extract_text("pdf-sample-text.pdf")
print(text)
