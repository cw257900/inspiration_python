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


def creat_class_oct (client, class_name, class_description):
    
    print ("requested to create new collection: ", class_name)
    try:
      
        collection = client.collections.create( #this is v4 weaviate
            name=class_name,
            description=class_description,
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
                ),
                wvc.config.Property (
                    name="processing_dt",
                    data_type=wvc.config.DataType.DATE,
                )
            ],
            # Configure the vector index
            vectorizer_config=None,  # We'll provide our own vectors
            # Configure the vector index
            vector_index_config=wvc.config.Configure.VectorIndex.hnsw(  # Or `flat` or `dynamic`
                distance_metric=wvc.config.VectorDistances.COSINE,
                quantizer=wvc.config.Configure.VectorIndex.Quantizer.bq(),
            ),
            generative_config=None,
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
    client = vector_store.create_client()
    if (not client.is_connected()): 
        print (client.is_connected)
        client.connect()
    #create_class_with_vectorizer_and_dims(client, class_name=class_name)
    #create_class_with_vectorizer_index_and_dims(client, class_name=class_name, class_description=class_description)
    creat_class_oct(client, class_name=class_name, class_description=class_description)
    vector_store.close_client(client)
