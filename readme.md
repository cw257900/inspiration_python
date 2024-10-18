


## Introduction
------------
an app to chat with private knowledge base build from pdfs <br>
ask question in natural English, app provides relevant reponse based on content from the documents <br>
the app can only respond to questions related to the loaded pdfs

[RAG Reading from Medium](https://medium.com/@florian_algo/list/2334780a5667)

## update requirements.txt 
```
pip install package_name && echo "package_name==$(pip show package_name | grep Version | awk '{print $2}')" >> requirements.txt
```
##

## install and start weaviate db
```
docker-compose up -d  #start docker service as deamon 
source .venv/bin/activate  #active the virtual environment

```


## How It Works
------------

The application follows these steps to provide responses to your questions:

1. PDF Loading: The app reads multiple PDF documents and extracts their text content. <br>
   &emsp;&emsp; &emsp; - load from local in this project;  <br>
   &emsp;&emsp; &emsp; - later can build plugin to read from any sources such as S3, GCP, MongoDB ... <br>

2. Text Chunking: The extracted text is divided into smaller chunks that can be processed effectively.<br>
   &emsp;&emsp; &emsp;- PyPDF2 to read pdf; and langchain CharacterTextSplitter to split text to chunks <br>

3. Language Model: The application utilizes a language model to generate vector representations (embeddings) of the text chunks.
   &emsp;&emsp; &emsp; - weaviately's build in model : text2vec_openai: model="text-embedding-3-large",  dimensions=1024  <br>

4. Similarity Matching: cosine When you ask a question, the app compares it with the text chunks and identifies the most semantically similar ones.<br>

5. Response Generation: The selected chunks are passed to the language model, which generates a response based on the relevant content of the PDFs.<br>


## Dependencies and Installations
----------------------------

1. Weaviate: <br>

   Weaviate integrates well with Hugging Face, OpenAI, Cohere, and other model providers for automatic vector creation. <br>
   It provides GraphQL and REST API support, which can make complex queries easier. <br>
   Weaviate is designed for building applications that require more than just vector search, offering extensive extensibility via plugins. <br>
   Self-Hosted: Weaviate is open-source, so you can self-host it without paying for licenses. However, the cost of managing infrastructure (servers, storage, etc.) will depend on your setup. <br>
   Managed Service: Weaviate Cloud is a managed service where you pay based on usage (compute, storage, queries), but the pricing can vary depending on your deployment size. <br>
   <br>
   - indexInverted: true: This is added to all properties to explicitly indicate that they are filterable (indexed). This is particularly useful when performing searches or queries based on property values (e.g., finding all movies with a certain vote_average). <br>
   - Vector Embeddings: The "vectorizer": "text2vec-openai" setting is already in place, so text properties will automatically generate vector embeddings using OpenAI’s embedding model.

   [Weaviate Tutorials](https://weaviate.io/developers/academy/py/zero_to_mvp) <br>
   

## Usage
-----


## Contributing
------------


