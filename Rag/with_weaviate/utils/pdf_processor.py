import os
import traceback 
#from PyPDF2 import PdfReader
from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import CharacterTextSplitter,RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings


# Function to read PDF and extract text from all pages
def get_pdf_text(pdf_file_path):
    """
    with open(pdf_file_path, 'rb') as file:
        reader = PdfReader(file)
        text = ""
        # Iterate through all pages and extract text
        for page_num in range(len(reader.pages)):
            page = reader.pages[page_num]
            text += page.extract_text()
    return text
   """
   
# Function to split the extracted text into chunks for better embedding
def get_checked_doc(pdf_file_path):
    

    if not pdf_file_path or not os.path.exists(pdf_file_path):
        raise ValueError(f"Invalid PDF file path: {pdf_file_path}")

    text = get_pdf_text(pdf_file_path)
   
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200,
        length_function=len
    )
    docs = PyPDFLoader(pdf_file_path).load_and_split(text_splitter)
    print(f"1. Number of chunks from pdf: {len(docs)}")
    return docs