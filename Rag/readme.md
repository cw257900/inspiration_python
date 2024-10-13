


## Introduction
------------
an app to chat with private knowledge base build from pdfs <br>
ask question in natural English, app provides relevant reponse based on content from the documents <br>
the app can only respond to questions related to the loaded pdfs


## How It Works
------------

The application follows these steps to provide responses to your questions:

1. PDF Loading: The app reads multiple PDF documents and extracts their text content. <br>
   &emsp;&emsp; &emsp; - load from local in this project;  <br>
   &emsp;&emsp; &emsp; - later can build plugin to read from any sources such as S3, GCP, MongoDB ... <br>

2. Text Chunking: The extracted text is divided into smaller chunks that can be processed effectively.<br>
   &emsp;&emsp; &emsp;- PyPDF2 to read pdf; and langchain CharacterTextSplitter to split text to chunks <br>

3. Language Model: The application utilizes a language model to generate vector representations (embeddings) of the text chunks.
   &emsp;&emsp; &emsp; - weaviately's build in model  <br>

4. Similarity Matching: When you ask a question, the app compares it with the text chunks and identifies the most semantically similar ones.<br>

5. Response Generation: The selected chunks are passed to the language model, which generates a response based on the relevant content of the PDFs.<br>


## Dependencies and Installation
----------------------------

1. Weaviate: <br>

   Weaviate integrates well with Hugging Face, OpenAI, Cohere, and other model providers for automatic vector creation. <br>
   It provides GraphQL and REST API support, which can make complex queries easier. <br>
   Weaviate is designed for building applications that require more than just vector search, offering extensive extensibility via plugins. <br>
   Self-Hosted: Weaviate is open-source, so you can self-host it without paying for licenses. However, the cost of managing infrastructure (servers, storage, etc.) will depend on your setup. <br>
   Managed Service: Weaviate Cloud is a managed service where you pay based on usage (compute, storage, queries), but the pricing can vary depending on your deployment size. <br>

## Usage
-----


## Contributing
------------


