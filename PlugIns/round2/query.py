import os
import numpy as np
from sentence_transformers import SentenceTransformer
from dotenv import load_dotenv
from pinecone import Pinecone
from sklearn.metrics.pairwise import cosine_similarity

# Load environment variables (Pinecone API key and index name)
load_dotenv()

# Fetch required environment variables
pinecone_api_key = os.getenv("PINECONE_API_KEY")
pinecone_index_name = os.getenv("PINECONE_INDEX_NAME")

# Initialize Pinecone
pc = Pinecone(api_key=pinecone_api_key)
index = pc.Index(pinecone_index_name)

# Initialize SentenceTransformer model
text_model = SentenceTransformer('sentence-transformers/paraphrase-MiniLM-L6-v2')


def pad_embedding(embedding, target_dim=512):
    if len(embedding) < target_dim:
        embedding = np.pad(embedding, (0, target_dim - len(embedding)), 'constant')
    else:
        embedding = embedding[:target_dim]
    return embedding

# Function to query Pinecone with cosine similarity
def query_pinecone_with_cosine_similarity(text_prompt, top_k=5, namespace=None):
    # Step 1: Encode the text prompt into a vector
    query_vector = text_model.encode(text_prompt)
    
     # Pad the query vector to 512 dimensions
    query_vector = pad_embedding(query_vector)

    # Step 2: Query Pinecone with the vector
    try:
        response = index.query(
            vector=query_vector.tolist(),  # Convert NumPy array to list
            top_k=top_k,  # Get the top K similar vectors
            namespace=namespace,  # Optional namespace
            include_values=True  # Retrieve vector values along with metadata
        )
    except Exception as e:
        print(f"Error querying Pinecone: {e}")
        return

    # Step 3: Extract the results from Pinecone
    matches = response.get('matches', [])
    
    if not matches:
        print("No matches found.")
        return

    # Step 4: Calculate cosine similarity between query vector and each match
    vectors = np.array([match['values'] for match in matches])
    similarities = cosine_similarity([query_vector], vectors)[0]

    # Step 5: Print the top K matches with their cosine similarity scores
    print(f"Top {top_k} matches for the prompt: {text_prompt}")
    for idx, match in enumerate(matches):
        print(f"Match {idx+1}: ID = {match['id']}, Score = {match['score']}, Cosine Similarity = {similarities[idx]}")

# Main function to prompt user and query Pinecone
def main():
    # Input the text prompt from the user
    text_prompt = input("Enter your text prompt: ")

    # Query Pinecone using the text prompt
    query_pinecone_with_cosine_similarity(text_prompt)

if __name__ == "__main__":
    main()
