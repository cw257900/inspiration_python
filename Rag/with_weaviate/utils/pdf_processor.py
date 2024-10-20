import os
import sys 
import datetime
from dotenv import load_dotenv
from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import CharacterTextSplitter,RecursiveCharacterTextSplitter


# Add the parent directory (or wherever "with_pinecone" is located) to the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from configs import configs


load_dotenv()

# Set API keys and Weaviate URL from environment variables


# Function to split the extracted text into chunks for better embedding
def get_chunked_doc(pdf_file_path):
    
    if not pdf_file_path or not os.path.exists(pdf_file_path):
        raise ValueError(f"Invalid PDF file path: {pdf_file_path}")
   
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200,
        length_function=len
    )
    docs = PyPDFLoader(pdf_file_path).load_and_split(text_splitter)
    
    return docs

def main ():
 
    pdf_file_path =  os.getenv("LOCAL_FILE_INPUT_PATH")
    doc = get_chunked_doc(pdf_file_path)
    print(f"1. Number of chunks from pdf: {len(doc)}")


if __name__ == "__main__":
    main()