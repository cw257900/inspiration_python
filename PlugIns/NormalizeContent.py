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
nltk.download('averaged_perceptron_tagger_eng')

from Utils import Utils
utils = Utils()

DLAI_API_KEY = utils.get_dlai_api_key()
DLAI_API_URL = utils.get_dlai_url()


 # Display the image as part of initialization
from IPython.display import Image
Image(filename="images/HTML_demo.png", height=600, width=600)

class NormalizeContent: 

    def __init__(self, filename):
        self.filename = filename
       

    def json_outof_html(self):
        try:
            # Assuming partition_html is defined or imported
            elements = partition_html(filename=self.filename)
            #print(elements)
            total_elements = len(elements)
            print(f"Total elements: {total_elements}")

            element_dict = [el.to_dict() for el in elements]

            # Print elements 11 to 13
            example_output = json.dumps(element_dict[11:13], indent=2)
            print(f"Elements 11 to 13: {example_output}")

        except Exception as e:
            print(f"An error occurred: {e}")

    def json_outof_pdf(self):
        try:
            s = UnstructuredClient(
				api_key_auth=DLAI_API_KEY,
				server_url=DLAI_API_URL,
			)
			
            # Read the file content
            with open(self.filename, "rb") as f:
                files = shared.Files(
                    content=f.read(), 
                    file_name=self.filename,
                )

            # Prepare the request
            req = shared.PartitionParameters(
                files=files,
                strategy='hi_res',
                pdf_infer_table_structure=True,
                languages=["eng"],
            )

            # Send the partition request and print the first 3 elements
            print(dir(s))
            resp = s.general.partition(req)
            print(json.dumps(resp.elements[:3], indent=2))

        except SDKError as e:
            print(f"An SDK error occurred: {e}")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")

# Main function to execute the class
def main():

    processor = NormalizeContent( filename = "example_files/el_nino.html" )   
    processor.json_outof_html()
    

# Entry point for the script
if __name__ == "__main__":
    main()
