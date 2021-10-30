FROM python:alpine3.14

WORKDIR /app

RUN pip install pika

COPY *.py .

CMD ["python", "ServiceSimulator.py"]