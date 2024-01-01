### PDF Bot with Ollama

<img width="15%" src="https://raw.githubusercontent.com/amithkoujalgi/ollama-pdf-bot/main/.demo-stuff/logo.jpeg"/>

A bot that accepts PDF docs and lets you ask questions on it.

The LLMs are downloaded and served via [Ollama](https://github.com/jmorganca/ollama).

![GitHub stars](https://img.shields.io/github/stars/amithkoujalgi/ollama-pdf-bot?style=social)
![GitHub forks](https://img.shields.io/github/forks/amithkoujalgi/ollama-pdf-bot?style=social)
![Hits](https://hits.seeyoufarm.com/api/count/incr/badge.svg?url=https%3A%2F%2Fgithub.com%2Famithkoujalgi%2Follama-pdf-bot&count_bg=%2379C83D&title_bg=%23555555&icon=&icon_color=%23E7E7E7&title=hits&edge_flat=false)

## Table of Contents

- [Requirements](#requirements)
- [How to run](#how-to-run)
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

When the server is up and running, access the app at: http://localhost:8501

Switch to a different model by changing the `MODEL` env variable in the [docker-compose.yaml](https://github.com/amithkoujalgi/ollama-pdf-bot/blob/main/docker-compose.yml#L18). Check out the available models from [here](https://ollama.ai/library).

**Note:**

- It takes a while to start up since it downloads the specified model for the first time.
- If your hardware does not have a GPU and you choose to run only on CPU, expect high response time from the bot.
- Only Nvidia is supported as mentioned in Ollama's documentation. Others such as AMD isn't supported yet. Read how to
  use GPU on [Ollama container](https://hub.docker.com/r/ollama/ollama)
  and [docker-compose](https://docs.docker.com/compose/gpu-support/#:~:text=GPUs%20are%20referenced%20in%20a,capabilities%20.).
- Make sure to have Nvidia drivers setup on your execution environment for the best results.

Image on DockerHub: https://hub.docker.com/r/amithkoujalgi/pdf-bot

### [Demo](https://www.youtube.com/watch?v=jJyFslR-oNQ)

https://github.com/amithkoujalgi/ollama-pdf-bot/assets/1876165/40dc70e6-9d35-4171-9ae6-d82247dbaa17

#### Sample PDFs

[Hl-L2351DW v0522.pdf](https://github.com/amithkoujalgi/ollama-pdf-bot/files/13323209/Hl-L2351DW.v0522.pdf)

[HL-B2080DW v0522.pdf](https://github.com/amithkoujalgi/ollama-pdf-bot/files/13323208/HL-B2080DW.v0522.pdf)


### Improvements

- [ ] Expose model params such as `temperature`, `top_k`, `top_p` as configurable env vars

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

#### Start the app

```shell
streamlit run pdf_bot/app.py
```

### Credits

Thanks to the incredible [Ollama](https://github.com/jmorganca/ollama), [Langchain](https://www.langchain.com/)
and [Streamlit](https://streamlit.io/) projects.

