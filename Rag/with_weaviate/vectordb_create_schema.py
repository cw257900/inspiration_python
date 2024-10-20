import os
import weaviate.classes as wvc
import weaviate
import sys

# Add the parent directory (or wherever "with_pinecone" is located) to the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from vector_stores import vector_store as vector_store
from utils import utils

from configs import configs
from dotenv import load_dotenv

load_dotenv()

# Set API keys and Weaviate URL from environment variables
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
WEAVIATE_URL = os.getenv("WEAVIATE_URL")  # WEAVIATE_URL
class_name = configs.WEAVIATE_STORE_NAME  # WEAVIATE_STORE_NAME
class_description = configs.WEAVIATE_STORE_DESCRIPTION
text2vec_model=configs.text2vec_model  


"""
This function is to create schema only
vector_create.py file upload data with customized embedding objects
"""
def create_class(client, class_name):
    properties = [
            {"name": "source", "dataType": ["string"], "indexInverted": True, "indexSearchable": True},
            {"name": "pdf_content", "dataType": ["text"], "indexInverted": True,"indexSearchable": True},
            {"name": "page_number", "dataType": ["int"], "indexInverted": True,"indexSearchable": True},
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
    


def create_class_with_vectorizer_and_dims(client, class_name, model="text-embedding-3-large", dimensions=1024):
    """ 
    text-embedding-3-large, dimensions: 3072
    text-embedding-ada-002, dimensions: 1536
    text-embedding-3-small, dimensions: 768
    """
    if utils.class_exists(client, class_name):
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

def create_class_with_vectorizer_index_and_dims(client, class_name, class_description, model=text2vec_model):
    """ 
    text-embedding-3-large, dimensions: 3072
    text-embedding-ada-002, dimensions: 1536
    text-embedding-3-small, dimensions: 1536
    """

    print ("requested to create new collection: ", class_name, " with vectorizer: ", " model: ", model)
    try:
      
        collection = client.collections.create( #this is v4 weaviate
            name=class_name,
            description=class_description,
            vectorizer_config=wvc.config.Configure.Vectorizer.text2vec_openai(
                model=text2vec_model
            ),    # Set the vectorizer to "text2vec-openai" to use the OpenAI API for vector-related operations
            generative_config=wvc.config.Configure.Generative.cohere () ,            # Set the generative module to "generative-cohere" to use the Cohere API for RAG
            properties=[
                wvc.config.Property(
                    name="page_content",
                    data_type=wvc.config.DataType.TEXT,
                ),
                wvc.config.Property(
                    name="page_number",
                    data_type=wvc.config.DataType.INT,
                ),
                wvc.config.Property(
                    name="source",
                    data_type=wvc.config.DataType.TEXT,
                )
            ],
            # Configure the vector index
            vector_index_config=wvc.config.Configure.VectorIndex.hnsw(  # Or `flat` or `dynamic`
                distance_metric=wvc.config.VectorDistances.COSINE,
                quantizer=wvc.config.Configure.VectorIndex.Quantizer.bq(),
            ),
            # Configure the inverted index
            inverted_index_config=wvc.config.Configure.inverted_index(
                index_null_state=True,
                index_property_length=True,
                index_timestamps=True,
            ),
        )

    finally:
        
        client.close()


   
# Example usage
if __name__ == "__main__":

    #client = vector_store.client
    
    # Initialize the Weaviate client
    client = weaviate.connect_to_local(
        headers={
            "X-OpenAI-Api-Key": OPENAI_API_KEY # Replace with your inference API key
        }
    )
    
    #create_class_with_vectorizer_and_dims(client, class_name=class_name)
    create_class_with_vectorizer_index_and_dims(client, class_name=class_name, class_description=class_description)
