import os
import traceback 
from dotenv import load_dotenv
from dotenv import load_dotenv
from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import CharacterTextSplitter,RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings

load_dotenv()


# Function to split the extracted text into chunks for better embedding
def get_checked_doc(pdf_file_path):
    
    if not pdf_file_path or not os.path.exists(pdf_file_path):
        raise ValueError(f"Invalid PDF file path: {pdf_file_path}")
   
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200,
        length_function=len
    )
    docs = PyPDFLoader(pdf_file_path).load_and_split(text_splitter)
    print(f"1. Number of chunks from pdf: {len(docs)}")
    return docs

def main ():

    pdf_file_path = os.env("LOCAL_FILE_INPUT_PATH")
    print (pdf_file_path)
    doc = get_checked_doc(pdf_file_path)
    print (pdf_file_path)
    

def __main__():
    main()