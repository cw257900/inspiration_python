
from dotenv import load_dotenv
import os
import sys

from pinecone import Pinecone
from langchain_openai import OpenAIEmbeddings 
# Add the parent directory (or wherever "with_pinecone" is located) to the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from configs import configs


"""""
# Explicitly specify the path to the .env file
dotenv_path = os.path.join(os.path.dirname(__file__), '..', '.env')

# Load environment variables from the specified .env file
load_dotenv(dotenv_path)

# Check if the environment variables are being loaded correctly
print(f"dotenv_path: {dotenv_path}")
pinecone_api_key = os.getenv("PINECONE_API_KEY")
pinecone_index_name = os.getenv("PINECONE_INDEX_NAME")

# Verify the loaded environment variables
print(f"pinecone_api_key: {pinecone_api_key}")
print(f"pinecone_index_name: {pinecone_index_name}")

"""

load_dotenv()
pinecone_api_key = os.getenv("PINECONE_API_KEY")
openai_api_key = os.getenv("OPENAI_API_KEY")
pinecone_index_name = configs.PINECONE_INDEX_NAME
pinecone_url = configs.PINECONE_URL


pinecone=Pinecone(api_key=pinecone_api_key, environment = pinecone_url)

embeddings = OpenAIEmbeddings(openai_api_key=openai_api_key)

print(f"0.1. embeddings:  {embeddings}")

