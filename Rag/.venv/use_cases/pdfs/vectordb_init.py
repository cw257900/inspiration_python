import weaviate
import os
from dotenv import load_dotenv
import uuid
import config

# Load environment variables
load_dotenv()

# Set API keys and Weaviate URL from environment variables
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
WEAVIATE_URL = os.getenv("WEAVIATE_URL")

headers = {
    "X-OpenAI-Api-Key": OPENAI_API_KEY
}  # OpenAI API key for vectorization

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

        return client 
    
    except Exception as e:
        print(f"Error creating class '{class_name}': {e}")

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
            {"name": "title", "dataType": ["text"], "indexInverted": True},
            {"name": "overview", "dataType": ["text"], "indexInverted": True},
            {"name": "vote_average", "dataType": ["number"], "indexInverted": True},
            {"name": "genre_ids", "dataType": ["int[]"], "indexInverted": True},
            {"name": "release_date", "dataType": ["date"], "indexInverted": True},
            {"name": "tmdb_id", "dataType": ["int"], "indexInverted": True}
        ]
    elif class_name in ["PDF_COLLECTIONS", "PDF_Vector_Collection"]:
        properties = [
            {"name": "pdf_name", "dataType": ["string"], "indexInverted": True},
            {"name": "pdf_content", "dataType": ["text"], "indexInverted": True},
            {"name": "pdf_chunk_id", "dataType": ["string"], "indexInverted": True}
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
    print(config.class_name)
    class_name = config.class_name 
    client = init(class_name)
