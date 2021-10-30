FROM python:slim-buster

WORKDIR /app

RUN pip install pika
RUN pip install psycopg2-binary

COPY *.py .

CMD ["python", "main.py"]