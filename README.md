# PDF_Query_LLM_Project
We will be querying any user input quetion and answer his query using LLM models.

+-----------------------------------------------------------+
|                        Frontend                           |
|                                                           |
|                      PDF Upload                           |
|                      Query Input                          |
|                                                           |
+----------------------------|------------------------------+
                             |
                             v
+-----------------------------------------------------------+
|                      Backend                              |
|                                                           |
|              Text Extraction (PyPDF2)                     |
|                Chunk Creation (CharacterTextSplitter)      |
|                    Embedding (LangChain, OpenAI)           |
|                                                           |
|                      AstraDB                              |
|              Pushing Embeddings (Cassandra)                |
|                                                           |
+----------------------------|------------------------------+
                             |
                             v
+-----------------------------------------------------------+
|                      Query Processing                      |
|                                                           |
|              User Query Interpretation                     |
|             Vector-based Query Retrieval                   |
|                                                           |
+-----------------------------------------------------------+

