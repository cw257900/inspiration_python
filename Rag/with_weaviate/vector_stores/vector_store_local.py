import os
import sys
import weaviate
from weaviate.classes.init import Auth

# Add the parent directory (or wherever "with_pinecone" is located) to the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
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


# Initialize the Weaviate client
client = weaviate.connect_to_local(
        headers={
            "X-OpenAI-Api-Key": OPENAI_API_KEY # Replace with your inference API key
        }
    )

print(f"0.2. vector_store client from venctor_store_local.py: client status", client.is_ready())