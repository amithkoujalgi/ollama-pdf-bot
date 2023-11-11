### PDF Bot with Ollama

A bot that accepts PDF docs and lets you ask questions on it.

The LLMs are downloaded and served via [Ollama](https://github.com/jmorganca/ollama).

![GitHub stars](https://img.shields.io/github/stars/amithkoujalgi/ollama-pdf-bot?style=social)
![GitHub forks](https://img.shields.io/github/forks/amithkoujalgi/ollama-pdf-bot?style=social)
![Hits](https://hits.seeyoufarm.com/api/count/incr/badge.svg?url=https%3A%2F%2Fgithub.com%2Famithkoujalgi%2Follama-pdf-bot&count_bg=%2379C83D&title_bg=%23555555&icon=&icon_color=%23E7E7E7&title=hits&edge_flat=false)

## Table of Contents

- [Requirements](#requirements)
- [How to run](#how-to-run)
- [Demo](#demo)
- [Credits](#credits)

#### Requirements

- Docker (with docker-compose)
- Python (for development only)

#### How to run

Define a `docker-compose.yml` and add the following contents into the file.

```yaml
services:

  ollama:
    image: ollama/ollama
    ports:
      - 11434:11434
    volumes:
      - ~/ollama:/root/.ollama
    networks:
      - net

  app:
    image: amithkoujalgi/pdf-bot:1.0.0
    ports:
      - 8501:8501
    environment:
      - OLLAMA_API_BASE_URL=http://ollama:11434
      - MODEL=orca-mini
    networks:
      - net

networks:
  net:
```

Then run:

```shell
docker-compose up
```

When the server is up and running, access the app at: http://localhost:8501

Image on DockerHub: https://hub.docker.com/r/amithkoujalgi/pdf-bot

#### [Demo](https://www.youtube.com/watch?v=jJyFslR-oNQ):

https://github.com/amithkoujalgi/ollama-pdf-bot/assets/1876165/40dc70e6-9d35-4171-9ae6-d82247dbaa17

Sample PDFs:

[Hl-L2351DW v0522.pdf](https://github.com/amithkoujalgi/ollama-pdf-bot/files/13323209/Hl-L2351DW.v0522.pdf)

[HL-B2080DW v0522.pdf](https://github.com/amithkoujalgi/ollama-pdf-bot/files/13323208/HL-B2080DW.v0522.pdf)


#### Credits

Thanks to the incredible [Ollama](https://github.com/jmorganca/ollama) and [Streamlit](https://streamlit.io/) projects.
