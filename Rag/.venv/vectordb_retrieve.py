import weaviate
import os
import vectordb  # Assuming this is a module where init() is defined
import json

# Initialize your client (assuming it's locally hosted or cloud, depending on your use case)
client = vectordb.init()  # Initialize the client using your `vectordb` module

def get_all_movies(client):
    """
    Query all movies from the "Movie" class and return the result.
    """
    result = client.query.get(
        "Movie",  # The class to query
        ["title", "overview", "vote_average", "genre_ids", "release_date", "tmdb_id"]  # Fields to retrieve
    ).do()

    return result


def get_all_movie_objects(client):
    """
    Get all objects from the "Movie" class and return the result.
    """
    result = client.data_object.get(class_name="Movie")
    
    return result


def main():
    # Call the get_all_movies function
    print("Querying movies with specific fields:")
    movie_data = get_all_movies(client)
    print(json.dumps(movie_data, indent=2))

    # Call the get_all_movie_objects function
    print("\nFetching all movie objects:")
    all_movie_objects = get_all_movie_objects(client)
    print(json.dumps(all_movie_objects, indent=2))


# Call the main function
if __name__ == "__main__":
    main()
