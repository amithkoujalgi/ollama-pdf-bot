import os

base_url = os.environ.get('OLLAMA_API_BASE_URL', "http://192.168.29.223:11434")
if base_url.endswith('/'):
    base_url = base_url.rstrip('/')


class Config:
    MODEL = os.environ.get('MODEL', "llama2")
    EMBEDDING_MODEL_NAME = os.environ.get('EMBEDDING_MODEL_NAME', "all-MiniLM-L6-v2")
    OLLAMA_API_BASE_URL = base_url
    HUGGING_FACE_EMBEDDINGS_DEVICE_TYPE = os.environ.get('HUGGING_FACE_EMBEDDINGS_DEVICE_TYPE',
                                                         "cpu")
