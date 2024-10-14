import weaviate
import os
from dotenv import load_dotenv
import json
from use_cases.pdfs.utils import pdf_processor  # Correct import

# Load environment variables
load_dotenv()

# Set API keys and Weaviate URL from environment variables
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
WEAVIATE_API_KEY = os.getenv("WEAVIATE_API_KEY")  # Weaviate API key
WEAVIATE_URL = os.getenv("WEAVIATE_URL")

# Optional: Add class names to environment variables if needed
WEAVIATE_CLASS_NAME_MOVIE = os.getenv("WEAVIATE_CLASS_NAME_MOVIE", "Movie")
WEAVIATE_CLASS_NAME_PDF = os.getenv("WEAVIATE_CLASS_NAME_PDF", "PDF_Library")

# Test pdf_processor function
pdf_processor.get_text_chunks("This is input test")
