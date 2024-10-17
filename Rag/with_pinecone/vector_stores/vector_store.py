import os
import sys
from pinecone import Pinecone

from dotenv import load_dotenv


# Add the parent directory (or wherever "with_pinecone" is located) to the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from vector_stores import vector_store as vector_store
from embeddings import openai_embeddings as embeddings
from configs import configs


load_dotenv()
pinecone_api_key = os.getenv("PINECONE_API_KEY")
pinecone_index_name = configs.PINECONE_INDEX_NAME
pinecone_url = configs.PINECONE_URL

print("*********",pinecone_api_key,pinecone_index_name,pinecone_url, pinecone_index_name)

pinecone =  Pinecone(api_key=pinecone_api_key, environment=pinecone_url)

# index is PDF database
vector_store = pinecone.Index(pinecone_index_name)


print(f"vector_store: {vector_store}")