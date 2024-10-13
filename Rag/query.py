import os
import traceback 
from PyPDF2 import PdfReader
from dotenv import load_dotenv
from langchain.text_splitter import CharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
import weaviate
from weaviate.classes.init import Auth
from weaviate.exceptions import WeaviateBaseError

# Load environment variables
load_dotenv()

# Set API keys and Weaviate URL from environment variables
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
WEAVIATE_API_KEY = os.getenv("WEAVIATE_API_KEY")  # Weaviate API key
WEAVIATE_URL=os.getenv("WEAVIATE_URL")

# Initialize Weaviate client with API key authentication (v4)
client = weaviate.connect_to_weaviate_cloud(
    cluster_url=WEAVIATE_URL,
    auth_credentials=Auth.api_key(WEAVIATE_API_KEY),
)

# Function to check if the client is ready
def is_weaviate_ready():
    if client.is_ready():
        print("Weaviate instance is ready.")
    else:
        print("Weaviate instance is NOT ready.")
        return False
    return True



def upload_text_to_weaviate():
    try:
        # Define a simple schema
        client.collections.create("Article")

        
        

    except Exception as e:
        print(f"Error uploading text to Weaviate: {e}")
        traceback.print_exc()
        
    finally:
        client.close()  # Close the Weaviate client properly

# Main function
def main():
    if is_weaviate_ready():
        upload_text_to_weaviate()

if __name__ == "__main__":
    main()