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

# Load environment variables
load_dotenv()

# Set API keys and Weaviate URL from environment variables
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
WEAVIATE_API_KEY = os.getenv("WEAVIATE_API_KEY")  # Weaviate API key
WEAVIATE_URL = os.getenv("WEAVIATE_URL")
WEAVIATE_CLASS_NAME = os.getenv("WEAVIATE_CLASS_NAME")
WEAVIAtE_CLASS_DESCRIPTION = os.getenv("WEAVIAtE_CLASS_DESCRIPTION")


# Initialize Weaviate client with API key authentication (v4)
client = weaviate.connect_to_weaviate_cloud(
    cluster_url=WEAVIATE_URL,
    auth_credentials=Auth.api_key(WEAVIATE_API_KEY),
)



# Function to read PDF and extract text from all pages
def get_pdf_text(pdf_file_path):
    with open(pdf_file_path, 'rb') as file:
        reader = PdfReader(file)
        text = ""
        # Iterate through all pages and extract text
        for page_num in range(len(reader.pages)):
            page = reader.pages[page_num]
            text += page.extract_text()
    return text

# Function to split the extracted text into chunks for better embedding
def get_text_chunks(text):
    text_splitter = CharacterTextSplitter(
        separator="\n",
        chunk_size=1000,
        chunk_overlap=200,
        length_function=len
    )
    chunks = text_splitter.split_text(text)
    return chunks

def define_schema():
     # Define the schema manually for v4 (adjust if necessary)
    class_obj = {
        "class": WEAVIATE_CLASS_NAME,
        "description": WEAVIAtE_CLASS_DESCRIPTION,
        "properties": [{
            "name": "content",
            "dataType": ["text"]
        },
        {
            "name": "chunk_id",
            "dataType": ["string"]
        }
        ],
        #"vectorizer": "none"  # Vectors are provided manually when insert object into db
        "vectorizer": "text2vec-transformers"  # Weaviate will use this vectorizer to create embeddings
    }  
    return class_obj  

# Function to load text chunks into Weaviate
def load_pdf_to_weaviate_db(pdf_file_path):
    try:
        # Extract text from the PDF file
        text = get_pdf_text(pdf_file_path)
        
        # Split the text into manageable chunks
        text_chunks = get_text_chunks(text)
   
        
        # Define the schema manually for v4 (adjust if necessary)
        class_obj = define_schema()
        
        # Iterate through text chunks and upload them to Weaviate
        for idx, chunk in enumerate(text_chunks):

            # Prepare the object to upload
            data_object = {
                "content": chunk,
                "chunk_id": f"{pdf_file_path}_chunk_{idx}"
            }

            try:
                pdf_collections =  client.collections.get(WEAVIATE_CLASS_NAME)
                pdf_collections.data.insert(
                    properties=data_object,
                    uuid = str(uuid_lib.uuid4())
                )
             
            except WeaviateBaseError as e:
                traceback.print_exc()
        
    except Exception as e:
        traceback.print_exc(data_object)
        return None
    
    finally:

        client.close()  # Close the Weaviate client properly




def main():
    pdf_file_path = "data/business_law.pdf"  # Specify the path to your PDF file
    load_pdf_to_weaviate_db(pdf_file_path)
  

if __name__ == "__main__":
    main()
