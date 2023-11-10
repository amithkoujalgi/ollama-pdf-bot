FROM python:3.8.18

WORKDIR /app

COPY ./requirements.txt /app/requirements.txt
RUN pip install -r /app/requirements.txt

COPY ./pdf_bot /app/pdf_bot

CMD ["bash", "/app/pdf_bot/run.sh"]