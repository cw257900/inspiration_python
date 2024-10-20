# Chunking and Embedding


## Chunking Strategy

Options:
- Extract Text: tools as `PyPDF2` or `pdfminer`.
- Semantic Splitting: OpenAI GPT, Hugging Face models, or `LangChain`'s `RecursiveCharacterTextSplitter`.

Selected:
- CharacterTextSplitter, RecursiveCharacterTextSplitter

---





## Embedding Strategy
#### Pre-Embedded Vector Approach

Where to do the Embedding:
1. Pre-embed vectors before loading to Weaviate, or 
2. Use [Weaviate embed](https://weaviate.io/developers/weaviate/concepts/vector-quantization) during object creation. 

What models to use:
1. openai: 
- text-embedding-3-large, dimensions: 3072 
- text-embedding-ada-002, dimensions: 1536 
- text-embedding-3-small,dimensions: 1536 
2. cohere: 
-   name=multilingual-22-12, dimension=768,semgments=384, 256, 192, 96 
3. huggingface: 
-   sentence-transformers/all-MiniLM-L12-v2, dimention=384, segments=192, 128, 96 

Selected: 
```
    Weaviate to embed: text2vec-openai text-embedding-ada-002, dimensions: 1536, max token 8191
    vectorizer_config=
            wvc.config.Configure.Vectorizer.text2vec_openai(
                model="text-embedding-ada-002",
                name="page_content",
                source_properties="page_content"
            ),    # Set the vectorizer to "text2vec-openai" to use the OpenAI API for vector-related operations
            generative_config=wvc.config.Configure.Generative.cohere(
                name="tiles", 
                source="page_content"
            ),             
```

---
## Embedding Approach Analysis


#### Pre-Embedded Vector Approach

1. Embed PDF chunks using external models (e.g., `LangChain OpenAIEmbeddings`).  
2. Store vectors directly in Weaviate, bypassing its internal embedding module.

Pros:
- Full control over model selection and preprocessing.
- Avoids Weaviate module costs and dependencies.

Cons:
- More complex embedding management outside Weaviate.

---

#### With `moduleConfig` (using `text2vec-openai`)

1. Weaviate handles embedding via `text2vec-openai`.
2. Embedding happens automatically during object creation.

- Simplifies embedding process; direct integration with OpenAI.
  
- Dependent on external services; less control over the process.

---

### Key Differences

- **Control**:  
  - Without `moduleConfig`: Full control over embeddings.  
  - With `moduleConfig`: Weaviate manages embeddings.
  
- **Process**:  
  - Without: You handle embeddings externally.  
  - With: Weaviate handles everything.

- **Costs**:  
  - Without: Avoids Weaviate API costs.  
  - With: API costs via Weaviate modules.

- **Flexibility**:  
  - Without: Switch models easily.  
  - With: Tied to Weaviate’s modules.
