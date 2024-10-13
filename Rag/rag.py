
import os
import streamlit as st
from dotenv import load_dotenv

load_dotenv()

API_KEY_OPENAI=os.getenv("API_KEY_OPENAI")
API_TOKEN_HUGGENFACE=os.getenv("")

def main():
    st.set_page_config(page_title="Chat with Connie", page_icon=":books:")
    st.header("Chat with Connie :books: ")
    st.text_input ("Ask Connie:")

    with st.sidebar:
        st.subheader("Upload documents")
        st.file_uploader("Upload PDFs here, click on process to continue" )
        st.button("Process")

    if __name__ == '__main__':
        main()