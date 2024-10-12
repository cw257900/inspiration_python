import os
import pinecone  # Correct Pinecone import
from dotenv import load_dotenv
from pinecone import Pinecone, ServerlessSpec
import numpy as np

# Load environment variables from .env
load_dotenv()

# Fetch required environment variables
pdf_directory = os.getenv("PDF_FILE_INPUT_DIR")
pinecone_api_key = os.getenv("PINECONE_API_KEY")
pinecone_index_name = os.getenv("PINECONE_INDEX_NAME")

# Ensure all required environment variables are loaded
if not pinecone_api_key or not pinecone_index_name or not pdf_directory:
    raise ValueError("Missing environment variables: PINECONE_API_KEY, PINECONE_INDEX_NAME, or PDF_FILE_INPUT_DIR.")

def initialize_pinecone():
    """
    Initializes Pinecone and connects to an existing index.
    If the index does not exist, it creates it.
    """
    try:
        # Initialize Pinecone using the new API key structure
        pc = Pinecone(api_key=pinecone_api_key)

        # Check if the index exists, and create it if it doesn't
        if pinecone_index_name not in pc.list_indexes().names():
            pc.create_index(
                name=pinecone_index_name, 
                dimension=512,  # Adjust based on your embedding dimension
                metric='cosine',  # Adjust the metric based on your needs
                spec=ServerlessSpec(
                cloud='aws',
                region='us-east-1'
            )
            )
        else:
            print(f"setup.py Index {pinecone_index_name} already exists. Connecting...")
            print()

        # Connect to the index
        index = pc.Index(pinecone_index_name)
        return index
    
    except Exception as e:
        print(f" setup.py Error initializing Pinecone: {e}")
        return None

def add_vectors_to_index(index, vectors):
    """
    Adds vectors to the given Pinecone index.
    """
    try:
        # Upsert vectors into the index
        index.upsert(vectors)
        print("Vectors added successfully.")
    except Exception as e:
        print(f"setup.py Error adding vectors to index: {e}")
        print()

# Example usage
if __name__ == "__main__":
    # Initialize the Pinecone index
    index = initialize_pinecone()



    if index:
        # Example vectors to be added (replace with your actual vectors)
         example_vectors = [
            ("vector_id_1", np.random.rand(512).tolist()),  # Vector with dimension 512
            ("vector_id_2", np.random.rand(512).tolist())
        ]
    add_vectors_to_index(index, example_vectors)


