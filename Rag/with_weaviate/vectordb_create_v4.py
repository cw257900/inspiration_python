import os
import traceback 
from dotenv import load_dotenv
from langchain.text_splitter import CharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
import weaviate
from weaviate.classes.init import Auth
from weaviate.exceptions import WeaviateBaseError 
import sys
from weaviate.util import generate_uuid5
# Add the parent directory (or wherever "with_pinecone" is located) to the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from vector_stores import vector_store_local    as vector_store_local
from embeddings import openai_embeddings as embeddings
from utils import pdf_processor , utils
from configs import configs
import datetime
import asyncio

load_dotenv()

# Set API keys and Weaviate URL from environment variables
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
WEAVIATE_API_KEY = os.getenv("WEAVIATE_API_KEY")  # Weaviate API key
WEAVIATE_URL = os.getenv("WEAVIATE_URL")  # WEAVIATE_URL
pdf_file_path =  os.getenv("LOCAL_FILE_INPUT_PATH")
class_name =configs.WEAVIATE_STORE_NAME
class_description =configs.WEAVIATE_STORE_DESCRIPTION




# Assuming embeddings.embeddings.aembed_documents is async and we are running this in an async environment
async def insert_embeddings_to_vector_store(pdf_file_path, vector_store, pdf_processor, embeddings, WEAVIATE_STORE_NAME):
    try:
        client = vector_store.client
        docs = pdf_processor.get_chunked_doc(pdf_file_path)  # Load and process the document

        collection = client.collections.get(class_name)

        print(f"1. Inserting chunks of {pdf_file_path} - {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        
        # Iterate through the processed docs and insert them into Weaviate
        for idx, doc in enumerate(docs):
            # Generate embeddings for the document page content
            embedding = await embeddings.embeddings.aembed_documents([doc.page_content])
            
            # Get the page number from metadata or use idx + 1 if not available
            page_number = doc.metadata.get('page', idx + 1)
            
            # Create the data object with metadata
            data_object = {
                "page_content": doc.page_content,  # Add doc content as metadata
                "page_number": page_number,        # Add page number as metadata
                "source": pdf_file_path            # Optional: add file path as metadata
            }

            # Insert the object along with its vector into Weaviate
            # client.data_object will be depercated in Nov, 2024
            collection.data.insert(
                data_object=data_object,
                class_name=class_name,  # Use the actual Weaviate class name
                vector=embedding[0]  # Use the embedding as the vector
            )

            print(f"Inserted: Page {page_number} - Chunk {idx} - {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

        print(f"2. All chunks inserted for {pdf_file_path} - {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

        # Optionally, print a few inserted data objects
        print(client.data_object.get(class_name=WEAVIATE_STORE_NAME, limit=10))
        print(f"Embeddings uploaded - {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    except Exception as e:
        print(f"Error: {e}")
        traceback.print_exc()

    finally:
       # client.close() not needed , he Python client uses standard HTTP requests under the hood, which are automatically closed after the response is received. 
       del client  # Delete the client to release resources

# Uploading chunks to Weaviate, not using the async function
def upsert_chunks_to_store(pdf_file_path, vector_store_local, class_name):

    try:
        client = vector_store_local.client
        docs = pdf_processor.get_chunked_doc(pdf_file_path)  # Load and process the document

        collection = client.collections.get(class_name)

        print(f"1. Inserting chunks of {pdf_file_path} - {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}") 
        
        # Iterate through the processed docs and insert them into Weaviate
        for idx, doc in enumerate(docs):
            # Generate embeddings for the document page content
          
            # Get the page number from metadata or use idx + 1 if not available
            page_number = doc.metadata.get('page', idx + 1)
            
            # Create the data object with metadata
            data_object = {
                "page_content": doc.page_content,  # Add doc content as metadata
                "page_number": page_number,        # Add page number as metadata
                "source": pdf_file_path            # Optional: add file path as metadata
            }

            # Insert the object along with its vector into Weaviate
            collection.data.insert(
                properties=data_object,
                uuid=generate_uuid5(data_object),
            )

            print(f"Inserted: Page {page_number} - Chunk {idx} - {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")


        """
        @TODO: check for duplicate for update
        """
        print (f"{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - All chuncks inserted for {pdf_file_path} ")


    except Exception as e:
        print(f"Error: {e}") # will error out if object already in db to avoid duplicates 
        #traceback.print_exc()
        pass 

    finally:
       # client.close() not needed , he Python client uses standard HTTP requests under the hood, which are automatically closed after the response is received. 
       del client  # Delete the client to release resources


# Entry point
if __name__ == "__main__":
    # Use asyncio.run to run the async function
    # asyncio.run(upsert_embeddings_to_vector_store(pdf_file_path, vector_store, pdf_processor, embeddings, WEAVIATE_STORE_NAME))

    print(pdf_file_path)
    upsert_chunks_to_store(pdf_file_path, vector_store_local=vector_store_local, class_name=class_name)
       