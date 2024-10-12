from sentence_transformers import SentenceTransformer
from transformers import CLIPProcessor, CLIPModel
from PIL import Image
import torch
import io

# Load models
text_embedding_model = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')
clip_model = CLIPModel.from_pretrained("openai/clip-vit-base-patch32")
clip_processor = CLIPProcessor.from_pretrained("openai/clip-vit-base-patch32")

# Function to generate embeddings for text and images
def generate_embeddings(content):
    embeddings = []
    
   
    for item in content:
        # Debugging: print the item to see what structure it has
        #print(f"Processing item: {item}")
        
        if 'type' not in item:
            # print(f"Warning: Item missing 'type' key: {item}")
            continue  # Skip this item if it doesn't have a 'type' key
        
        if item['type'] == 'text':
            # Generate text embeddings
            embedding = generate_text_embedding(item['value'])
            embeddings.append({'id': item.get('id', 'text_id'), 'values': embedding})
        elif item['type'] == 'image':
            # Generate image embeddings
            embedding = generate_image_embedding(item['value'])
            embeddings.append({'id': item.get('id', 'image_id'), 'values': embedding})
        else:
            print(f"Unknown item type: {item['type']}")

    return embeddings

# Subfunction to generate text embeddings
def generate_text_embedding(text):
    """
    Generate embeddings for the provided text using SentenceTransformer.
    """
    print(f"Generating text embedding for: {text}")
    # Encode the text using the SentenceTransformer model
    embedding = text_embedding_model.encode(text).tolist()
    return embedding

# Subfunction to generate image embeddings
def generate_image_embedding(image_data):
    """
    Generate embeddings for the provided image using CLIP.
    image_data should be in bytes or PIL.Image format.
    """
    print(f"Generating image embedding.")
    
    # Check if the image data is in bytes or a file path, convert it to a PIL Image
    if isinstance(image_data, bytes):
        image = Image.open(io.BytesIO(image_data))
    elif isinstance(image_data, str):
        image = Image.open(image_data)
    else:
        image = image_data  # Assume it's already a PIL Image

    # Process the image using CLIPProcessor
    inputs = clip_processor(images=image, return_tensors="pt", padding=True)
    
    # Get image embeddings from the CLIP model
    with torch.no_grad():
        image_embedding = clip_model.get_image_features(**inputs).squeeze().tolist()
    
    return image_embedding


# Run the main process
"""""
if __name__ == "__main__":
   content = [
        {'id': 'text1', 'type': 'text', 'value': 'What is artificial intelligence?'},
        #{'id': 'image1', 'type': 'image', 'value': 'path/to/image.jpg'}
    ]
   
   embeddings = generate_embeddings(content)
   #print(f"Generated Embeddings: {embeddings}")

"""