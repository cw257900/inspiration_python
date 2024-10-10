import warnings
warnings.filterwarnings("ignore")

from IPython.display import JSON 
import json
from unstructured_client import UnstructuredClient
from unstructured_client.models import shared
from unstructured_client.models.errors import SDKError

from unstructured.partition.html import partition_html
from unstructured.partition.pptx import partition_pptx
from unstructured.staging.base import dict_to_elements, elements_to_json

import nltk
nltk.download('punkt')
nltk.download('punkt_tab')
nltk.download('averaged_perceptron_tagger_eng')


from Utils import Utils
utils = Utils()

DLAI_API_KEY = utils.get_dlai_api_key()
DLAI_API_URL = utils.get_dlai_url()

s = UnstructuredClient(
	api_key_auth=DLAI_API_KEY,
	server_url=DLAI_API_URL,
)


from IPython.display import Image
Image(filename="images/HTML_demo.png", height=600, width=600)

filename = "example_files/medium_blog.html"
try:
	elements = partition_html(filename=filename)
	print("\n\n".join([str(el) for el in elements]))
except Exception as e:
	print(f"An error occurred: {e}")





#sample test
data = '{"name":"John", "age":30}'
parsed_data = json.loads(data)
print(parsed_data)