import os


class Config:
    MODEL = os.environ.get('MODEL', "llama2")
    EMBEDDING_MODEL_NAME = os.environ.get('EMBEDDING_MODEL_NAME', "all-MiniLM-L6-v2")
    OLLAMA_API_BASE_URL = os.environ.get('OLLAMA_API_BASE_URL', "http://localhost:11434")
    HUGGING_FACE_EMBEDDINGS_DEVICE_TYPE = os.environ.get('HUGGING_FACE_EMBEDDINGS_DEVICE_TYPE',
                                                         "cpu")
