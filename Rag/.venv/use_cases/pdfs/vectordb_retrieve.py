import weaviate
import os
import json
import sys
sys.path.append("../../")
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


def main():

    class_name = 'PDF_COLLECTIONS'  # Define the class name you want to fetch objects from
    client = vectordb_init.init(class_name)  # Initialize the client using your `vectordb_init` module

    query_rlt = get_query_object_by_keyword(client, 'New Jersey')    

    query_rlt = get_hybridsearch_object_by_keyword(client, 'What constituation say about carrying guns?')    
    
    # Pretty print the result
    print(json.dumps(query_rlt, indent=2))


# Call the main function
if __name__ == "__main__":
    main()
