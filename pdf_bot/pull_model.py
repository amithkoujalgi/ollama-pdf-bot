import json
import os

import requests

model_name = os.environ.get('MODEL', "orca-mini")
ollama_api_base_url = os.environ.get('OLLAMA_API_BASE_URL', "http://localhost:11434")
print(f"Using model: {model_name}")
print(f"Using Ollama base URL: {ollama_api_base_url}")


def pull_model(model_name_):
    print(f"pulling model '{model_name_}'...")
    url = f"{ollama_api_base_url}/api/pull"
    data = json.dumps(dict(name=model_name_))
    print(data)
    headers = {'Content-Type': 'application/json'}
    _response = requests.post(url, data=data, headers=headers)
    print(_response.text)


pull_model(model_name_=model_name)
