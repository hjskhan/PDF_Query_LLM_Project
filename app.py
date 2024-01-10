import streamlit as st
from langchain.indexes.vectorstore import VectorStoreIndexWrapper
from langchain.llms import OpenAI
from langchain.text_splitter import CharacterTextSplitter
from langchain_community.vectorstores import Cassandra
from langchain.embeddings.openai import OpenAIEmbeddings
from PyPDF2 import PdfReader
import cassio
import os
from dotenv import load_dotenv


# Load environment variables from .env file
load_dotenv()

ASTRA_DB_APPLICATION_TOKEN = os.getenv('ASTRA_DB_APPLICATION_TOKEN')
ASTR_DB_ID = os.getenv('ASTR_DB_ID')
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')

# Debug: Print API keys to check if they are loaded correctly
print(f"ASTRA_DB_APPLICATION_TOKEN: {ASTRA_DB_APPLICATION_TOKEN}")
print(f"ASTR_DB_ID: {ASTR_DB_ID}")
print(f"OPENAI_API_KEY: {OPENAI_API_KEY}")


# AstraDB connection and vector store initialization
def initialize_astra_vector_store():
    cassio.init(token=ASTRA_DB_APPLICATION_TOKEN, database_id=ASTR_DB_ID)
    llm = OpenAI(openai_api_key = OPENAI_API_KEY)
    embedding = OpenAIEmbeddings(openai_api_key = OPENAI_API_KEY)

    astra_vector_store = Cassandra(
        embedding = embedding,
        table_name= 'pdfquery02',
        session = None,
        keyspace = None
    )
    return astra_vector_store

# Function to preprocess the uploaded file
def preprocessor(uploaded_file, astra_vector_store):
    pdf_reader = PdfReader(uploaded_file)
    raw_text = ''
    for page in pdf_reader.pages:
        content = page.extract_text()
        if content:
            raw_text += content

    text_splitter = CharacterTextSplitter(
        separator='\n',
        chunk_size=800,
        chunk_overlap=200,
        length_function=len
    )
    texts = text_splitter.split_text(raw_text)

    astra_vector_store.add_texts(texts)
    astra_vector_index = VectorStoreIndexWrapper(vectorstore=astra_vector_store)

    return astra_vector_index

def perform_query(query_text,astra_vector_index):
    llm = OpenAI(openai_api_key = OPENAI_API_KEY)
    answer = astra_vector_index.query(query_text, llm=llm).strip()
    return answer


# Streamlit UI
def main():
    
    st.title('Your PDF Query App')

    uploaded_file = st.file_uploader("Upload a PDF file", type="pdf")

    if uploaded_file is not None:
        astra_vector_store = initialize_astra_vector_store()  # Initialize once before processing
        astra_vector_index = preprocessor(uploaded_file, astra_vector_store)
        query_text = st.text_input('Enter your query here:')
        
    
        if st.button('Get Answer'):
            if query_text:
                answer = perform_query(query_text, astra_vector_index)
                st.write(f'Question: {query_text}')
                st.write(f'Answer: {answer}')
            else:
                st.write('Please enter a query!')

if __name__ == '__main__':
    main()
