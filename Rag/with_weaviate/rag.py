import os, sys 
import weaviate
from vector_stores import vector_stores 
import vectordb_create_schema as create_schema

import vectordb_create as create_data

# Add the parent directory (or wherever "with_pinecone" is located) to the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from vector_stores import vector_stores as vector_store
from utils import utils
from configs import configs
from dotenv import load_dotenv

load_dotenv()

# Set API keys and Weaviate URL from environment variables
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
WEAVIATE_URL = os.getenv("WEAVIATE_URL")  # WEAVIATE_URL
pdf_file_path = os.getenv("LOCAL_FILE_INPUT_PATH")
class_name = configs.WEAVIATE_STORE_NAME  # WEAVIATE_STORE_NAME
class_description = configs.WEAVIATE_STORE_DESCRIPTION



def load_data_embed_weaviate():
    # Initialize the Weaviate client
    client = vector_stores.create_client()
    if (not client.is_connected()): 
        print (client.is_connected)
        client.connect()

    class_name = 'PDF_COLLECTION'
    class_description = 'PDF Collection Weaviate embedding'
    print('with customized embedding ', class_name)

    #use weaviate to embed
    create_schema.create_collection_embed_with_weaviate(client, class_name=class_name,class_description=class_description)
    create_data.psert_chunks_to_store(pdf_file_path, vector_store, class_name)
        

    vector_stores.close_client(client)

def load_data_embed_outside():
    
    # Initialize the Weaviate client
    client = vector_stores.create_client()
    if (not client.is_connected()): 
        print (client.is_connected)
        client.connect()

    class_name = 'PDF_COLLECTION_EMBEDDING'
    class_description = 'PDF Collection with pre-embedding'
    print('with customized embedding ', class_name)


    #embed outside
    create_schema.create_collection_embed_customized(client, class_name=class_name, class_description=class_description)

    vector_stores.close_client(client)

if __name__ == "__main__":
    load_data_embed_weaviate()