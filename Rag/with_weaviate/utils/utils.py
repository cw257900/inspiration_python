import weaviate
import os
import sys
import weaviate
from dotenv import load_dotenv
from weaviate.exceptions import WeaviateBaseError
import inspect

# Add the parent directory (or wherever "with_pinecone" is located) to the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from vector_stores import vector_store as vector_store
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


def class_exists(client, class_name):
    """Check if a class already exists in the Weaviate schema."""
    schema = client.schema.get()
    return any(cls['class'] == class_name for cls in schema.get('classes', []))


# Using context management if Weaviate client supports it
def reflect_weaviate_client():
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


def get_total_count(client, class_name):

    # Perform the aggregate query to get the count of objects
    result = client.query.aggregate(class_name).with_meta_count().do()

    # Extract the count from the response
    count = result['data']['Aggregate']['PDF_COLLECTION'][0]['meta']['count']
    print(f"Total records in {class_name}: {count}")


def main():
    #reflect_weaviate_client()

    get_total_count(vector_store.client, class_name)
  
   

if __name__ == "__main__":
    print ("weaviate version:", weaviate.__version__)
    print ("weaviate url:", WEAVIATE_URL)
    main()