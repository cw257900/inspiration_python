import os
import traceback 
import uuid as uuid_lib 
from PyPDF2 import PdfReader
from dotenv import load_dotenv
from langchain.text_splitter import CharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
import weaviate
from weaviate.classes.init import Auth
from weaviate.exceptions import WeaviateBaseError
from utils import pdf_processor  
import sys
# Add the parent directory (or wherever "with_pinecone" is located) to the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from vector_stores import vector_store as pinecone_vector_store
from embeddings import openai_embeddings as embeddings
from configs import configs

import datetime
import asyncio

load_dotenv()



# Add the parent directory (or wherever "with_pinecone" is located) to the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from vector_stores import vector_store as vector_store
from embeddings import openai_embeddings as embeddings
from configs import configs


# Load environment variables
load_dotenv()

# Set API keys and Weaviate URL from environment variables
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
WEAVIATE_URL = os.getenv("WEAVIATE_URL")  # WEAVIATE_URL
WEAVIATE_STORE_NAME = os.getenv("WEAVIATE_STORE_NAME")  # WEAVIATE_STORE_NAME

headers = {
    "X-OpenAI-Api-Key": OPENAI_API_KEY
}  # OpenAI API key for vectorization




client = weaviate.Client(WEAVIATE_URL, additional_headers=headers)


print(f"0.2. vector_store client")