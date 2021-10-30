FROM python:alpine3.14

WORKDIR /app

RUN pip install pika
RUN pip install kafka-python
RUN pip install flask
RUN pip install requests

COPY *.py .

CMD ["python", "main.py"]