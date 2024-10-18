import weaviate
import pandas as pd
import requests
from datetime import datetime, timezone
import json
from weaviate.util import generate_uuid5
from tqdm import tqdm
import os
import sys
sys.path.append("../../")
import vectordb_init_schema


# Instantiate your client (not shown). e.g.:
# client = weaviate.connect_to_weaviate_cloud(...) or
# client = weaviate.connect_to_local(...)

client = vectordb_init_schema.init()

# Get the collection
movies = client.schema.get("Movie")

# Example movie data to insert in batch
movies_data = [
    {
        "title": "Inception",
        "overview": "A thief who steals corporate secrets through use of dream-sharing technology.",
        "vote_average": 8.8,
        "genre_ids": [28, 878],
        "release_date": "2010-07-16T00:00:00Z",
        "tmdb_id": 27205
    },
    {
        "title": "The Matrix",
        "overview": "A computer hacker learns from mysterious rebels about the true nature of his reality.",
        "vote_average": 8.7,
        "genre_ids": [28, 878],
        "release_date": "1999-03-31T00:00:00Z",
        "tmdb_id": 603
    }
]



# Create a batch for bulk insertion
def insert_movies_batch(client, movies_data):
    """
    Insert a list of movies into Weaviate using the batch dynamic method.
    """
    with client.batch as batch:  # Correct usage of batch
        for movie in movies_data:
            batch.add_data_object(
                movie,
                class_name="Movie"  # Class name in Weaviate schema
            )
    print("Batch insertion completed.")

# Call the function to insert the movies in batch
insert_movies_batch(client, movies_data)
