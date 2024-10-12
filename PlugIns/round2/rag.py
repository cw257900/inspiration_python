import pdfplumber
from sentence_transformers import SentenceTransformer
from PIL import Image
import pinecone
from pinecone import Pinecone
from transformers import CLIPProcessor, CLIPModel
from dotenv import load_dotenv
import os
import numpy as np

load_dotenv()

# Fetch required environment variables
pdf_directory = os.getenv("PDF_FILE_INPUT_DIR")
pinecone_api_key = os.getenv("PINECONE_API_KEY")
pinecone_index_name = os.getenv("PINECONE_INDEX_NAME")

# Initialize models
#text_model = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')
# Replace with a model that generates 512-dimensional embeddings
text_model = SentenceTransformer('sentence-transformers/paraphrase-MiniLM-L6-v2')

image_model = CLIPModel.from_pretrained("openai/clip-vit-base-patch32")
image_processor = CLIPProcessor.from_pretrained("openai/clip-vit-base-patch32")

# Initialize Pinecone
pc = Pinecone(api_key=pinecone_api_key)
index = pc.Index(pinecone_index_name)

def pad_embedding(embedding, target_dim=512):
    if len(embedding) < target_dim:
        embedding = np.pad(embedding, (0, target_dim - len(embedding)), 'constant')
    else:
        embedding = embedding[:target_dim]
    return embedding


def pad_image_embedding(embedding, target_dim=512):
    """
    Pad the dimensionality of image embeddings from 384 to 512 by appending zeros.
    
    Args:
    - embedding (np.ndarray or torch.Tensor): The original image embeddings (384 dimensions).
    - target_dim (int): The target dimensionality, default is 512.

    Returns:
    - padded_embedding (np.ndarray): Embeddings with adjusted dimensionality.
    """
    if isinstance(embedding, list):
        embedding = np.array(embedding)

    if isinstance(embedding, np.ndarray) is False:
        embedding = embedding.detach().cpu().numpy()

    embedding = embedding.flatten()

    if embedding.shape[0] < target_dim:
        padded_embedding = np.pad(embedding, (0, target_dim - embedding.shape[0]), 'constant')
    else:
        padded_embedding = embedding[:target_dim]  # Truncate if larger than target_dim

    return padded_embedding

# Extract content from PDF
def extract_pdf_content(pdf_path):
    text_content = []
    image_content = []
    table_content = []

    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            text = page.extract_text()
            if text:
                text_content.append(text)
            
            tables = page.extract_tables()
            if tables:
                table_content.extend(tables)
            
            images = page.images
            if images:
                image_content.extend(images)

    print(text_content)
    return text_content, table_content, image_content

# Modify to allow testing specific types of content
def generate_embedding(text_content=None, table_content=None, image_content=None):
    text_embeddings = text_model.encode(text_content) if text_content else []
    text_embeddings = [pad_embedding(embedding) for embedding in text_embeddings]


    table_embeddings = [text_model.encode('\n'.join([' '.join(row) for row in table])) 
                        for table in table_content] if table_content else []
    table_embeddings = [pad_embedding(embedding) for embedding in table_embeddings]

    image_embeddings = []
    if image_content:
        for image in image_content:
            image_embedding = image_model.get_image_features(
                **image_processor(images=Image.new("RGB", (100, 100)), return_tensors="pt")
            )
            image_embedding_adjusted = pad_image_embedding(image_embedding, 512)
            image_embeddings.append(image_embedding_adjusted)

    return text_embeddings, table_embeddings, image_embeddings

# Upload embeddings to Pinecone
# Upload embeddings to Pinecone
def upload_embeddings(text_embeddings=None, table_embeddings=None, image_embeddings=None):

    # Check if text_embeddings exist and have elements
    if text_embeddings is not None and len(text_embeddings) > 0 and np.any(text_embeddings):
        for i, text_embedding in enumerate(text_embeddings):
            index.upsert(vectors=[(f"text_vector_{i}", text_embedding)])

    # Check if table_embeddings exist and have elements
    if table_embeddings is not None and len(table_embeddings) > 0 and np.any(table_embeddings):
        for i, table_embedding in enumerate(table_embeddings):
            index.upsert(vectors=[(f"table_vector_{i}", table_embedding)])

    # Check if image_embeddings exist and have elements
    if image_embeddings is not None and len(image_embeddings) > 0 and np.any(image_embeddings):
        for i, image_embedding in enumerate(image_embeddings):
            index.upsert(vectors=[(f"image_vector_{i}", image_embedding)])

# Main function to process a PDF and upload embeddings
def main(pdf_file_path, embed_text=True, embed_table=False, embed_image=False):
    text_content, table_content, image_content = extract_pdf_content(pdf_file_path)

    text_embeddings, table_embeddings, image_embeddings = generate_embedding(
        text_content if embed_text else None,
        table_content if embed_table else None,
        image_content if embed_image else None
    )

    upload_embeddings(
        text_embeddings if embed_text else None,
        table_embeddings if embed_table else None,
        image_embeddings if embed_image else None
    )

if __name__ == "__main__":
    pdf_file_path = "data/input_pdfs/emphasis-text.pdf"
    main(pdf_file_path, embed_text=True, embed_table=True, embed_image=True)
