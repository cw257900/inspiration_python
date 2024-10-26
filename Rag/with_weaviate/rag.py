import os, sys 
import weaviate
from vector_stores import vector_stores 
import vectordb_create_schema as create_schema

import vectordb_create as create_data

# Add the parent directory (or wherever "with_pinecone" is located) to the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from vector_stores import vector_stores as vector_store
from utils import utils
from configs import configs
from dotenv import load_dotenv

load_dotenv()

# Set API keys and Weaviate URL from environment variables
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
WEAVIATE_URL = os.getenv("WEAVIATE_URL")  # WEAVIATE_URL
pdf_file_path = os.getenv("LOCAL_FILE_INPUT_PATH")
class_name = configs.WEAVIATE_STORE_NAME  # WEAVIATE_STORE_NAME
class_description = configs.WEAVIATE_STORE_DESCRIPTION


from llama_index.llms import openai
from llama_index import VectorstoreIndex, SimpleDirectoryReader
from IPython.display import Markdown, display 


documents = SimpleDirectoryReader('./data/images').load_data()
index = VectorstoreIndex.from_documents(documents)

query_engine = index.as_query_engine()
query = "What is the meaning of life?"
response = query_engine.query(query)
print(Markdown(response.response))  



def main():
    pass
def __main__():
    main()




