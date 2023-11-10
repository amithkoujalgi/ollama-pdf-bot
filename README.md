### PDF Bot with Ollama

A bot that accepts PDF docs and lets you ask questions on it.

The LLMs are downloaded and served via [Ollama](https://github.com/jmorganca/ollama).

## Table of Contents

- [Requirements](#requirements)
- [How to run](#how-to-run)
- [Contributions](#get-involved)

#### Requirements

- Docker (with docker-compose)
- Ollama (Either [natively](https://ollama.ai/download) setup or
  the [Docker image](https://hub.docker.com/r/ollama/ollama))
- Python (for development only)

#### How to run

##### With `docker`

Option 1:

If you're running Ollama server natively, you can directly start the `pdf-bot` docker.

```shell
docker run \
  -p 8501:8501 \
  -e MODEL=orca-mini \
  -e OLLAMA_API_BASE_URL=http://<host-address-of-ollama-server>:<port-of-ollama-server> \
  amithkoujalgi/pdf-bot:1.0.0
```

Option 2:

If you're not running Ollama server natively, and you'd want Ollama server to be run as a Docker container like so:

```shell
docker run \
  -v ~/ollama:/root/.ollama \
  -p 11434:11434 \
  ollama/ollama
```

and then start the `pdf-bot` container (refer to the docker run command above).

##### With `docker-compose` (probably the easiest way to run the app)

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