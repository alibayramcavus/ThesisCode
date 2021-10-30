#!/usr/bin/env python
from kafka import KafkaConsumer
import time
from datetime import datetime
import pickle
import threading
from log import log

class KafkaSubscriber:
    def __init__(self, name, ip, port, topic, mycallback):
        self.name = name
        self.ip = ip
        self.port = port
        self.topic = topic
        self.mycallback = mycallback

        self.consumer = KafkaConsumer(self.topic, bootstrap_servers=ip + ":" + str(port))

        self.isConsuming = False
        self.startConsuming()

    def current_milli_time(self):
        return round(time.time() * 1000)

    def __consumeContinously(self):
        for msg in self.consumer:
            if self.isConsuming == False:
                break
            self.mycallback(msg.value)

    def startConsuming(self):
        self.isConsuming = True
        thread = threading.Thread(target=self.__consumeContinously)
        thread.start()

    def stopConsuming(self):
        self.isConsuming = False
        self.consumer = KafkaConsumer(self.topic, bootstrap_servers=self.ip + ":" + str(self.port))