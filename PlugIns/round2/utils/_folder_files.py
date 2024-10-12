import os
from PDFParser import main_single_file
from generate_embeddings import generate_embeddings
import upload_embeddings
import pinecone
from dotenv import load_dotenv
import setup
from query_system import query_vector_db

# Load environment variables from .env
load_dotenv()


# Main function to process PDFs and upload to Vector DB
def process_pdfs():
    pdf_directory = os.getenv("PDF_FILE_INPUT_DIR")
    if not pdf_directory:
        raise ValueError("PDF_FILE_INPUT_DIR not set in environment variables.")
    
    pdf_files = os.listdir(pdf_directory)
    print(f"main.py process those files in input folder   ...")
    print(pdf_files)
    print()

    counter =0

    for pdf_file in pdf_files:
        pdf_file = os.path.join(pdf_directory, pdf_file)

        counter = counter+1
        print(f"main.py one file a time  : {counter} ")
        print(pdf_file)
        print()

        if '.DS_Store' in pdf_file:
            continue

        # Step 1: Extract content
        content = main_single_file(pdf_file)

        # Step 2: Generate embeddings
        print ("main.py process_pdfs *** about to generate embedding ")
        print ()
        embeddings = generate_embeddings(content)

        # Step 3: Upload embeddings to Pinecone
        print ("main.py process_pdfs *** about to upload embedding ")
        print ()
        upload_embeddings.upload(embeddings)

    print("All PDFs processed and uploaded to Vector DB.")

# Function to query the Vector DB
def query_pdfs(query_text):
    # Step 1: Generate embedding for the query text
    query_embedding = generate_embeddings(query_text)  # Assuming this function returns an embedding vector
    
    # Debugging: Check if query_embedding is generated correctly
    print(f"Generated Embeddings: {query_embedding}")

    # Check if query_embedding contains valid data
    if not query_embedding or len(query_embedding) == 0:
        raise ValueError("No embeddings were generated for the query text. Please check your embedding generation function.")

    # Initialize Pinecone and get the index
    index = setup.initialize_pinecone()

    # Query the index with the generated embedding
    result = query_vector_db(query_embedding[0]['values'], index)  # Assuming embeddings have 'values' key
    print(f"Query Results: {result}")

# Run the main process
if __name__ == "__main__":
    process_pdfs()
    # Uncomment if you want to run the query after processing

    query_text = "What about the metal surface?"
   # query_pdfs(query_text)

