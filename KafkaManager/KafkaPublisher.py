#!/usr/bin/env python
from kafka import KafkaProducer
import time
from datetime import datetime
import pickle
import threading
from log import log

class KafkaPublisher:
    def __init__(self, name, ip, port, topic):
        self.name = name
        self.ip = ip
        self.port = port
        self.topic = topic

        self.producer = KafkaProducer(bootstrap_servers=self.ip + ":" + str(self.port))

    def current_milli_time(self):
        return round(time.time() * 1000)

    def publish(self, message):
        self.producer.send(self.topic, message)