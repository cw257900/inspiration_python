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
'''
https://medium.com/ai-in-plain-english/advanced-rag-03-using-ragas-llamaindex-for-rag-evaluation-84756b82dca7 (validation )
https://medium.com/@florian_algo/list/2334780a5667
https://medium.com/search?q=RAGAS
https://medium.com/search?q=Graph+RAG
https://medium.com/search?q=Semantic+RAG
https://medium.com/search?q=SWARM+in+LLM


'''


