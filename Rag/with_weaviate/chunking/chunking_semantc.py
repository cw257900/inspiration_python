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
