# Chunking and Embedding

## Chunking Strategy

### Options:
- **Extract Text**: Tools like `PyPDF2` or `pdfminer`.
- **Semantic Splitting**: OpenAI GPT, Hugging Face models, or `LangChain`'s `RecursiveCharacterTextSplitter`.

### Selected:
- **CharacterTextSplitter** and **RecursiveCharacterTextSplitter**

---

## Embedding Strategy

### Options:
- **When to Embed**: Pre-embed vectors before loading to Weaviate, or let Weaviate embed during object creation.

### Selected:
- **Weaviate** to embed using **OpenAI's `text-embedding-ada-002`** (1536 dimensions).

---

## Pre-Embedded Vector Approach

1. Embed PDF chunks using external models (e.g., `LangChain OpenAIEmbeddings`).  
2. Store vectors directly in Weaviate, bypassing its internal embedding module.

### Pros:
- Full control over model selection and preprocessing.
- Avoids Weaviate module costs and dependencies.

### Cons:
- More complex embedding management outside Weaviate.

---

## With `moduleConfig` (using `text2vec-openai`)

1. Weaviate handles embedding via `text2vec-openai`.
2. Embedding happens automatically during object creation.

### Pros:
- Simplifies embedding process; direct integration with OpenAI.
  
### Cons:
- Dependent on external services; less control over the process.

---

## Key Differences

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
