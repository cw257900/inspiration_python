import weaviate
import os
import json
from dotenv import load_dotenv
from weaviate.classes.query import MetadataQuery
from models import graphQL
from configs import configs
from vector_stores import vector_stores as vector_store  #vector_store_local is for V4; otherwise, client.Collections will throw exception 
from models import graphQL
from configs import configs
load_dotenv()

# Set API keys and Weaviate URL from environment variables
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
WEAVIATE_API_KEY = os.getenv("WEAVIATE_API_KEY")  # Weaviate API key
WEAVIATE_URL = os.getenv("WEAVIATE_URL")  # WEAVIATE_URL
WEAVIATE_URL_GRAPHQL = os.getenv("WEAVIATE_URL_GRAPHQL")
pdf_file_path =  os.getenv("LOCAL_FILE_INPUT_PATH")
class_name =configs.WEAVIATE_STORE_NAME

headers = {
    "Content-Type": "application/json"
}

def retrieve_graphql( text_query, class_name=class_name,  limit =5):

    client = vector_store.create_client()
    connection = client.collections.get(class_name)

    query = graphQL.gql_hybridsearch_withLimits % (class_name, text_query, limit)
    print(query)

    if text_query is None:
        pass
    else:
        
        response = connection.query.hybrid(
            query=text_query,
            alpha=0.5,
            limit=limit,
            return_metadata=MetadataQuery(score=True, explain_score=True),
        )

        return response
    
    vector_store.close_client(client)




def main():
    #Prompt the user to input a question for hybrid search
    question = input("Enter a question for hybrid search: ")
    try:
        limit = int(input("Enter the limit for number of results to return: "))
    except ValueError:
        limit = 5  # Default limit if the input is not a valid integer

    hybrid_rlt =retrieve_graphql(question, class_name=class_name,  limit =5)

    print("\nResults for hybrid search:")
    for o in hybrid_rlt.objects:
       
        print(json.dumps(o.properties, indent=4))
        print(o.metadata.score)
        print(o.metadata.explain_score)
        print()

if __name__ == "__main__":
    main()
