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
import config
import vectordb_init  # Assuming this is a module where init() is defined

load_dotenv()

# Set API keys and Weaviate URL from environment variables
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
WEAVIATE_API_KEY = os.getenv("WEAVIATE_API_KEY")  # Weaviate API key
WEAVIATE_URL = config.WEAVIATE_URL
class_name =config.class_name

# manual specify file path for now 
pdf_file_path = config.LOCAL_FILE_INPUT_PATH


def vectordb_verify_data(client):

    collection_objects = client.data_object.get(class_name=class_name, limit=10)  # Adjust limit as needed

    """""
    # Print each object in the collection
    for obj in collection_objects['objects']:
        print(f"Object ID: {obj['id']}, Data: {obj['properties']}")
        
        # Optionally, print each property and its value in detail
        for prop, value in obj['properties'].items():
            print(f"Property: {prop}, Value: {value}")
    """



# Function to load text chunks into Weaviate
def vectordb_upload_pdf():
    try:
        # Initialize Weaviate client
        
        client = vectordb_init.init(class_name)

        print (f"1. input data_file = {pdf_file_path}")
        # Process PDF and upload chunks to Weaviate
        text_chunks = pdf_processor.get_text_chunks(pdf_file_path)
       
        for idx, chunk in enumerate(text_chunks):
            # Prepare the object to upload
            data_object = {
                "pdf_name": pdf_file_path,
                "pdf_content": chunk,
                "pdf_chunk_id": f"chunk_{idx}"
            }
            # Create data object in Weaviate
            client.data_object.create(data_object, class_name)

        print ("2. Data uploaded to Weaviate")
        vectordb_verify_data(client)


    except Exception as e:
        print(f"Error invectordb_create.py Error retrieving class schema: {e}")
        traceback.print_exc()

    finally:
        None
             
vectordb_upload_pdf()