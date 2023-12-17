import json
import requests

from config import Config

model_name = Config.MODEL
ollama_api_base_url = Config.OLLAMA_API_BASE_URL
print(f"Using model: {model_name}")
print(f"Using Ollama base URL: {ollama_api_base_url}")


def pull_model(model_name_):
    print(f"Pulling model '{model_name_}'...")
    url = f"{ollama_api_base_url}/api/pull"
    data = json.dumps(dict(name=model_name_))
    headers = {'Content-Type': 'application/json'}

    # Use stream=True to handle streaming response
    with requests.post(url, data=data, headers=headers, stream=True) as response:
        if response.status_code == 200:
            # Process the response content in chunks
            for chunk in response.iter_content(chunk_size=1024):
                if chunk:
                    print(chunk.decode('utf-8'), end='')  # Replace 'utf-8' with the appropriate encoding
        else:
            print(f"Error: {response.status_code} - {response.text}")


pull_model(model_name_=model_name)
