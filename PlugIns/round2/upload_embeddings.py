import pinecone

def upload(embeddings, index, namespace="default"):
    """
    Uploads a list of embeddings to the specified Pinecone index.

    Parameters:
    embeddings (list of dict): List of embeddings to upload. Each embedding should be a dictionary
                               with keys 'id' and 'values' (embedding vector).
    index (pinecone.Index): The Pinecone index object to upload embeddings to.
    namespace (str): The namespace within the Pinecone index to upload to (default is "default").
    """

    try:
        # Prepare the list of vectors for uploading
        vectors = []
        for embedding in embeddings:
            if 'id' not in embedding or 'values' not in embedding:
                print(f"Skipping invalid embedding: {embedding}")
                continue

            vectors.append((embedding['id'], embedding['values']))

        # Upload the vectors to Pinecone
        if vectors:
            print(f"Uploading {len(vectors)} embeddings to Pinecone...")
            index.upsert(vectors=vectors, namespace=namespace)
            print("Upload successful.")
        else:
            print("upload_embeddings.py ** No valid embeddings to upload.")

    except Exception as e:
        print(f"Error uploading embeddings to Pinecone: {e}")
