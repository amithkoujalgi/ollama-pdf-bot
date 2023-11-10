import os
from pathlib import Path
from typing import Optional

import requests
import streamlit as st

from pdf_helper import PDFHelper


def pull_model(model_name_):
    print(f"pulling model '{model_name_}'...")
    url = f"{ollama_api_base_url}/api/pull"
    data = f'{"name": "{model_name_}"}'
    headers = {'Content-Type': 'application/json'}
    _response = requests.post(url, data=data, headers=headers)
    print(_response.text)


title = "PDF Bot"

model_name = os.environ.get('MODEL', "orca-mini")

ollama_api_base_url = os.environ.get('OLLAMA_API_BASE_URL', "http://localhost:11434")
pdfs_directory = os.path.join(str(Path.home()), 'langchain-store', 'uploads', 'pdfs')
os.makedirs(pdfs_directory, exist_ok=True)

print(f"Using model: {model_name}")
print(f"Using Ollama base URL: {ollama_api_base_url}")
print(f"Using PDFs upload directory: {pdfs_directory}")
pull_model(model_name_=model_name)

st.set_page_config(page_title=title)


def on_upload_change():
    clear_chat_history()


def set_uploaded_file(_uploaded_file: str):
    st.session_state['uploaded_file'] = _uploaded_file


def get_uploaded_file() -> Optional[str]:
    if 'uploaded_file' in st.session_state:
        return st.session_state['uploaded_file']
    return None


with st.sidebar:
    st.title(title)
    st.write('This chatbot accepts a PDF file and lets you ask questions on it.')
    uploaded_file = st.file_uploader(
        label='Upload a PDF', type=['pdf', 'PDF'],
        accept_multiple_files=False,
        key='file-uploader',
        help=None,
        on_change=on_upload_change,
        args=None,
        kwargs=None,
        disabled=False,
        label_visibility="visible"
    )

    if uploaded_file is not None:
        bytes_data = uploaded_file.getvalue()
        target_file = os.path.join(pdfs_directory, uploaded_file.name)
        # print(uploaded_file)
        set_uploaded_file(target_file)
        with open(target_file, 'wb') as f:
            f.write(bytes_data)

# Store LLM generated responses
if "messages" not in st.session_state.keys():
    st.session_state.messages = [{"role": "assistant", "content": "Hello, I'm your PDF assistant."}]

# Display or clear chat messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])


def clear_chat_history():
    st.session_state.messages = [{"role": "assistant", "content": "Hello, I'm your PDF assistant."}]


st.sidebar.button('Reset', on_click=clear_chat_history)

# User-provided prompt
if prompt := st.chat_input(disabled=False, placeholder="What do you want to know from the uploaded PDF?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.write(prompt)

if st.session_state.messages[-1]["role"] != "assistant":
    source_file = get_uploaded_file()
    if source_file is None:
        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                placeholder = st.empty()
                full_response = 'PDF file needs to be uploaded before you can ask questions on it 😟. Please upload a file.'
                placeholder.markdown(full_response)
        message = {"role": "assistant", "content": full_response}
        st.session_state.messages.append(message)
    else:
        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                question = dict(st.session_state.messages[-1]).get('content')
                pdf_helper = PDFHelper(
                    ollama_api_base_url=ollama_api_base_url,
                    model_name=model_name
                )
                response = pdf_helper.ask(
                    pdf_file_path=source_file,
                    question=question
                )
                placeholder = st.empty()
                full_response = ''
                for item in response:
                    full_response += item
                    placeholder.markdown(full_response)
                placeholder.markdown(full_response)
        message = {"role": "assistant", "content": full_response}
        st.session_state.messages.append(message)
