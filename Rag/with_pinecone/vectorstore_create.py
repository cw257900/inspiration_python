from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import CharacterTextSplitter, RecursiveCharacterTextSplitter
import os
import sys
import datetime
import asyncio

# Add the parent directory (or wherever "with_pinecone" is located) to the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from vector_stores import vector_store as pinecone_vector_store
from embeddings import openai_embeddings as embeddings
from configs import configs

pdf_file_path = configs.PDF_FILE_INPUT_PATH

# Convert relative path to absolute path
pdf_file_path = os.path.abspath(os.path.join(os.path.dirname(__file__), pdf_file_path))


# Ensure the file exists before proceeding
if not os.path.exists(pdf_file_path):
    raise FileNotFoundError(f"File not found: {pdf_file_path}")


async def create_embeddings_for_pdf():

    print(f"1. split file into chunks: pdf_file_path: {pdf_file_path}")
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200,
        length_function=len    
    )
    print (text_splitter)

    print(f"2. load file with splitter to doc object")
    docs = PyPDFLoader(pdf_file_path).load_and_split(text_splitter)

    print(f"3. embed documents: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    embedded_docs = []
    for idx, doc in enumerate(docs):
        # Generate embeddings and create a tuple (ID, vector)
        embedding = await embeddings.embeddings.aembed_documents([doc.page_content])
        
        # Include the page number in the metadata
        page_number = doc.metadata.get('page', idx + 1)  # Default to idx + 1 if page is not available

        # Create a tuple with ID, vector, and metadata
        embedded_docs.append({
            "id": f"doc_{idx}",  # Unique ID
            "values": embedding[0],  # Embedding vector
            "metadata": {
                "page_content": doc.page_content,  # Add doc content as metadata
                "page_number": page_number,  # Add page number as metadata
                "source": pdf_file_path  # Optional: add file path as metadata
            }
        })
        print(f"Page {page_number} - Chunk {idx} - {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

    print(f"4. upload the embedded vectors to pinecone: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    pinecone_vector_store.vector_store.upsert(vectors=embedded_docs)
    
    print(f"5. done: pdf_file_path: {pdf_file_path}")
    

if __name__ == "__main__":
   asyncio.run(create_embeddings_for_pdf())
