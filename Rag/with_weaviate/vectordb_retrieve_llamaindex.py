from llama_index.llms import openai
from llama_index import VectorstoreIndex, SimpleDirectoryReader
from IPython.display import Markdown, display 


documents = SimpleDirectoryReader('./data/input_files').load_data()
index = VectorstoreIndex.from_documents(documents)

query_engine = index.as_query_engine()
query = "What is the meaning of life?"
response = query_engine.query(query)
print(Markdown(response.response))  



def main():
    pass
def __main__():
    main()