import os
import traceback
import datetime
import asyncio
import weaviate
from weaviate.exceptions import WeaviateBaseError
import weaviate
import sys

# Add the parent directory (or wherever "with_pinecone" is located) to the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from vector_stores import vector_store as vector_store
from embeddings import openai_embeddings as embeddings
from utils import pdf_processor
from configs import configs

from dotenv import load_dotenv

load_dotenv()

# Set API keys and Weaviate URL from environment variables
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
WEAVIATE_URL = os.getenv("WEAVIATE_URL")  # WEAVIATE_URL
WEAVIATE_STORE_NAME = configs.WEAVIATE_STORE_NAME  # WEAVIATE_STORE_NAME

headers = {
    "X-OpenAI-Api-Key": OPENAI_API_KEY
}  # OpenAI API key for vectorization

def create_class(client, class_name):
    properties = [
            {"name": "source", "dataType": ["string"], "indexInverted": True},
            {"name": "pdf_content", "dataType": ["text"], "indexInverted": True},
            {"name": "page_number", "dataType": ["int"], "indexInverted": True}
    ]
    class_schema = {
        "class": class_name,
        "properties": properties,
        "description": "Collection for PDF documents with embeddings built before inserting into Weaviate"
    }


    try:
        # Get the existing schema
        schema = client.schema.get()

        # Check if the class "test" already exists
        class_exists = any(cls['class'] == class_name for cls in schema['classes'])

        if not class_exists:
            client.schema.create_class(class_schema)
            print("Class created successfully.")

        else:
            print("Class already exists.")

    except Exception as e:
        print(f"Error: {e}")

    finally:
        # client.close()
        pass
    
   
def delete_class(client, class_name):
    client.schema.delete_class(class_name)

def create_vector_class(client, class_name, properties, model="text-embedding-3-large", dimensions=1024):
    """Create a vectorized class in Weaviate with specified properties and OpenAI vectorizer."""
    
    class_schema = {
        "class": class_name,
        "properties": properties,
        "vectorizer": "text2vec-openai",
        "moduleConfig": {
            "text2vec-openai": {
                "model": model,
                "type": "text",
                "vectorizeClassName": False
            }
        },
        "vectorIndexConfig": {
            "dimensions": dimensions  # Set vector dimensions
        }
    }

    try:
        client.schema.create_class(class_schema)
        print(f"Class '{class_name}' created successfully!")

    except Exception as e:
        print(f"Error creating class '{class_name}': {e}")

    finally:
        client.close()



def class_exists(client, class_name):
    """Check if a class already exists in the Weaviate schema."""
    schema = client.schema.get()
    return any(cls['class'] == class_name for cls in schema.get('classes', []))



def init_schema(client, class_name):
    """Initialize the schema with class creation based on the provided class name."""
    
    if class_exists(client, class_name):
        print(f"Class '{class_name}' already exists.")
        return client

    # Define class properties based on class name
    if class_name == "Movie":
        properties = [
            {"name": "title", "dataType": ["text"], "indexInverted": True,"indexSearchable": True},
            {"name": "overview", "dataType": ["text"], "indexInverted": True,"indexSearchable": True},
            {"name": "vote_average", "dataType": ["number"], "indexInverted": True,"indexSearchable": True},
            {"name": "genre_ids", "dataType": ["int[]"], "indexInverted": True,"indexSearchable": True},
            {"name": "release_date", "dataType": ["date"], "indexInverted": True, "indexSearchable": True},
            {"name": "tmdb_id", "dataType": ["int"], "indexInverted": True, }
        ]
    elif class_name in ["PDF_COLLECTIONS", "PDF_COLLECTION"]:
        properties = [
            {"name": "source", "dataType": ["string"], "indexInverted": True, "indexSearchable": True},
            {"name": "pdf_content", "dataType": ["text"], "indexInverted": True, "indexSearchable": True},
            {"name": "page_number", "dataType": ["int"], "indexInverted": True, "indexSearchable": True}
        ]
    else:
        print(f"Unknown class name: {class_name}")
        return client

    # Create class with vectorization enabled
    return create_vector_class(client, class_name, properties)

def init(class_name):

    """Initialize the Weaviate client and set up the schema for the specified class."""
    # Initialize the Weaviate client
    client = weaviate.Client(WEAVIATE_URL, additional_headers=headers)

    # Set up schema for the class
    init_schema(client, class_name)
    
    # Return the initialized client
    return client


# Example usage
if __name__ == "__main__":
    # Initialize and create vector schema for the class "PDF_Vector_Collection"
    
    #client = init(WEAVIATE_STORE_NAME)
    
    #create_class(client, class_name=WEAVIATE_STORE_NAME)


    client = weaviate.Client("http://localhost:8080")
    create_class(client, class_name=WEAVIATE_STORE_NAME)

    # create class with embeddings manually
    # create_class(client, class_name=configs.WEAVIATE_STORE_NAME) # embedding before data insert into db

    """
    delete_class(client, "PDF_COLLECTIONS")
    print( " *** deleted  ***")
  

    # Print the class names (collections)
    print("Existing collections (classes):")
    schema = client.schema.get()
    for cls in schema['classes']:
        print(f" - {cls['class']}")

    print()
    """


