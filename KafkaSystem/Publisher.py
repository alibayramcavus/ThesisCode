#!/usr/bin/env python
from LogHandler import LogHandler
from kafka import KafkaProducer
import time
from datetime import datetime
import pickle
import threading
from log import log

class Publisher:
    def __init__(self, name, ip, port, topic, interval, logEnabled, logOnlyAtTheEnd, logBrokerIP, logBrokerPort):
        self.name = name
        self.ip = ip
        self.port = port
        self.topic = topic
        self.interval = interval / 1000.0
        self.logEnabled =  logEnabled
        self.logOnlyAtTheEnd = logOnlyAtTheEnd
        if self.logEnabled and self.logOnlyAtTheEnd == False:
            self.logBrokerIP = logBrokerIP
            self.logBrokerPort = logBrokerPort
            self.logHandler = LogHandler(self.logBrokerIP, self.logBrokerPort)

        self.producer = KafkaProducer(bootstrap_servers=self.ip + ":" + str(self.port))

        self.isPublishing = False

    def current_milli_time(self):
        return round(time.time() * 1000)

    def __publishContinously(self):
        while(self.isPublishing):
            ptime = self.current_milli_time()
            message = self.name + ":-:" + self.topic + ":-:" + str(ptime)
            self.producer.send(self.topic, message.encode("utf-8"))
            if self.logEnabled and self.logOnlyAtTheEnd == False:
                self.logHandler.publisherLog(message)
            time.sleep(self.interval)

    def startPublishing(self):
        self.isPublishing = True
        thread = threading.Thread(target=self.__publishContinously)
        thread.start()

    def stopPublishing(self):
        self.isPublishing = False