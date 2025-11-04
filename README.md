### File Whisper - Your Intelligent Document Assistant 📁✨

<p align="center">
  <img width="15%" src="https://raw.githubusercontent.com/cli-github-dev/ollama-pdf-bot/feature/file-whisper-ui-updates/assets/file-whisper-logo.svg"/>
</p>

**File Whisper** is an intelligent document assistant that lets you upload multiple PDF files and have natural conversations with your documents. Powered by Ollama for local AI processing, it provides privacy-focused document analysis and question answering.

The LLMs are downloaded and served via [Ollama](https://github.com/jmorganca/ollama).

<p align="center">
  <img src="https://img.shields.io/docker/pulls/amithkoujalgi/pdf-bot?style=for-the-badge&link=https%3A%2F%2Fhub.docker.com%2Fr%2Famithkoujalgi%2Fpdf-bot"/>
</p>

<p align="center">
  <img src="https://img.shields.io/github/stars/amithkoujalgi/ollama-pdf-bot?style=social"/>
    <img src="https://img.shields.io/github/forks/amithkoujalgi/ollama-pdf-bot?style=social"/>
  <img src="https://hits.seeyoufarm.com/api/count/incr/badge.svg?url=https%3A%2F%2Fgithub.com%2Famithkoujalgi%2Follama-pdf-bot&count_bg=%2379C83D&title_bg=%23555555&icon=&icon_color=%23E7E7E7&title=hits&edge_flat=false"/>
</p>

## ✨ What's New in File Whisper

- 🔄 **Multi-File Support**: Upload and chat with multiple PDF documents simultaneously
- 🎨 **Enhanced UI**: Beautiful new interface with File Whisper branding
- 📁 **Smart Document Management**: View uploaded files with file info and status
- 🤖 **Cross-Document Intelligence**: Ask questions that span across all your uploaded documents
- 💬 **Natural Conversations**: Chat naturally with your document collection

## Table of Contents

- [Requirements](#requirements)
- [How to run](#how-to-run)
- [New Features](#new-features)
- [Demo](#demo)
- [Improvements](#improvements)
- [Contributing](#contributing)
- [Credits](#credits)

### Requirements

[![][shield]][site]

[![][maketool-shield]][maketool-site]

[site]: https://docs.docker.com/compose/

[shield]: https://img.shields.io/badge/Docker_Compose-Installation-blue.svg?style=for-the-badge&labelColor=gray

[maketool-site]: https://www.gnu.org/software/make/

[maketool-shield]: https://img.shields.io/badge/Make-Tool-blue.svg?style=for-the-badge&labelColor=gray

### How to run

#### CPU version

```shell
make start
```

#### GPU version

```shell
make start-gpu
```

When the server is up and running, access **File Whisper** at: http://localhost:8501

Switch to a different model by changing the `MODEL` env variable in the [docker-compose.yaml](https://github.com/amithkoujalgi/ollama-pdf-bot/blob/main/docker-compose.yml#L18). Check out the available models from [here](https://ollama.ai/library).

**Note:**

- It takes a while to start up since it downloads the specified model for the first time.
- If your hardware does not have a GPU and you choose to run only on CPU, expect high response time from the bot.
- Only Nvidia is supported as mentioned in Ollama's documentation. Others such as AMD isn't supported yet. Read how to
  use GPU on [Ollama container](https://hub.docker.com/r/ollama/ollama)
  and [docker-compose](https://docs.docker.com/compose/gpu-support/#:~:text=GPUs%20are%20referenced%20in%20a,capabilities%20.).
- Make sure to have Nvidia drivers setup on your execution environment for the best results.

Image on DockerHub: https://hub.docker.com/r/amithkoujalgi/pdf-bot

### New Features 🚀

#### Multi-Document Intelligence
- **Upload Multiple PDFs**: Drag and drop or select multiple PDF files at once
- **Cross-Document Queries**: Ask questions that require information from multiple documents
- **Source Attribution**: File Whisper identifies which documents contain relevant information
- **Unified Knowledge Base**: All documents are processed together for comprehensive answers

#### Enhanced User Experience
- **File Management**: See all uploaded files with size information and status
- **Smart UI**: Clean, intuitive interface with File Whisper branding
- **Progress Indicators**: Visual feedback during document processing
- **Chat Reset**: Easy reset functionality to start fresh conversations

#### Example Use Cases
- **Research**: Upload multiple research papers and ask comparative questions
- **Documentation**: Load various manuals and find specific procedures
- **Analysis**: Compare information across multiple reports
- **Learning**: Upload course materials and ask comprehensive questions

### [Demo](https://www.youtube.com/watch?v=jJyFslR-oNQ)

*Original demo - new multi-file features coming soon!*

https://github.com/amithkoujalgi/ollama-pdf-bot/assets/1876165/40dc70e6-9d35-4171-9ae6-d82247dbaa17

#### Sample PDFs

[Hl-L2351DW v0522.pdf](https://github.com/amithkoujalgi/ollama-pdf-bot/files/13323209/Hl-L2351DW.v0522.pdf)

[HL-B2080DW v0522.pdf](https://github.com/amithkoujalgi/ollama-pdf-bot/files/13323208/HL-B2080DW.v0522.pdf)

### Improvements

- [x] **Multi-file upload support** - Upload and chat with multiple PDFs simultaneously
- [x] **Enhanced UI with File Whisper branding** - Beautiful new interface design
- [x] **Cross-document intelligence** - Ask questions across multiple documents
- [x] **File management interface** - View and manage uploaded documents
- [ ] Expose model params such as `temperature`, `top_k`, `top_p` as configurable env vars
- [ ] Support for additional file formats (DOCX, TXT, etc.)
- [ ] Document similarity analysis and clustering
- [ ] Export conversation history

### Contributing

Contributions are most welcome! Whether it's reporting a bug, proposing an enhancement, or helping
with code - any sort of contribution is much appreciated.

#### Requirements

![Python](https://img.shields.io/badge/python-3.8_+-green.svg)

#### Setup Ollama server for development

```shell
docker run -it -v ~/ollama:/root/.ollama -p 11434:11434 ollama/ollama
```

#### Install the libs

```shell
pip install -r requirements.txt
```

#### Start File Whisper

```shell
streamlit run pdf_bot/app.py
```

### Credits

Thanks to the incredible [Ollama](https://github.com/jmorganca/ollama), [Langchain](https://www.langchain.com/)
and [Streamlit](https://streamlit.io/) projects.

### Appreciate my work?

<p align="center">
  <a href="https://www.buymeacoffee.com/amithkoujalgi" target="_blank"><img src="https://cdn.buymeacoffee.com/buttons/v2/default-yellow.png" alt="Buy Me A Coffee" style="height: 60px !important;width: 217px !important;" ></a>
</p>

---

**File Whisper** - *Where documents meet intelligence* 📁✨
