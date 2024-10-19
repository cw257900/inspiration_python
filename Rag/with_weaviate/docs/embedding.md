## Embedding strategy

    1. For doc with text based files, embedded with weaviate to streamline the process 
    2. For doc needs process image, or special customized formular, use more customized embedding outstide Weaviate


## Pre-embeded Vector Approach 
------------
```
what happens  

    1. System embedded the PDF chuncks using separate model : langchain_openai's OpenAIEmbeddings. code - vectordb_create.py  
    2. vectors provided will be stored as-is in Weaviate, bypass Weaviate's module-based embedding and handle vectorization outside Weaviate  

Workflow  
    1. You embed the text outside of Weaviate (e.g., using OpenAI’s API).  
    2. You store this vector in the Weaviate object by specifying the vector parameter when creating the object. 
    3. Weaviate uses this precomputed vector for similarity searches. 

Pros: 
    1. Full control over the embeddings (e.g., choice of model, pre-processing, and optimization). 
    2. Avoid extra API costs or dependencies on Weaviate's built-in modules. 
    3. Flexibility to switch models without affecting the Weaviate setup. 

Cons: 
    1. You are responsible for handling the entire embedding pipeline. 
    2. Potential extra complexity if managing large volumes of data and embeddings outside Weaviate. 
```

## With moduleConfig using text2vec-openai for text-embedding-ada-002 (or another model)
------------
```
What happens:
    If you specify moduleConfig like text2vec-openai, Weaviate will handle embedding the text for you at the time of object creation. Specifically, for OpenAI’s embedding, Weaviate will call the OpenAI API to generate embeddings for the text you provide in the object's properties.
    The moduleConfig points to a specific vectorization module (e.g., text2vec-openai) and configures Weaviate to use that module to embed the text before saving it.

Example Workflow:
    You create an object in Weaviate without pre-embedding the text.
    The text is passed to the OpenAI embedding model (via Weaviate’s text2vec-openai module).
    The resulting vector is automatically generated and stored in Weaviate.

Pros:
    No need to handle the embedding yourself, which simplifies the pipeline.
    Direct integration with powerful models like OpenAI's text embedding.
    Automatically handled by Weaviate, which can be more efficient for smaller projects.

Cons:
    Dependent on Weaviate's module and external service (e.g., OpenAI).
    Additional costs may be incurred for embedding API usage.
    Less control over the embedding process (you have to trust Weaviate’s module configuration).
```
## Key Differences:
------------
```
    Control Over Embeddings:
        Without moduleConfig: You have full control over which embedding model to use and can fine-tune or preprocess your data accordingly.
        With moduleConfig: Weaviate decides the embedding process for you based on the chosen module (e.g., text2vec-openai).
   
    Embedding Process:
        Without moduleConfig: You embed the data outside Weaviate, so Weaviate only handles storage and search over the provided vectors.
        With moduleConfig: Weaviate handles both the embedding and the storage processes.
   
    Cost and API Calls:
        Without moduleConfig: You avoid additional API calls through Weaviate but may incur costs elsewhere (if using external embedding tools).
        With moduleConfig: You may incur OpenAI API costs when using their embedding model via Weaviate.
   
    Embedding Flexibility:
        Without moduleConfig: You can switch embedding models and strategies easily, but it requires external management.
        With moduleConfig: You are tied to the module defined in Weaviate, such as OpenAI’s model.
```