import os
import weaviate.classes as wvc
import weaviate
import sys
from sentence_transformers import SentenceTransformer

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
class_name = configs.WEAVIATE_STORE_NAME  # WEAVIATE_STORE_NAME
class_description = configs.WEAVIATE_STORE_DESCRIPTION
text2vec_model=configs.text2vec_model  


import warnings
warnings.filterwarnings("ignore", category=ResourceWarning)

    

# weaviate's vector - openai's , v3 code, deprecated 
def create_collection_embed_with_weaviate(client, class_name, class_description=None, model="text-embedding-3-large", dimensions=1024):
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


##embeded outstide 
def create_collection(client, class_name, class_description=None,  dimension = 1536):
    """ 
    text-embedding-3-large, dimensions: 3072
    text-embedding-ada-002, dimensions: 1536
    text-embedding-3-small, dimensions: 1536

    vectorizer_config=wvc.config.Configure.Vectorizer.text2vec_openai( model=text2vec_model)  
    vectorizer_config=wvc.config.Configure.Vectorizer.text2vec_transformers( ) 
    """
   

    if utils.check_collection_exists(client, class_name):
        print(f"Collection '{class_name}' already exists.")
        return

    try:
        collection = client.collections.create( #this is v4 weaviate
            name=class_name,
            description=class_description,
            # Set the vectorizer to "text2vec-openai" to use the OpenAI API for vector-related operations
            vectorizer_config=wvc.config.Configure.Vectorizer.text2vec_openai()  ,
            # Set the generative module to "generative-cohere" to use the Cohere API for RAG
            generative_config=wvc.config.Configure.Generative.cohere () ,        
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

        print (f" === collection: {class_name} created ")
        print ()
        #print(collection)

    finally:
        
        client.close()




   
# Example usage
if __name__ == "__main__":

    #client = vector_store.client
    
    # Initialize the Weaviate client
    client = vector_store.create_client()
    if (not client.is_connected()): 
        print (client.is_connected)
        client.connect()


    #without vector, use outside ; default vector = None 
    create_collection(client, class_name=class_name,class_description=class_description)


    vector_store.close_client(client)
