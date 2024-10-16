import weaviate
import weaviate.classes.config as wc
import os
from dotenv import load_dotenv
import json

# Load environment variables
load_dotenv()

# Set API keys and Weaviate URL from environment variables
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
WEAVIATE_API_KEY = os.getenv("WEAVIATE_API_KEY")  # Weaviate API key

headers = {
    "X-OpenAI-Api-Key": OPENAI_API_KEY
}  # Replace with your OpenAI API key

# Connect to Weaviate (assuming local)
client = weaviate.Client("http://localhost:8080", additional_headers=headers)

try:
    # Check if "Movie" collection already exists
    schema = client.schema.get()
    class_exists = any(cls['class'] == "Movie" for cls in schema['classes'])
    
    if not class_exists:
        # Create the "Movie" class if it doesn't exist
        client.schema.create_class({
            "class": "Movie",
            "properties": [
                {
                    "name": "title",
                    "dataType": ["text"]
                },
                {
                    "name": "overview",
                    "dataType": ["text"]
                },
                {
                    "name": "vote_average",
                    "dataType": ["number"]
                },
                {
                    "name": "genre_ids",
                    "dataType": ["int[]"]
                },
                {
                    "name": "release_date",
                    "dataType": ["date"]
                },
                {
                    "name": "tmdb_id",
                    "dataType": ["int"]
                }
            ],
            "vectorizer": "text2vec-openai",
            "moduleConfig": {
                "generative-openai": {}
            }
        })
        print("Movie collection created.")
    else:
        print("Movie collection already exists.")
    
    # Retrieve and print meta information about the Weaviate instance
    meta_info = client.get_meta()
    print()
    print ("meta data")
    print(json.dumps(meta_info, indent=2))

finally:
    client.close()
