import weaviate
import os
from dotenv import load_dotenv
import json

# Load environment variables
load_dotenv()

# Set API keys and Weaviate URL from environment variables
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
WEAVIATE_API_KEY = os.getenv("WEAVIATE_API_KEY")  # Weaviate API key
WEAVIATE_URL = os.getenv("WEAVIATE_URL")

<<<<<<< HEAD
=======
# Optional: Add class names to environment variables if needed
WEAVIATE_CLASS_NAME_MOVIE = os.getenv("WEAVIATE_CLASS_NAME_MOVIE", "Movie")
WEAVIATE_CLASS_NAME_PDF = os.getenv("WEAVIATE_CLASS_NAME_PDF", "PDF_Library")
>>>>>>> dc645fc4b39851026ba8c3c64e9b59cbe32353ac

headers = {
    "X-OpenAI-Api-Key": OPENAI_API_KEY
}  # Replace with your OpenAI API key


def init_schema(schemaClassName, client):
    # Retrieve schema from the Weaviate client
    schema = client.schema.get()

    try:
        # Check if the class exists
        class_exists = any(cls['class'] == schemaClassName for cls in schema['classes'])
        
        if not class_exists:
            # Create schema properties based on the class name
            if schemaClassName == "Movie":
                properties = [
                    {"name": "title", "dataType": ["text"], "indexInverted": True},
                    {"name": "overview", "dataType": ["text"], "indexInverted": True},
                    {"name": "vote_average", "dataType": ["number"], "indexInverted": True},
                    {"name": "genre_ids", "dataType": ["int[]"], "indexInverted": True},
                    {"name": "release_date", "dataType": ["date"], "indexInverted": True},
                    {"name": "tmdb_id", "dataType": ["int"], "indexInverted": True}
                ]
<<<<<<< HEAD
            elif schemaClassName == "PDF_COLLECTIONS":
=======
            elif schemaClassName == "PDF_Library":
>>>>>>> dc645fc4b39851026ba8c3c64e9b59cbe32353ac
                properties = [
                    {"name": "pdf_name", "dataType": ["string"], "indexInverted": True},
                    {"name": "pdf_content", "dataType": ["text"], "indexInverted": True},
                    {"name": "pdf_chunk_id", "dataType": ["string"], "indexInverted": True}
                ]
            else:
                print(f"Unknown class name: {schemaClassName}")
                return

            # Create the class with properties and enable vectorization
            client.schema.create_class({
                "class": schemaClassName,
                "properties": properties,
                "vectorizer": "text2vec-openai",
                "moduleConfig": {
                    "generative-openai": {}
                }
            })
            print(f"vectordb.py: {schemaClassName} collection created.")
        else:
            print(f"vectordb.py: {schemaClassName} collection already exists.")
        
    finally:
        # Return the client in case you need to reuse it elsewhere
        return client


def init(schemaClassName):
    # Initialize the Weaviate client
    client = weaviate.Client(WEAVIATE_URL, additional_headers=headers)
    
    # Call init_schema for any classes (database)
    client = init_schema(schemaClassName=schemaClassName, client=client)
   

    # Return the client object
    return client



# Initialize the client and create both classes
#client = init("PDF_Library")
