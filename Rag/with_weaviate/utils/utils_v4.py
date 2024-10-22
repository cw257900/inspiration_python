import weaviate
import os
import sys
import weaviate
from dotenv import load_dotenv
from weaviate.exceptions import WeaviateBaseError
import inspect
import asyncio

# Add the parent directory (or wherever "with_pinecone" is located) to the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import vector_stores.vector_stores as vector_store

import configs.configs as configs

# Load environment variables
load_dotenv()

# Get environment variables
# Set API keys and Weaviate URL from environment variables
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
WEAVIATE_API_KEY = os.getenv("WEAVIATE_API_KEY")  # Weaviate API key
WEAVIATE_URL = os.getenv("WEAVIATE_URL")  # WEAVIATE_URL
pdf_file_path =  os.getenv("LOCAL_FILE_INPUT_PATH")
class_name =configs.WEAVIATE_STORE_NAME
class_description =configs.WEAVIATE_STORE_DESCRIPTION

from weaviate.classes.config import ConsistencyLevel

def get_object_by_uuid():

    client = weaviate.connect_to_local()
    collection = client.collections.get("PDF_COLLECTION")

    questions = client.collections.get("PDF_COLLECTION").with_consistency_level(
        consistency_level=ConsistencyLevel.QUORUM
    )
    print(" ")
    response = collection.query.fetch_object_by_id("0f105783-ca15-52b1-81e8-eb18a09c808c")
    response = collection.query.fetch_object_by_id("0f105783-ca15-52b1-81e8-eb18a09")  #raise Exception :aise ValueError("Not valid 'uuid' or 'uuid' can not be extracted from value")

    print(response)
    print()
    print (response.properties['page_content'])
    print (response.properties['page_number'])
    print (response.properties['source'])

    client.close()
   

def get_object_by_class_name():

    client = vector_store.create_client()

    try:
        collection = client.collections.get("PDF_COLLECTION")
        response = collection.query.fetch_objects(
            # Object IDs are included by default with the `v4` client! :)
            limit=10
        )

        for o in response.objects:
            print(o.uuid)

       
        print(response)

        return response
    except Exception as e:
        print(f"Error querying object by UUID: {e}")
        return None

    vector_store.close_client(client) 

def main():
    get_object_by_uuid()

if __name__ == "__main__":
    main()
