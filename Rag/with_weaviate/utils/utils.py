import weaviate
import os
import weaviate
from dotenv import load_dotenv
from weaviate.exceptions import WeaviateBaseError
import inspect

# Load environment variables
load_dotenv()

# Get environment variables
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
WEAVIATE_URL = os.getenv("WEAVIATE_URL")

#
# Define headers
headers = {"X-OpenAI-Api-Key": OPENAI_API_KEY}


# Using context management if Weaviate client supports it
def reflect_weaviate_client():
    # Perform your operations with the client here
    client = weaviate.connect_to_local()

    attributes = dir(client)
    for attr in attributes:
        #print(attr)
        pass

    print()

    batch = client.batch
    attributes = dir(batch)
    for attr in attributes:
        print(attr)

    #print (help(client.collections))
    client.batch.dynamic=True

    print (client.batch)
    methods = [func for func in dir(client.batch) if callable(getattr(client.batch, func)) and not func.startswith("__")]

    print()
    print("Methods of client.batch:")
    for method in methods:
        print(method)

    # Alternatively, use inspect to get more detailed information
    print("\nDetailed method info from inspect:")
    for name, method in inspect.getmembers(client.batch, predicate=inspect.isfunction):
        print(f"Method: {name}, Callable: {method}")

    del client
    
def main():
    reflect_weaviate_client()
  
   

if __name__ == "__main__":
    print ("weaviate version:", weaviate.__version__)
    print ("weaviate url:", WEAVIATE_URL)
    main()