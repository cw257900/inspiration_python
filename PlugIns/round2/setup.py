import os
from dotenv import load_dotenv
from pinecone import Pinecone, ServerlessSpec

# Load environment variables from .env
load_dotenv()

# Fetch PDF directory and Pinecone API key from environment variables
pdf_directory = os.getenv("PDF_FILE_INPUT_DIR")
pinecone_api_key = os.getenv("PINECONE_API_KEY")
pinecone_index_name = os.getenv("PINECONE_INDEX_NAME")

# Check if the environment variables were loaded correctly
if not pinecone_api_key or not pinecone_index_name or not pdf_directory:
    raise ValueError("One or more required environment variables are missing: PINECONE_API_KEY, PINECONE_INDEX_NAME, or PDF_FILE_INPUT_DIR.")

# Initialize Pinecone client using the correct API
def initialize_pinecone():
    try:
        # Initialize Pinecone using the Pinecone class and API key
        pc = Pinecone(api_key=pinecone_api_key)

        if pinecone_index_name not in pc.list_indexes():
            # Create the index only if it doesn't already exist
            print(f"Creating Pinecone index: {pinecone_index_name}")
            pc.create_index(
                name=pinecone_index_name, 
                dimension=512,  # Adjust based on your embedding dimension
                metric='cosine',
                spec=ServerlessSpec(
                    cloud='aws',
                    region='us-east-1'  # Adjust region as needed
                ),
                
            )
        else:
            print(f"Index {pinecone_index_name} already exists, skipping creation.")


        # Get the index host
        index_description = pc.describe_index(pinecone_index_name)
        if index_description is None:
            raise ValueError(f"Index {pinecone_index_name} does not exist or was not properly created.")
        
        host = index_description['host']
        
        # Connect to the index using the host
        index = pc.Index(pinecone_index_name, host=host)
        
        print(f"Pinecone Index Name: {index}")
        print("Pinecone initialized and index connected successfully.")
        return index
    
    except Exception as e: 
        print(f"Error initializing Pinecone: {e}")
        return None

# List all PDF files in the specified directory
def list_pdfs(pdf_directory):
    if not os.path.exists(pdf_directory):
        raise FileNotFoundError(f"PDF directory {pdf_directory} does not exist.")
    
    return [f for f in os.listdir(pdf_directory) if f.endswith('.pdf')]

# Example usage: print all PDFs
if __name__ == "__main__":
    index = initialize_pinecone()
    if index:
        pdf_files = list_pdfs(pdf_directory)
        print("setup.py ** PDFs found:", pdf_files)
