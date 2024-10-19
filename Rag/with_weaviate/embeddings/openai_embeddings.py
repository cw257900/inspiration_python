
import os
import sys
from langchain_openai import OpenAIEmbeddings 
# Add the parent directory (or wherever "with_pinecone" is located) to the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from configs import configs
from dotenv import load_dotenv

load_dotenv()
openai_api_key = os.getenv("OPENAI_API_KEY")

# Set API keys and Weaviate URL from environment variables
embeddings = OpenAIEmbeddings(openai_api_key=openai_api_key)

print(f"0.1. embeddings initiated from openai_embeddings.py")

