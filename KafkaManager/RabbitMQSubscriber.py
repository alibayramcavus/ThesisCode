#!/usr/bin/env python
import pika
import time
from datetime import datetime
import pickle
import threading
from log import log

class RabbitMQSubscriber:
    def __init__(self, name, ip, port, topic, myCallback):
        self.name = name
        self.ip = ip
        self.port = port
        self.topic = topic
        self.myCallback = myCallback

        # create connection to message broker
        self.connection = pika.BlockingConnection(
                        pika.ConnectionParameters(
                            host=self.ip,
                            port=self.port))
        self.channel = self.connection.channel()
        self.startConsuming()

    def __callback(self, ch, method, properties, body):
        sLog = pickle.loads(body)
        sLog.subscriberName = self.name
        sLog.subscribedTopic = self.topic
        sLog.arriveMs = self.current_milli_time()
        print(str(sLog.__dict__))

    def current_milli_time(self):
        return round(time.time() * 1000)

    def __consumeContinously(self):
        self.channel.exchange_declare(exchange=self.topic, exchange_type='fanout')

        self.result = self.channel.queue_declare(queue='', exclusive=True)
        self.queue_name = self.result.method.queue
        self.channel.queue_bind(exchange=self.topic, queue=self.queue_name)

        self.channel.basic_consume(queue=self.queue_name, 
                        on_message_callback=self.myCallback, 
                        auto_ack=True)

        self.channel.start_consuming()

    def startConsuming(self):
        thread = threading.Thread(target=self.__consumeContinously)
        thread.start()

    def stopConsuming(self):
        self.channel.stop_consuming()