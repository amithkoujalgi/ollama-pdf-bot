import os
from pathlib import Path
from typing import Optional, List
import tempfile

import streamlit as st

from config import Config
from pdf_helper import PDFHelper, load_embedding_model

load_embedding_model(model_name=Config.EMBEDDING_MODEL_NAME)

title = "File Whisper"
init_msg = "Hello, I'm File Whisper 📁✨ - your intelligent document assistant. Upload one or more PDF files to get started!"
model_name = Config.MODEL

ollama_api_base_url = Config.OLLAMA_API_BASE_URL
pdfs_directory = os.path.join(str(Path.home()), 'langchain-store', 'uploads', 'pdfs')
os.makedirs(pdfs_directory, exist_ok=True)

print(f"Using model: {model_name}")
print(f"Using Ollama base URL: {ollama_api_base_url}")
print(f"Using PDFs upload directory: {pdfs_directory}")

# Page configuration with File Whisper branding
st.set_page_config(
    page_title=title,
    page_icon="📁",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
.main-header {
    display: flex;
    align-items: center;
    gap: 10px;
    font-size: 2.5rem;
    font-weight: bold;
    color: #1e3a8a;
    margin-bottom: 0.5rem;
}

.file-icon {
    font-size: 2rem;
}

.uploaded-files-container {
    background-color: #f8fafc;
    padding: 1rem;
    border-radius: 0.5rem;
    border: 1px solid #e2e8f0;
    margin: 1rem 0;
}

.file-item {
    display: flex;
    align-items: center;
    gap: 8px;
    padding: 0.5rem 0;
    border-bottom: 1px solid #e2e8f0;
}

.file-item:last-child {
    border-bottom: none;
}

.stButton > button {
    width: 100%;
}
</style>
""", unsafe_allow_html=True)


def on_upload_change():
    """Handle file upload changes"""
    print("Files changed.")
    st.session_state.messages = [{
        "role": "assistant", 
        "content": init_msg
    }]


def set_uploaded_files(uploaded_files: List[str]):
    """Store uploaded file paths in session state"""
    st.session_state['uploaded_files'] = uploaded_files


def get_uploaded_files() -> Optional[List[str]]:
    """Retrieve uploaded file paths from session state"""
    if 'uploaded_files' in st.session_state:
        return st.session_state['uploaded_files']
    return None


def get_file_summary():
    """Generate a summary of uploaded files"""
    uploaded_files = get_uploaded_files()
    if not uploaded_files:
        return "No files uploaded"
    
    if len(uploaded_files) == 1:
        return f"1 file: {os.path.basename(uploaded_files[0])}"
    else:
        return f"{len(uploaded_files)} files uploaded"


# Sidebar with File Whisper branding and file upload
with st.sidebar:
    # Header with icon
    st.markdown(
        '<div class="main-header">'
        '<span class="file-icon">📁</span>'
        f'<span>{title}</span>'
        '</div>', 
        unsafe_allow_html=True
    )
    
    st.markdown("**Your intelligent document assistant**")
    st.write('Upload multiple PDF files and chat with all your documents at once! 🚀')
    
    # Multiple file uploader
    uploaded_files = st.file_uploader(
        label='📂 Upload PDF Files',
        type=['pdf', 'PDF'],
        accept_multiple_files=True,  # Enable multiple file uploads
        key='file-uploader',
        help="You can upload multiple PDF files and chat with all of them together!",
        on_change=on_upload_change,
        disabled=False,
        label_visibility="visible"
    )
    
    # Process uploaded files
    if uploaded_files is not None and len(uploaded_files) > 0:
        file_paths = []
        
        # Display uploaded files info
        st.markdown("### 📚 Uploaded Files:")
        
        for i, uploaded_file in enumerate(uploaded_files, 1):
            target_file = os.path.join(pdfs_directory, uploaded_file.name)
            file_paths.append(target_file)
            
            # Save file to disk
            bytes_data = uploaded_file.getvalue()
            with open(target_file, 'wb') as f:
                f.write(bytes_data)
            
            # Display file info
            st.markdown(f"**{i}.** 📄 `{uploaded_file.name}`")
            st.caption(f"Size: {len(bytes_data) / 1024:.1f} KB")
        
        # Store file paths
        set_uploaded_files(file_paths)
        
        # Add success message to chat
        file_count = len(uploaded_files)
        success_msg = f"Perfect! I've loaded {file_count} document{'s' if file_count > 1 else ''}. What would you like to know from your files? 📖"
        
        # Check if message already exists to avoid duplicates
        added = False
        for msg in st.session_state.messages:
            if "Perfect! I've loaded" in msg["content"]:
                added = True
                break
        
        if not added:
            st.session_state.messages.append({
                "role": "assistant", 
                "content": success_msg
            })
    
    st.markdown("---")
    
    # File summary
    summary = get_file_summary()
    st.markdown(f"**Status:** {summary}")
    
    # Reset button
    st.button('🔄 Reset Chat', on_click=lambda: st.session_state.update({
        'messages': [{"role": "assistant", "content": init_msg}],
        'uploaded_files': None
    }))

# Main chat interface
st.markdown(f"# {title}")

# Initialize chat messages
if "messages" not in st.session_state.keys():
    st.session_state.messages = [{"role": "assistant", "content": init_msg}]

# Display chat messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

# Chat input
if prompt := st.chat_input(
    disabled=False, 
    placeholder="Ask anything about your uploaded documents... 💬"
):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.write(prompt)

# Generate assistant response
if st.session_state.messages[-1]["role"] != "assistant":
    uploaded_files = get_uploaded_files()
    
    if not uploaded_files:
        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                placeholder = st.empty()
                full_response = '📁 Please upload one or more PDF files before asking questions. I\'m ready to help you explore your documents! 😊'
                placeholder.markdown(full_response)
        message = {"role": "assistant", "content": full_response}
        st.session_state.messages.append(message)
    else:
        with st.chat_message("assistant"):
            with st.spinner("🔍 Analyzing your documents..."):
                question = dict(st.session_state.messages[-1]).get('content')
                pdf_helper = PDFHelper(
                    ollama_api_base_url=ollama_api_base_url,
                    model_name=model_name
                )
                
                # Pass all uploaded files to the PDF helper
                response = pdf_helper.ask_multiple(
                    pdf_file_paths=uploaded_files,
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
