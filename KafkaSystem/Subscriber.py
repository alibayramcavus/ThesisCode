#!/usr/bin/env python
from LogHandler import LogHandler
from kafka import KafkaConsumer
import time
from datetime import datetime
import pickle
import threading
from log import log

class Subscriber:
    def __init__(self, name, ip, port, topic, logEnabled, logOnlyAtTheEnd, logBrokerIP, logBrokerPort):
        self.name = name
        self.ip = ip
        self.port = port
        self.topic = topic
        self.logEnabled =  logEnabled
        self.logOnlyAtTheEnd = logOnlyAtTheEnd
        if self.logEnabled:
            self.logBrokerIP = logBrokerIP
            self.logBrokerPort = logBrokerPort
            self.logHandler = LogHandler(self.logBrokerIP, self.logBrokerPort)

        self.consumer = KafkaConsumer(self.topic, bootstrap_servers=ip + ":" + str(port))

        self.isConsuming = False

    def __mycallback(self, body):
        message = body.decode("utf-8")
        time = self.current_milli_time()
        if self.logEnabled:
            if self.logOnlyAtTheEnd == False:
                self.logHandler.subscriberLog(message, self.name, self.topic, time)
            else:
                messageWithLog = message + ":-:" + self.name + ":-:" + self.topic + ":-:" + str(time)
                self.logHandler.all_in_one_from_actual_subscriber(messageWithLog)
        
        print(message)

    def current_milli_time(self):
        return round(time.time() * 1000)

    def __consumeContinously(self):
        for msg in self.consumer:
            if self.isConsuming == False:
                break
            self.__mycallback(msg.value)

    def startConsuming(self):
        self.isConsuming = True
        thread = threading.Thread(target=self.__consumeContinously)
        thread.start()

    def stopConsuming(self):
        self.isConsuming = False
        self.consumer = KafkaConsumer(self.topic, bootstrap_servers=self.ip + ":" + str(self.port))