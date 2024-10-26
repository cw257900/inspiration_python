import torch
from torchvision import models, transforms
from torchvision.models import ResNet50_Weights
from PIL import Image
import pytesseract
import hashlib
from datetime import datetime
import logging
from pathlib import Path
from typing import Optional, Dict  # <-- Make sure this is added
import os, sys

# Add the parent directory (or wherever "with_pinecone" is located) to the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from vector_stores import vector_stores as vector_store
from utils import utils
from configs import configs
from dotenv import load_dotenv
load_dotenv()


import warnings
# Suppress ResourceWarnings
warnings.filterwarnings("ignore", category=ResourceWarning)


class ImageProcessor:
    def __init__(self, model=None, logger=None):
         # Load the pre-trained ResNet model using the updated 'weights' parameter
        self.model = model or models.resnet50(weights=ResNet50_Weights.IMAGENET1K_V1)
        self.model.eval()  # Set the model to evaluation mode
        self.logger = logger or logging.getLogger(__name__)

        # Define the transformations to apply to the image
        self.transform = transforms.Compose([
            transforms.Resize((224, 224)),  # Resize the image to 224x224
            transforms.ToTensor(),  # Convert the image to a PyTorch tensor
            transforms.Normalize(  # Normalize the image (using ImageNet means/stds)
                mean=[0.485, 0.456, 0.406],
                std=[0.229, 0.224, 0.225]
            )
        ])

    def compute_embedding(self, image: Image.Image) -> torch.Tensor:

          # Ensure the image is in RGB format
        if image.mode != "RGB":
            image = image.convert("RGB")
       
        
        # Transform the image
        image_tensor = self.transform(image).unsqueeze(0)  # convert the image to the shape [1, 3, 224, 224],as input to a neural network model that expects batches of images.

         # Verify the shape after transformation
        if image_tensor.shape[1] != 3:
            raise ValueError(f"Image tensor has unexpected shape {image_tensor.shape}. Expected [1, 3, 224, 224].")


        # Generate embeddings using the model
        with torch.no_grad():
            embedding = self.model(image_tensor)

        return embedding.squeeze()  # Remove the batch dimension

    def process_image(self, image_path: str, metadata: Optional[Dict] = None) -> Dict:
       
        try:
            # Read image using PIL
            image = Image.open(image_path)
            
            # Extract text from the image using Tesseract
            extracted_text = pytesseract.image_to_string(image, lang='eng')

            # Print the extracted text
            print("11111  Extracted Text:", extracted_text)
            
            # Compute file hash
            file_hash = hashlib.sha256(image.tobytes()).hexdigest()
            
            # Compute embedding for the image
            embedding = self.compute_embedding(image)
            
            # Prepare document object with metadata
            document = {
                "file_hash": file_hash,
                "source": Path(image_path).name,
                "processing_dt": datetime.now().isoformat(),
                "page_content": extracted_text, 
                "page_number": 1  # Assuming single image
            }
            
            return document, embedding.tolist()  # Convert the embedding to a list for easier serialization
            
        except Exception as e:
            self.logger.error(f"Error processing image {image_path}: {str(e)}")
            raise

def main():
    # Load environment variables inside main
    image_path = os.getenv("LOCAL_FILE_INPUT_PATH")
    
    if not image_path:
        print("Error: LOCAL_FILE_INPUT_PATH is not set in the .env file.")
        return

    # Initialize the image processor with a pre-trained ResNet model
    processor = ImageProcessor()

    # Process the image and get the document metadata and embedding
    doc, embedding = processor.process_image(image_path)
    
    # Print the results
    print("imagePath:", image_path)
    print("Document Metadata:", doc)

if __name__ == "__main__":
    main()
