import os
import numpy as np
from sentence_transformers import SentenceTransformer
from dotenv import load_dotenv
from pinecone import Pinecone

from sklearn.metrics.pairwise import cosine_similarity



# Load environment variables
load_dotenv()

# Fetch required environment variables
pinecone_api_key = os.getenv("PINECONE_API_KEY")
pinecone_index_name = os.getenv("PINECONE_INDEX_NAME")

# Initialize Pinecone
pc = Pinecone(api_key=pinecone_api_key)
index = pc.Index(pinecone_index_name)

# Initialize SentenceTransformer model
text_model = SentenceTransformer('sentence-transformers/paraphrase-MiniLM-L6-v2')


# Sample reference texts and their pre-embedded vectors
reference_texts = [
    "The sky is blue.",
    "The sun is bright today.",
    "It is raining outside.",
    "The weather is pleasant and sunny.",
    "It is snowing in the mountains."
]
# Pre-compute embeddings for reference texts
reference_embeddings = text_model.encode(reference_texts)

# Function to query Pinecone and convert vector to text
def convert_vector_to_text(vector_id, namespace=None, top_k=3):
    try:
        # Query Pinecone with the vector ID
        response = index.query(
            namespace=namespace,  # Namespace (optional)
            id=vector_id,  # Vector ID to query
            top_k=top_k,  # Top K results
            include_values=True  # Include vector values in the result
        )

        # Extract the vector from the response
        matches = response['matches']
        if not matches:
            return "No matches found."

        # Convert the top match vector to a text answer
        best_match_vector = matches[0]['values']
        text_answer = vector_to_text(best_match_vector)

        return text_answer

    except Exception as e:
        return f"Error querying Pinecone: {e}"


# Function to decode vector into a text answer by finding the nearest text match
def vector_to_text(vector):
    # Reshape the query vector for comparison
    query_vector = np.array(vector).reshape(1, -1)

    # Compute cosine similarity between the query vector and reference embeddings
    similarities = cosine_similarity(query_vector, reference_embeddings)

    # Find the index of the most similar text
    best_match_idx = np.argmax(similarities)

    # Return the most similar text
    return reference_texts[best_match_idx]

# Main function to execute the query
def main():

    # Prompt the user for input text
    user_input = input("prompt: ")

     # Simulated vector (replace with actual vector from Pinecone)
    example_vector = text_model.encode(user_input)

    # Decode the vector into the most similar text
    decoded_text = vector_to_text(example_vector)
    print(f"Decoded text: {decoded_text}")

if __name__ == "__main__":
    main()
