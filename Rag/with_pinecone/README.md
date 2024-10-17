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


