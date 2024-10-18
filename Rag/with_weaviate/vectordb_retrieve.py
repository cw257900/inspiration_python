import weaviate
import os
import json
from dotenv import load_dotenv
from models import graphQL
from configs import configs
from vector_stores import vector_store as vector_store 

load_dotenv()

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



def main():

    class_name = configs.WEAVIATE_STORE_NAME
    client = vector_store.client

    # Prompt the user to input a question for hybrid search
    question = input("Enter a question for hybrid search: ")
    try:
        limit = int(input("Enter the limit for number of results to return: "))
    except ValueError:
        limit = 5  # Default limit if the input is not a valid integer

    hybrid_rlt = get_hybridsearch_withLimits(client, question, limit)

    print("\nResults for hybrid search:")
    print(json.dumps(hybrid_rlt, indent=2))


# Call the main function
if __name__ == "__main__":
    main()
