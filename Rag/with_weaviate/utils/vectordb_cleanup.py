
import os
import weaviate
import weaviate
import sys

# Add the parent directory (or wherever "with_pinecone" is located) to the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from vector_stores import vector_stores as vector_store
from configs import configs
import utils

import logging
# Configure logging for development
logging.basicConfig(
    format='%(asctime)s - %(levelname)s - %(message)s',
    level=logging.INFO,  # Changed from WARNING to INFO
    handlers=[
        logging.StreamHandler()  # This ensures output to console
    ]
)


from dotenv import load_dotenv
load_dotenv()

# Set API keys and Weaviate URL from environment variables
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
WEAVIATE_URL = os.getenv("WEAVIATE_URL")  # WEAVIATE_URL
WEAVIATE_STORE_NAME = configs.WEAVIATE_STORE_NAME  # WEAVIATE_STORE_NAME

# Delete all objects in the class without deleting the schema
def delete_objects(client, class_name): 
    # Delete all objects in the class without deleting the schema
    result = client.collections.delete(class_name) 
    logging.info(f" === *cleanup.py {class_name} deleted")
   

def main():

    client = vector_store.create_client()
    collection_for_deletion = "PDF_COLLECTION"
    delete_objects(client, collection_for_deletion)

    utils.get_total_object_count(client)

    vector_store.close_client(client)
    


if __name__ == "__main__":
    main()