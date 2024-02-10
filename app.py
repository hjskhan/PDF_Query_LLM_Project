from flask import Flask, render_template, request, redirect, url_for, session
from flask_session import Session
import os
from langchain.indexes.vectorstore import VectorStoreIndexWrapper
from langchain.llms import OpenAI
from langchain.text_splitter import CharacterTextSplitter
from langchain_community.vectorstores import Cassandra
from langchain.embeddings.openai import OpenAIEmbeddings
from PyPDF2 import PdfReader
from docx import Document
import cassio
from dotenv import load_dotenv
import exception

app = Flask(__name__)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)


# Load environment variables from .env file
load_dotenv(override=True)

ASTRA_DB_APPLICATION_TOKEN = os.getenv('ASTRA_DB_APPLICATION_TOKEN')
ASTR_DB_ID = os.getenv('ASTR_DB_ID')
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
app.secret_key = 'your_secret_key_here'


# AstraDB connection and vector store initialization
def initialize_astra_vector_store():
    cassio.init(token=ASTRA_DB_APPLICATION_TOKEN, database_id=ASTR_DB_ID)
    llm = OpenAI(openai_api_key=OPENAI_API_KEY)
    embedding = OpenAIEmbeddings(openai_api_key=OPENAI_API_KEY)

    astra_vector_store = Cassandra(
        embedding=embedding,
        table_name='pdfquery02',
        session=None,
        keyspace=None
    )
    return astra_vector_store

# Function to preprocess the uploaded file

def preprocessor(uploaded_file):
    if uploaded_file.filename.endswith('.pdf'):
        return preprocess_pdf(uploaded_file)
    elif uploaded_file.filename.endswith(('.doc', '.docx')):
        return preprocess_word(uploaded_file)

def preprocess_pdf(uploaded_file):
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
    return texts

def preprocess_word(uploaded_file):
    document = Document(uploaded_file)
    raw_text = ''
    for paragraph in document.paragraphs:
        raw_text += paragraph.text

    text_splitter = CharacterTextSplitter(
        separator='\n',
        chunk_size=800,
        chunk_overlap=200,
        length_function=len
    )
    texts = text_splitter.split_text(raw_text)
    return texts


def perform_query(query_text, astra_vector_index):
    llm = OpenAI(openai_api_key=OPENAI_API_KEY)
    answer = astra_vector_index.query(query_text, llm=llm).strip()
    return answer

# Define Flask routes
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload():
    if request.method == 'POST':
        uploaded_file = request.files['file']
        if uploaded_file:
            session['texts'] = preprocessor(uploaded_file)
    return render_template('query.html')

@app.route('/query', methods=['POST'])
def query():
    query_text = request.form['query_text']
    texts = session.get('texts')

    astra_vector_store = initialize_astra_vector_store()  # Initialize once before processing
    astra_vector_store.add_texts(texts)
    astra_vector_index = VectorStoreIndexWrapper(vectorstore=astra_vector_store)

    if not query_text:
        return render_template('query.html', astra_vector_index=astra_vector_index, message='Please enter a query!')

    answer = perform_query(query_text, astra_vector_index)
    return render_template('query.html', query_text=query_text, answer=answer)

if __name__ == '__main__':
    app.run(debug=True)
