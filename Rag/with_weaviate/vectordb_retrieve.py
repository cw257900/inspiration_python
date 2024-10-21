import weaviate
import os
import json
from dotenv import load_dotenv
from weaviate.classes.query import MetadataQuery
from models import graphQL
from configs import configs
from vector_stores import vector_store_local as vector_store  #vector_store_local is for V4; otherwise, client.Collections will throw exception 

load_dotenv()

# Set API keys and Weaviate URL from environment variables
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
WEAVIATE_API_KEY = os.getenv("WEAVIATE_API_KEY")  # Weaviate API key
WEAVIATE_URL = os.getenv("WEAVIATE_URL")  # WEAVIATE_URL
pdf_file_path =  os.getenv("LOCAL_FILE_INPUT_PATH")
class_name =configs.WEAVIATE_STORE_NAME

def query (vector_store, inquiry = None, class_name = class_name, limit = 5):

    client = vector_store.client
    connection = client.collections.get(class_name)

    if inquiry is None:
        pass
    else:
        
        response = connection.query.hybrid(
            query=inquiry,
            alpha=0.5,
            limit=limit,
            return_metadata=MetadataQuery(score=True, explain_score=True),
        )

        return response


# Sample function to use gql_getSingleObjectById
def get_query_object_by_id(client, uuid):
    # Replace {uuid} in the query with the actual UUID value
    query = graphQL.gql_getSingleObjectById.replace("{uuid}", uuid)
    result = client.query.raw(query)
    return result

# Sample function to use gql_searchObjectsByKeyword
def get_query_object_by_keyword(client, keyword):
    # Replace {uuid} in the query with the actual UUID value
    query = graphQL.gql_queryObjectsByKeyword.replace("{keyword}", keyword)
    result = client.query.raw(query)
    return result


def get_hybridsearch_object_by_keyword(client, text):
    # Replace {uuid} in the query with the actual UUID value
    query = graphQL.gql_hybridSearchByText.replace("{text}", text)
    result = client.query.raw(query)
    return result

# Function to search objects by keyword with limit
def get_hybridsearch_withLimits(client, text, limit):
    # Dynamically replace {text} and {limit} in the query
    query = graphQL.gql_hybridsearch_withLimits.replace("{text}", text).replace("{limit}", str(limit))

    result = client.query.raw(query)
    return result



def retrieve_semantic_vector_search():

    # Prompt the user to input a question for hybrid search
    question = input("Enter a question for hybrid search: ")
    try:
        limit = int(input("Enter the limit for number of results to return: "))
    except ValueError:
        limit = 5  # Default limit if the input is not a valid integer

    hybrid_rlt =  query (vector_store, class_name = class_name, inquiry=question, limit=limit)

    print("\nResults for hybrid search:")
    for o in hybrid_rlt.objects:
       
        print(json.dumps(o.properties, indent=4))
        print(o.metadata.score)
        print(o.metadata.explain_score)
        print()

def retrieve_graphql():

    None
  
def main():
    retrieve_semantic_vector_search()

# Call the main function
if __name__ == "__main__":
    main()
