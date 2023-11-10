import os
import textwrap
import time
import uuid
from pathlib import Path

import langchain
from langchain.chains import RetrievalQA
from langchain.chat_models import ChatOllama
from langchain.document_loaders import PyMuPDFLoader
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.vectorstores import FAISS


# This loads the PDF file
def load_pdf_data(file_path):
    # Create a PyMuPDFLoader object with file_path
    loader = PyMuPDFLoader(file_path=file_path)

    # load the PDF file
    docs = loader.load()

    # return the loaded document
    return docs


# Responsible for splitting the documents into several chunks
def split_docs(documents, chunk_size=1000, chunk_overlap=20):
    # Initialize the RecursiveCharacterTextSplitter with
    # chunk_size and chunk_overlap
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap
    )

    # Split the documents into chunks
    chunks = text_splitter.split_documents(documents=documents)

    # return the document chunks
    return chunks


# function for loading the embedding model
def load_embedding_model(model_path, normalize_embedding=True):
    return HuggingFaceEmbeddings(
        model_name=model_path,
        model_kwargs={'device': 'cpu'},  # here we will run the model with CPU only
        encode_kwargs={
            'normalize_embeddings': normalize_embedding  # keep True to compute cosine similarity
        }
    )


# Function for creating embeddings using FAISS
def create_embeddings(chunks, embedding_model, storing_path="vectorstore"):
    # Create the embeddings using FAISS
    vectorstore = FAISS.from_documents(chunks, embedding_model)

    # Save the model in a directory
    vectorstore.save_local(storing_path)

    # return the vectorstore
    return vectorstore


# Create the chain for Question Answering
def load_qa_chain(retriever, llm, prompt):
    return RetrievalQA.from_chain_type(
        llm=llm,
        retriever=retriever,  # here we are using the vectorstore as a retriever
        chain_type="stuff",
        return_source_documents=True,  # including source documents in output
        chain_type_kwargs={'prompt': prompt}  # customizing the prompt
    )


def get_response(query, chain) -> str:
    # Get response from chain
    response = chain({'query': query})

    # Wrap the text for better output in Jupyter Notebook
    wrapped_text = textwrap.fill(response['result'], width=100)
    return wrapped_text


class PDFHelper:

    def __init__(self, ollama_api_base_url: str, model_name: str = "orca-mini",
                 embedding_model_path: str = "all-MiniLM-L6-v2"):
        self._ollama_api_base_url = ollama_api_base_url
        self._model_name = model_name
        self._embedding_model_path = embedding_model_path

    def ask(self, pdf_file_path: str, question: str) -> str:
        vector_store_directory = os.path.join(str(Path.home()), 'langchain-store', 'vectorstore',
                                              'pdf-doc-helper-store', str(uuid.uuid4()))
        os.makedirs(vector_store_directory, exist_ok=True)
        print(f"Using vector store: {vector_store_directory}")

        start_time = time.time()

        llm = ChatOllama(
            temperature=0,
            base_url=self._ollama_api_base_url,
            model=self._model_name,
            streaming=True,
            # seed=2,
            top_k=10,
            # A higher value (100) will give more diverse answers, while a lower value (10) will be more conservative.
            top_p=0.3,
            # Higher value (0.95) will lead to more diverse text, while a lower value (0.5) will generate more
            # focused text.
            num_ctx=3072,  # Sets the size of the context window used to generate the next token.
            verbose=False
        )

        # Load the Embedding Model
        embed = load_embedding_model(model_path=self._embedding_model_path)

        # load and split the documents
        docs = load_pdf_data(file_path=pdf_file_path)
        documents = split_docs(documents=docs)

        # create vectorstore
        vectorstore = create_embeddings(chunks=documents, embedding_model=embed, storing_path=vector_store_directory)

        # convert vectorstore to a retriever
        retriever = vectorstore.as_retriever()

        template = """
        ### System:
        You are an respectful and honest assistant. You have to answer the user's questions using only the context \
        provided to you. If you don't know the answer, just say you don't know. Don't try to make up an answer.
    
        ### Context:
        {context}
    
        ### User:
        {question}
    
        ### Response:
        """

        prompt = langchain.prompts.PromptTemplate.from_template(template)

        # Create the chain
        chain = load_qa_chain(retriever, llm, prompt)

        response = get_response(question, chain)
        end_time = time.time()

        print(f"Response time: {end_time - start_time} seconds.\n")
        return response.strip()
