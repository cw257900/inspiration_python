import os
import pinecone
from dotenv import load_dotenv
from pinecone import Pinecone
from sentence_transformers import SentenceTransformer
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from langchain.vectorstores import Pinecone
from embeddings import openai

# Load environment variables
load_dotenv()


# Fetch required environment variables
pdf_directory = os.getenv("PDF_FILE_INPUT_DIR")
pinecone_api_key = os.getenv("PINECONE_API_KEY")
pinecone_index_name = os.getenv("PINECONE_INDEX_NAME")


# Initialize Pinecone
pc = Pinecone(api_key=pinecone_api_key)
index = pc.Index(pinecone_index_name)

