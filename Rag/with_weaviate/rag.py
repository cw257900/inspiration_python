import os, sys 
import weaviate

import uuid
import time
import os
import sys
import base64
from sentence_transformers import SentenceTransformer
from PIL import Image
import pytesseract
import requests
from pathlib import Path 


# Add the parent directory (or wherever "with_pinecone" is located) to the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from vector_stores import vector_stores as vector_store
from utils import utils
from configs import configs
from dotenv import load_dotenv
load_dotenv()


import warnings
warnings.filterwarnings("ignore", category=ResourceWarning)


# Set API keys and Weaviate URL from environment variables
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
WEAVIATE_URL = os.getenv("WEAVIATE_URL")  # WEAVIATE_URL
pdf_file_path = os.getenv("LOCAL_FILE_INPUT_PATH")
class_name = configs.WEAVIATE_STORE_NAME  # WEAVIATE_STORE_NAME
class_description = configs.WEAVIATE_STORE_DESCRIPTION




import base64
from PIL import Image
import pytesseract
from pathlib import Path

from weaviate.util import generate_uuid5





   






