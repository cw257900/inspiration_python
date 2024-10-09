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

#sample test
data = '{"name":"John", "age":30}'
parsed_data = json.loads(data)
print(parsed_data)