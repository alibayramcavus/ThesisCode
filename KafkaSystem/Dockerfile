FROM python:alpine3.14

WORKDIR /app

RUN pip install pika
RUN pip install kafka-python

COPY *.py .

CMD ["python", "ServiceSimulator.py"]