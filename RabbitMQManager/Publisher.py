#!/usr/bin/env python
import pika
import time
from datetime import datetime
import pickle
import threading
from log import log

class Publisher:
    def __init__(self, name, ip, port, topic):
        self.name = name
        self.ip = ip
        self.port = port
        self.topic = topic

        # create connection to message broker
        self.connection = pika.BlockingConnection(
                        pika.ConnectionParameters(
                            host=self.ip,
                            port=self.port))
        self.channel = self.connection.channel()

        self.channel.exchange_declare(exchange=self.topic, exchange_type='fanout')

    def current_milli_time(self):
        return round(time.time() * 1000)

    def publish(self, message):
        try:
            self.channel.basic_publish(
                                exchange=self.topic,
                                routing_key='',
                                body=message)
        except:
            # connection reset, connect again then send
            self.connection = pika.BlockingConnection(
                        pika.ConnectionParameters(
                            host=self.ip,
                            port=self.port))
            self.channel = self.connection.channel()

            self.channel.exchange_declare(exchange=self.topic, exchange_type='fanout')
            self.channel.basic_publish(
                                exchange=self.topic,
                                routing_key='',
                                body=message)
