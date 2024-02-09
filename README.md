# PDF Query LLM Project

This project facilitates querying information from uploaded PDF files using Language Model (LLM) and AstraDB (Cassandra) for efficient text storage and retrieval.

## Architecture Overview

The architecture involves several key steps in the process:

## Setup

### Prerequisites

Before running the application, make sure you have the following:

- AstraDB Application Token (`ASTRA_DB_APPLICATION_TOKEN`) for database access.
- AstraDB ID (`ASTR_DB_ID`) for the specific AstraDB instance.
- OpenAI API Key (`OPENAI_API_KEY`)

### Installation

1. Install required Python libraries:

    ```bash
    pip install openai pinecone langchain PyPDF2 tiktoken cassio
    ```

2. Clone the repository:

    ```bash
    git clone https://github.com/hjskhan/PDF_Query_LLM_Project.git
    cd PDF_Query_LLM_Project
    ```
## Artichectural Overview

### 1. Upload PDF
- Users can upload PDF files via the Streamlit-based user interface.

### 2. Text Extraction
- PyPDF2 library extracts text content from uploaded PDF files, accumulating it into a single string.

### 3. Chunk Creation
- Text chunking using LangChain's `CharacterTextSplitter` for efficient processing.
- Parameters like separator, chunk size, and overlap are used to create manageable text chunks.

### 4. Embedding
- LangChain integrates with OpenAI to generate embeddings (vector representations) of the text chunks.
- OpenAI's language model converts text into compact numerical representations, capturing semantic information.

### 5. AstraDB Push
- Vectorized representations (embeddings) of text chunks are stored in AstraDB (Cassandra) using LangChain's `Cassandra` module.

### 6. Query
- User input queries are processed via Streamlit UI.
- LangChain's `VectorStoreIndexWrapper` queries the Cassandra database for relevant information based on stored vector representations.
- OpenAI's language model helps in interpreting and processing user queries.

## Workflow Diagram

![Workflow Diagram](pdf_query_architecture.png)


## Usage

1. Clone the repository.
2. Install required dependencies: `pip install -r requirements.txt`
3. Set up your environment variables in a `.env` file.
4. Run the application: `streamlit run app.py`

## Contributors

- [Hamza Jamal KHan](https://www.github.com/hjskhan)
