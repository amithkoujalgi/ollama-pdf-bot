import os
import textwrap
import time
import uuid
from pathlib import Path
from typing import List

import langchain
from langchain.chains import RetrievalQA
from langchain.chat_models import ChatOllama
from langchain.document_loaders import PyMuPDFLoader
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.vectorstores import FAISS

from config import Config


# This loads the PDF file
def load_pdf_data(file_path):
    # Create a PyMuPDFLoader object with file_path
    loader = PyMuPDFLoader(file_path=file_path)

    # load the PDF file
    docs = loader.load()

    # return the loaded document
    return docs


# Load multiple PDF files
def load_multiple_pdf_data(file_paths: List[str]):
    """Load multiple PDF files and combine their documents"""
    all_docs = []
    
    for file_path in file_paths:
        try:
            docs = load_pdf_data(file_path)
            # Add metadata to identify source file
            for doc in docs:
                doc.metadata['source_file'] = os.path.basename(file_path)
            all_docs.extend(docs)
            print(f"Loaded PDF: {os.path.basename(file_path)} ({len(docs)} pages)")
        except Exception as e:
            print(f"Error loading {file_path}: {str(e)}")
            continue
    
    print(f"Total documents loaded: {len(all_docs)} pages from {len(file_paths)} files")
    return all_docs


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
def load_embedding_model(model_name, normalize_embedding=True):
    print("Loading embedding model...")
    start_time = time.time()
    hugging_face_embeddings = HuggingFaceEmbeddings(
        model_name=model_name,
        model_kwargs={'device': Config.HUGGING_FACE_EMBEDDINGS_DEVICE_TYPE},  # here we will run the model with CPU only
        encode_kwargs={
            'normalize_embeddings': normalize_embedding  # keep True to compute cosine similarity
        }
    )
    end_time = time.time()
    time_taken = round(end_time - start_time, 2)
    print(f"Embedding model load time: {time_taken} seconds.\n")
    return hugging_face_embeddings


# Function for creating embeddings using FAISS
def create_embeddings(chunks, embedding_model, storing_path="vectorstore"):
    print("Creating embeddings...")
    e_start_time = time.time()

    # Create the embeddings using FAISS
    vectorstore = FAISS.from_documents(chunks, embedding_model)

    e_end_time = time.time()
    e_time_taken = round(e_end_time - e_start_time, 2)
    print(f"Embeddings creation time: {e_time_taken} seconds.\n")

    print("Writing vectorstore..")
    v_start_time = time.time()

    # Save the model in a directory
    vectorstore.save_local(storing_path)

    v_end_time = time.time()
    v_time_taken = round(v_end_time - v_start_time, 2)
    print(f"Vectorstore write time: {v_time_taken} seconds.\n")

    # return the vectorstore
    return vectorstore


# Create the chain for Question Answering
def load_qa_chain(retriever, llm, prompt):
    print("Loading QA chain...")
    start_time = time.time()
    qa_chain = RetrievalQA.from_chain_type(
        llm=llm,
        retriever=retriever,  # here we are using the vectorstore as a retriever
        chain_type="stuff",
        return_source_documents=True,  # including source documents in output
        chain_type_kwargs={'prompt': prompt}  # customizing the prompt
    )
    end_time = time.time()
    time_taken = round(end_time - start_time, 2)
    print(f"QA chain load time: {time_taken} seconds.\n")
    return qa_chain


def get_response(query, chain) -> str:
    # Get response from chain
    response = chain({'query': query})
    res = response['result']
    # Wrap the text for better output in Jupyter Notebook
    # wrapped_text = textwrap.fill(res, width=100)
    return res


class PDFHelper:

    def __init__(self, ollama_api_base_url: str, model_name: str = Config.MODEL,
                 embedding_model_name: str = Config.EMBEDDING_MODEL_NAME):
        self._ollama_api_base_url = ollama_api_base_url
        self._model_name = model_name
        self._embedding_model_name = embedding_model_name

    def ask(self, pdf_file_path: str, question: str) -> str:
        """Process a single PDF file and answer questions"""
        vector_store_directory = os.path.join(str(Path.home()), 'langchain-store', 'vectorstore',
                                              'pdf-doc-helper-store', str(uuid.uuid4()))
        os.makedirs(vector_store_directory, exist_ok=True)
        print(f"Using vector store: {vector_store_directory}")

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
        embed = load_embedding_model(model_name=self._embedding_model_name)

        # load and split the documents
        docs = load_pdf_data(file_path=pdf_file_path)
        documents = split_docs(documents=docs)

        # create vectorstore
        vectorstore = create_embeddings(chunks=documents, embedding_model=embed, storing_path=vector_store_directory)

        # convert vectorstore to a retriever
        retriever = vectorstore.as_retriever()

        template = """
        ### System:
        You are an honest assistant.
        You will accept PDF files and you will answer the question asked by the user appropriately.
        If you don't know the answer, just say you don't know. Don't try to make up an answer.
    
        ### Context:
        {context}
    
        ### User:
        {question}
    
        ### Response:
        """

        prompt = langchain.prompts.PromptTemplate.from_template(template)

        # Create the chain
        chain = load_qa_chain(retriever, llm, prompt)

        start_time = time.time()

        response = get_response(question, chain)

        end_time = time.time()

        time_taken = round(end_time - start_time, 2)

        print(f"Response time: {time_taken} seconds.\n")

        return response.strip()

    def ask_multiple(self, pdf_file_paths: List[str], question: str) -> str:
        """Process multiple PDF files and answer questions across all documents"""
        vector_store_directory = os.path.join(str(Path.home()), 'langchain-store', 'vectorstore',
                                              'multi-pdf-doc-helper-store', str(uuid.uuid4()))
        os.makedirs(vector_store_directory, exist_ok=True)
        print(f"Using vector store for multiple files: {vector_store_directory}")

        llm = ChatOllama(
            temperature=0,
            base_url=self._ollama_api_base_url,
            model=self._model_name,
            streaming=True,
            top_k=10,
            top_p=0.3,
            num_ctx=4096,  # Increased context window for multiple documents
            verbose=False
        )

        # Load the Embedding Model
        embed = load_embedding_model(model_name=self._embedding_model_name)

        # Load and combine all PDF documents
        all_docs = load_multiple_pdf_data(pdf_file_paths)
        
        if not all_docs:
            return "I couldn't load any documents. Please check your files and try again."

        # Split the combined documents
        documents = split_docs(documents=all_docs, chunk_size=1000, chunk_overlap=50)

        # Create vectorstore from all documents
        vectorstore = create_embeddings(chunks=documents, embedding_model=embed, storing_path=vector_store_directory)

        # Convert vectorstore to a retriever with higher k for multiple documents
        retriever = vectorstore.as_retriever(search_kwargs={"k": 8})

        # Enhanced template for multiple documents
        template = """
        ### System:
        You are File Whisper, an intelligent document assistant. You have access to multiple PDF documents uploaded by the user.
        
        When answering questions:
        1. Draw information from ALL relevant documents
        2. If information comes from specific documents, mention the source file name
        3. Provide comprehensive answers that synthesize information across documents
        4. If you don't know the answer, just say you don't know. Don't try to make up an answer.
        5. Be helpful and conversational while maintaining accuracy
    
        ### Context from Documents:
        {context}
    
        ### User Question:
        {question}
    
        ### Response:
        """

        prompt = langchain.prompts.PromptTemplate.from_template(template)

        # Create the chain
        chain = load_qa_chain(retriever, llm, prompt)

        start_time = time.time()

        # Get file names for context
        file_names = [os.path.basename(path) for path in pdf_file_paths]
        enhanced_question = f"Question about the {len(file_names)} uploaded documents ({', '.join(file_names)}): {question}"

        response = get_response(enhanced_question, chain)

        end_time = time.time()
        time_taken = round(end_time - start_time, 2)

        print(f"Multi-document response time: {time_taken} seconds.\n")

        return response.strip()
