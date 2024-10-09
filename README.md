echo "# inspiration_python" >> README.md
git init
git add README.md
git commit -m "first commit"
git branch -M main
git remote add origin https://github.com/cw257900/inspiration_python.git
git push -u origin main

pip install pdfminer.six

Recommendation Based on  Needs:
    For Text Extraction: Use PDFMiner.six or PyMuPDF.
    For Tables: Camelot and Tabula-py are specialized for tables.
    For Images: PyMuPDF and pdfplumber are better suited for image extraction.
    For Comprehensive Parsing (text, images, and tables): pdfplumber or PyMuPDF is the most versatile option.