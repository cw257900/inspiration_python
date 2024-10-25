import os
import sys
from typing import Dict, List, Optional
import pytesseract
from PIL import Image
import weaviate
from weaviate.collections import Collection
from weaviate.config import ConnectionConfig
import torch
from transformers import AutoTokenizer, AutoModel
from datetime import datetime
import logging
import hashlib
from pathlib import Path
# Add the parent directory (or wherever "with_pinecone" is located) to the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from vector_stores import vector_stores 

class DocumentProcessor:
    def __init__(self, batch_size: int = 100):
        """
        Initialize the document processor with Weaviate connection and models.
        
        Args:
            batch_size: Size of batches for processing documents
        """
        # Initialize Weaviate client with v4 syntax
        #self.client = weaviate.Client(connection_config=ConnectionConfig.from_url("http://localhost:8080"))
        self.client = vector_stores.create_client()
        self.batch_size = batch_size
        
        # Initialize the tokenizer and model for embeddings
        self.tokenizer = AutoTokenizer.from_pretrained('sentence-transformers/all-mpnet-base-v2')
        self.model = AutoModel.from_pretrained('sentence-transformers/all-mpnet-base-v2')
        
        # Setup logging
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger(__name__)
        
        # Create collection if it doesn't exist
        self._ensure_collection()
        
        # Store collection reference
        self.collection = self.client.collections.get("Document")

    def _ensure_collection(self):
        """Create the Weaviate collection for documents if it doesn't exist."""
        try:
            # Define properties for the collection
            properties = {
                "content": {
                    "dataType": ["text"],
                    "description": "The OCR extracted text content"
                },
                "filename": {
                    "dataType": ["string"],
                    "description": "Original filename"
                },
                "fileHash": {
                    "dataType": ["string"],
                    "description": "SHA-256 hash of file content"
                },
                "processingDate": {
                    "dataType": ["date"],
                    "description": "Date when the document was processed"
                },
                "pageCount": {
                    "dataType": ["int"],
                    "description": "Number of pages in document"
                },
                "metadata": {
                    "dataType": ["object"],
                    "description": "Additional metadata about the document"
                }
            }
            
            # Create collection with config
            self.client.collections.create(
                name="Document",
                properties=properties,
                vectorizer_config=None,  # We'll provide our own vectors
                vector_index_config={"distance": "cosine"},
                generative_config=None
            )
            
            self.logger.info("Created Document collection in Weaviate")
        except Exception as e:
            if "already exists" not in str(e):
                raise e
            self.logger.info("Document collection already exists")

    def compute_embedding(self, text: str) -> List[float]:
        """
        Compute embedding for the given text using the loaded model.
        
        Args:
            text: Input text to embed
            
        Returns:
            List of embedding values
        """
        # Tokenize and prepare for model
        inputs = self.tokenizer(text, padding=True, truncation=True, 
                              max_length=512, return_tensors="pt")
        
        # Generate embeddings
        with torch.no_grad():
            outputs = self.model(**inputs)
            embeddings = outputs.last_hidden_state.mean(dim=1)
        
        return embeddings[0].tolist()

    def process_image(self, image_path: str, metadata: Optional[Dict] = None) -> Dict:
        """
        Process a single image document using OCR.
        
        Args:
            image_path: Path to the image file
            metadata: Optional additional metadata
            
        Returns:
            Dictionary containing processed document information and its embedding
        """
        try:
            # Read image using PIL
            image = Image.open(image_path)
            
            # Perform OCR
            text_content = pytesseract.image_to_string(image)
            
            # Compute file hash
            file_hash = hashlib.sha256(image.tobytes()).hexdigest()
            
            # Compute embedding
            embedding = self.compute_embedding(text_content)
            
            # Prepare document object
            document = {
                "content": text_content,
                "filename": Path(image_path).name,
                "fileHash": file_hash,
                "processingDate": datetime.now().isoformat(),
                "pageCount": 1,  # Single image
                "metadata": metadata or {}
            }
            
            return document, embedding
            
        except Exception as e:
            self.logger.error(f"Error processing image {image_path}: {str(e)}")
            raise

    def batch_process_directory(self, directory_path: str, file_pattern: str = "*.png"):
        """
        Process all matching images in a directory and store in Weaviate.
        
        Args:
            directory_path: Path to directory containing images
            file_pattern: Pattern to match image files
        """
        paths = list(Path(directory_path).glob(file_pattern))
        self.logger.info(f"Found {len(paths)} files to process")
        
        # Create configuration for the batch
        with self.collection.batch.fixed_size(batch_size=self.batch_size) as batch:
            for path in paths:
                try:
                    # Process document
                    doc, embedding = self.process_image(str(path))
                    
                    # Add to batch
                    batch.add_object(
                        properties=doc,
                        vector=embedding
                    )
                    
                    self.logger.info(f"Processed and stored document: {path.name}")
                    
                except Exception as e:
                    self.logger.error(f"Error processing {path}: {str(e)}")
                    continue

    def search_similar_documents(self, query_text: str, limit: int = 5) -> List[Dict]:
        """
        Search for similar documents using text query.
        
        Args:
            query_text: Text to search for
            limit: Maximum number of results to return
            
        Returns:
            List of similar documents
        """
        # Compute query embedding
        query_embedding = self.compute_embedding(query_text)
        
        # Perform vector search using v4 syntax
        results = (
            self.collection.query
            .near_vector(
                vector=query_embedding,
                limit=limit
            )
            .with_additional(["distance"])
            .with_fields(["content", "filename", "processingDate", "metadata"])
            .do()
        )
        
        return results.objects

    def delete_all_documents(self):
        """Delete all documents from the collection."""
        try:
            self.collection.data.delete_many()
            self.logger.info("Deleted all documents from collection")
        except Exception as e:
            self.logger.error(f"Error deleting documents: {str(e)}")

# Example usage
if __name__ == "__main__":
    # Initialize processor
    processor = DocumentProcessor()
    
    # Process a directory of images
    processor.batch_process_directory(
        directory_path="./documents",
        file_pattern="*.png"
    )
    
    # Search for similar documents
    results = processor.search_similar_documents(
        query_text="example query",
        limit=5
    )
    
    # Print results with distances
    for result in results:
        print(f"Document: {result.properties['filename']}")
        print(f"Distance: {result.metadata['distance']}")
        print(f"Content Preview: {result.properties['content'][:100]}...\n")