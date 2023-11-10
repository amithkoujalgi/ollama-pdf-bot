#!/bin/bash
# used for running from within the docker container. Not recommended for running this in dev mode.
python /app/pdf_bot/pull_model.py
streamlit run /app/pdf_bot/app.py