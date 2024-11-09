import weaviate
import os
import sys
import weaviate
from weaviate.classes.query import Filter
from dotenv import load_dotenv
from weaviate.exceptions import WeaviateBaseError
import requests
import inspect

# Add the parent directory (or wherever "with_pinecone" is located) to the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import vector_stores.vector_stores as vector_stores

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


# Function to check if a collection (class) exists
def check_collection_exists(client, collection_name: str) -> bool:
    try:
        return client.collections.exists(collection_name)
    except Exception as e:
        print(f"Error checking if collection exists: {e}")
        return False

# Using context management if Weaviate client supports it
def reflect_weaviate_client(vector_store):
    # Perform your operations with the client here
    client = vector_store.client

    attributes = dir(client)
    for attr in attributes:
        #print(attr)
        pass

    print()

    batch = client.batch
    attributes = dir(batch)
    for attr in attributes:
        print(attr)

    #print (help(client.collections))
    client.batch.dynamic=True

    print (client.batch)
    methods = [func for func in dir(client.batch) if callable(getattr(client.batch, func)) and not func.startswith("__")]

    print()
    print("Methods of client.batch:")
    for method in methods:
        print(method)

    # Alternatively, use inspect to get more detailed information
    print("\nDetailed method info from inspect:")
    for name, method in inspect.getmembers(client.batch, predicate=inspect.isfunction):
        print(f"Method: {name}, Callable: {method}")

    del client # as there might be underline leak; and client.close() doesn't work

def get_total_object_count(client) -> int:
    """
    Get the total count of objects in the Weaviate instance.

    Args:
        client: Weaviate client instance (to get the base URL).

    Returns:
        int: The total count of objects, or 0 if an error occurs.
    """
    try:
        # Construct the URL for the objects endpoint
        url = f"{client._connection.url}/v1/objects/"
        
        # Make the GET request to get the total object count
        response = requests.get(url)
        response.raise_for_status()  # Raise an error for non-200 status codes
        
        # Extract the total count from the JSON response
        data = response.json()
        total_count = data.get("totalResults", 0)
        return total_count
    
    except requests.exceptions.RequestException as e:
        print(f"Error while getting total object count: {e}")
        return 0

# Delete all objects in the class without deleting the schema
def delete_objects(client, class_name): 
    # Delete all objects in the class without deleting the schema
    result = client.collections.delete(class_name) 
    print(result)

def delete_by_uuid (client, class_name, uuid) :

    collection = client.collections.get(class_name)
    collection.data.delete_by_id(
        uuid
    )
    

def main():
    print ("weaviate version:", weaviate.__version__)
    print ("weaviate url:", WEAVIATE_URL)
    print ("Collection ", class_name)

    client = vector_stores.create_client()
    collection = client.collections.get(class_name)

    delete_objects(client, class_name)
    #delete_by_uuid (client, class_name=class_name, uuid='e2a41e19-f9bf-58e6-b7fc-664d7391e621')


    vector_stores.close_client(client)
  
   

if __name__ == "__main__":

    main()