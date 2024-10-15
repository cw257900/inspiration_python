import os
import traceback 
import uuid as uuid_lib 
from PyPDF2 import PdfReader
from dotenv import load_dotenv
from langchain.text_splitter import CharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
import weaviate
from weaviate.classes.init import Auth
from weaviate.exceptions import WeaviateBaseError
from utils import pdf_processor  
import sys
sys.path.append("../../")
import vectordb_init  # Assuming this is a module where init() is defined

load_dotenv()

# Set API keys and Weaviate URL from environment variables
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
WEAVIATE_API_KEY = os.getenv("WEAVIATE_API_KEY")  # Weaviate API key
WEAVIATE_URL = os.getenv("WEAVIATE_URL")
<<<<<<< HEAD
class_name = os.getenv("WEAVIATE_CLASS_NAME_PDF")
#pdf_file_path = os.getenv("LOCAL_FILE_INPUT_PATH")
pdf_file_path="/Users/Connie/Desktop/connie/inspiration_python/Rag/.venv/use_cases/pdfs/data/all-number-table.pdf"
=======
class_name = os.getenv("WEAVIATE_CLASS_NAME_PDF", "PDF_COLLECTIONS")
pdf_file_path = os.getenv("LOCAL_FILE_INPUT_PATH")
>>>>>>> dc645fc4b39851026ba8c3c64e9b59cbe32353ac


def vectordb_verify_data(client):

<<<<<<< HEAD
    collection_objects = client.data_object.get(class_name=class_name, limit=5)  # Adjust limit as needed
=======
    collection_objects = client.data_object.get(class_name=class_name, limit=10)  # Adjust limit as needed
>>>>>>> dc645fc4b39851026ba8c3c64e9b59cbe32353ac
    for obj in collection_objects['objects']:
        print(f"Object ID: {obj['id']}, Data: {obj['properties']}")
        
        # Optionally, print each property and its value in detail
        for prop, value in obj['properties'].items():
            print(f"Property: {prop}, Value: {value}")


<<<<<<< HEAD
    print ("Finished vectordb_verify_data() print out 5 records")

=======
>>>>>>> dc645fc4b39851026ba8c3c64e9b59cbe32353ac

# Function to load text chunks into Weaviate
def vectordb_upload_pdf():
    try:
        # Initialize Weaviate client
        client = vectordb_init.init(class_name)


        # Process PDF and upload chunks to Weaviate
        text_chunks = pdf_processor.get_text_chunks(pdf_file_path)
       
<<<<<<< HEAD
       
=======
>>>>>>> dc645fc4b39851026ba8c3c64e9b59cbe32353ac
        for idx, chunk in enumerate(text_chunks):
            # Prepare the object to upload
            data_object = {
                "pdf_name": pdf_file_path,
                "pdf_content": chunk,
                "pdf_chunk_id": f"chunk_{idx}"
            }
            # Create data object in Weaviate
            client.data_object.create(data_object, class_name)

        vectordb_verify_data(client)

<<<<<<< HEAD
        print("Finished vectordb_upload_pdf()")
        print (pdf_file_path)

=======
>>>>>>> dc645fc4b39851026ba8c3c64e9b59cbe32353ac

    except Exception as e:
        print(f"vectordb_create.py Error retrieving class schema: {e}")
        traceback.print_exc()

    finally:
        None
             
vectordb_upload_pdf()
