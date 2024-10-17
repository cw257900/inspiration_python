# Inspiration Python

This is a project to demo code to build private pdf based knowledge base into pinecone vectore store, to enable LLM inquiries


## Using Pipenv 

```
# Install dependencies
pipenv install

# Create a virtual environment
pipenv shell

```

## Using Venv 

These instructions are included if you wish to use venv to manage your evironment and dependencies instead of Pipenv.

```
# Create the venv virtual environment
python -m venv .venv

# On MacOS, WSL, Linux
source .venv/bin/activate

# On Windows
.\.venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Initialize the database
flask --app app.web init-db
```

## Reference
```
https://medium.com/ai-in-plain-english/advanced-rag-03-using-ragas-llamaindex-for-rag-evaluation-84756b82dca7 (validation )
https://medium.com/@florian_algo/list/2334780a5667
https://medium.com/search?q=RAGAS
https://medium.com/search?q=Graph+RAG
https://medium.com/search?q=Semantic+RAG
https://medium.com/search?q=SWARM+in+LLM

```


## Steps : with asynchronized upsert to Pinecone
```
async def create_embeddings_for_pdf():

    print(f"1. split file into chunks: pdf_file_path: {pdf_file_path}")
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200,
        length_function=len    
    )
    print (text_splitter)

    print(f"2. load file with splitter to doc object")
    docs = PyPDFLoader(pdf_file_path).load_and_split(text_splitter)

    print(f"3. embed documents")
    embedded_docs = [await embeddings.embeddings.aembed_documents([doc.page_content]) for doc in docs]

    print(f"4. upload the embeded vectors to pinecone")
    pinecone_vector_store.vector_store.upsert(vectors=embedded_docs)
    
    print(f"5. done: pdf_file_path: {pdf_file_path}")
    

if __name__ == "__main__":
   asyncio.run(create_embeddings_for_pdf())

```