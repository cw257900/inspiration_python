import pinecone
import os
from dotenv import load_dotenv
import setup

# Load environment variables
load_dotenv()


# Directories from environment variables
PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")
pinecone_index_name = os.getenv("PINECONE_INDEX_NAME")

setup.initialize_pinecone()

def query_vector_db(query_embedding, index, top_k=10, namespace="default"):
    """
    Queries the Pinecone index with the embedding generated from the query text.

    Parameters:
    query_embedding (list): The embedding vector for the query.
    index (pinecone.Index): The Pinecone index object to query.
    top_k (int): The number of top matches to return.
    namespace (str): The namespace within the Pinecone index to search (default is "default").

    Returns:
    result (dict): The result of the query from Pinecone.
    """
    try:
        # Perform the query
        result = index.query(
            queries=[query_embedding],  # Use the query embedding vector
            top_k=top_k,  # Only pass top_k here once
            namespace=namespace
        )

        # Return the results
        return result

    except Exception as e:
        print(f"Error querying Pinecone: {e}")
        return None
