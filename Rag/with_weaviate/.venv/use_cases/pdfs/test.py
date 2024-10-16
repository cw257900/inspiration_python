import uuid
import vectordb_init 
import config

def insert_vectorized_data(class_name, pdf_name, pdf_content, pdf_chunk_id):

    client = vectordb_init(config.class_name)
    print ("start")
    """
    Insert data into a vectorized class in Weaviate. The vectorization will automatically occur on text fields.
    """
    # Define the data object to be inserted
    data_object = {
        "pdf_name": pdf_name,
        "pdf_content": pdf_content,
        "pdf_chunk_id": pdf_chunk_id
    }

    # Generate a UUID for the object
    object_id = str(uuid.uuid4())

    try:
        # Insert the data object into the class
        client.data_object.create(
            data_object,
            class_name=class_name,
            uuid=object_id
        )
        print(f"Data object with UUID {object_id} inserted successfully into '{class_name}'")
    except Exception as e:
        print(f"Error inserting data object: {e}")


# After creating the vectorized class (e.g., "PDF_Vector_Collection")
class_name = "PDF_Vector_Collection"

# Insert a sample PDF chunk
pdf_name = "Sample PDF Document"
pdf_content = "This is a chunk of the PDF document text."
pdf_chunk_id = "chunk_1"

# Insert the vectorized data
insert_vectorized_data( class_name, pdf_name, pdf_content, pdf_chunk_id)
