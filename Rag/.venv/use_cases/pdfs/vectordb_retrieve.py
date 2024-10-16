import weaviate
import os
import json
import sys
import vectordb_init  # Assuming this is a module where init() is defined
from utils import graphQL


def get_query_object(class_name, query):

    client = vectordb_init.init(class_name)  # Initialize the client using your `vectordb_init` module
    result = client.query.raw(query)  # Using the query from queries.py

    return result

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

    print ("query excuted")
    print (query)
    
    result = client.query.raw(query)
    return result



def main():

    class_name = 'PDF_COLLECTIONS'  # Define the class name you want to fetch objects from
    client = vectordb_init.init(class_name)  # Initialize the client using your `vectordb_init` module

    #query_rlt = get_query_object_by_keyword(client, 'New Jersey')    


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
