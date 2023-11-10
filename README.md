### PDF Bot with Ollama

A bot that accepts PDF docs and lets you ask questions on it.

The LLMs are downloaded and served via [Ollama](https://github.com/jmorganca/ollama).

## Table of Contents

- [Requirements](#requirements)
- [How to run](#how-to-run)
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
      - MODEL="orca-mini"
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

#### Credits

Thanks to the incredible Ollama project.