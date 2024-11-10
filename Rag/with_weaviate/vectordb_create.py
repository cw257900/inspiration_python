import os
import json
import datetime
import asyncio
import sys
import traceback 

from langchain.text_splitter import CharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
import weaviate
from weaviate.classes.init import Auth
from weaviate.exceptions import WeaviateBaseError 
from weaviate.util import generate_uuid5
from langchain_huggingface import HuggingFaceEmbeddings


# Add the parent directory (or wherever "with_pinecone" is located) to the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from chunking import chunking_recursiveCharacterTextSplitter
from embeddings import  embedding_openai 
from vector_stores import vector_stores    as vector_store
import vectordb_create_schema as vectordb_create_schema
from configs import configs
from utils import utils

from dotenv import load_dotenv
load_dotenv()

import logging

logging.basicConfig(
        format='%(asctime)s - %(levelname)s - %(message)s',
        level=logging.INFO,
        force=True
    )


# Set API keys and Weaviate URL from environment variables
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
WEAVIATE_API_KEY = os.getenv("WEAVIATE_API_KEY")  # Weaviate API key
WEAVIATE_URL = os.getenv("WEAVIATE_URL")  # WEAVIATE_URL
pdf_file_path =  os.getenv("LOCAL_FILE_INPUT_PATH")
class_name =configs.WEAVIATE_STORE_NAME
class_description =configs.WEAVIATE_STORE_DESCRIPTION
os.environ["OPENAI_API_KEY"]  = OPENAI_API_KEY


# Assuming embeddings.embeddings.aembed_documents is async and we are running this in an async environment
async def upsert_embeddings_to_vector_store(pdf_file_path, vector_store,  class_name):
    try:
        print(f"1. Inserting chunks of {pdf_file_path} - {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        
        docs = chunking_recursiveCharacterTextSplitter.get_chunked_doc(pdf_file_path)
        client = vector_store.create_client()
        collection = client.collections.get(class_name)
        embedding_huggingface =  HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
        
        # Iterate through the processed docs and insert them into Weaviate
        for idx, doc in enumerate(docs):
            # Generate embeddings for the document page content, openai , next 1 line
            embedding = await embedding_openai.embeddings.aembed_documents([doc.page_content])

            """
            # huggingface embedding, next 5 lines
            # Ensure page_content is a single string, not a list
            if isinstance(doc.page_content, list):
                page_content = " ".join(doc.page_content)  # Join list items into a single string
            else:
                page_content = doc.page_content  # Already a string
            embedding = embedding_huggingface.embed_query(page_content)  # Get the first embedding in the list
            """
            
            # Get the page number from metadata or use idx + 1 if not available
            page_number = doc.metadata.get('page', idx + 1)
            
            # Create the data object with metadata
            data_object = {
                "page_content": doc.page_content,  # Add doc content as metadata
                "page_number": page_number,        # Add page number as metadata
                "source": pdf_file_path            # Optional: add file path as metadata
            }
         
            collection.data.insert(
                properties=data_object,
                uuid=generate_uuid5(json.dumps(data_object) + class_name),
                vector=embedding[0]  # Use the embedding as the vector openai only
                #vector=embedding #hugging face only 
            )

            print(f"Inserted: Page {page_number} - Chunk {idx} - {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
            #print(embedding[0])


    
        print(f"Embeddings uploaded - {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    except Exception as e:
        print(f"Error: {e}")
        #traceback.print_exc()

    finally:
       vector_store.close_client(client)


# weaviate v4 code
# Uploading chunks to Weaviate, by default ebedding
# if same file updated already, it will throw exception : Unexpected status code: 422, 
# with response body: {'error': [{'message': "id '8a5c4432-9a82-5f98-b9dd-5ca80b77cd13' already exists"}]}
def upsert_chunks_to_store(pdf_file_path, vector_store, class_name):

    try:
        client = vector_store.create_client()
        collection_name = client.collections.get(class_name)

        all_files = []
        for dirpath, dirnames, filenames in os.walk(pdf_file_path):
            for filename in filenames:
               if not filename.startswith('.'):  # Exclude files that start with a dot
                    all_files.append(os.path.join(dirpath, filename))

        logging.info (f"\n *create.py -- all files \n {json.dumps(all_files, indent=2)}")

        for file in all_files:
                

            # this is sentenceBased chunker 
            docs = chunking_recursiveCharacterTextSplitter.get_chunked_doc(file)

            logging.info(f" === *create.py Inserting chunks of {file} ") 

            try: #if exception happens, move on to next

                # Iterate through the processed docs and insert them into Weaviate
                for idx, doc in enumerate(docs):
                    # Generate embeddings for the document page content

        
                    # Get the page number from metadata or use idx + 1 if not available
                    page_number = doc.metadata.get('page', idx + 1)
                    
                    # Create the data object with metadata
                    data_object = {
                        "page_content": doc.page_content,  # Add doc content as metadata
                        "page_number": page_number,        # Add page number as metadata
                        #"source": pdf_file_path            # Optional: add file path as metadata
                        "source": file
                    }
                

                    # Insert the object along with its vector into Weaviate
                    collection_name.data.insert(
                        properties=data_object,
                        uuid=generate_uuid5(data_object),
                    )
                    
                    logging.info (f"Inserted: Page {page_number} - Chunk {idx} for {file} ")
            
            except Exception as e:
                logging.error(f" *** *created.py - upsert_chunks_to_store {file} \n    {e}")
                continue

            logging.info (f" === *create.py - All chuncks inserted for {file} ")


    except Exception as e:
        logging.error(f" *** created.py -- upsert_chunks_to_store {e}") # will error out if object already in db to avoid duplicates 
        traceback.print_exc()
        pass 

    finally:
       # client.close() not needed , he Python client uses standard HTTP requests under the hood, which are automatically closed after the response is received. 
       vector_store.close_client(client)

def upsert_multi_models (pdf_file_path, vector_store, class_name):
    None

def main ():
    print(pdf_file_path)
    print(class_name)
    print()

    # Use asyncio.run to run the async function
    # asyncio.run(upsert_embeddings_to_vector_store(pdf_file_path, vector_store=vector_store, class_name=class_name))
    upsert_chunks_to_store(pdf_file_path, vector_store, class_name)
   

# Entry point
if __name__ == "__main__":
    main()




