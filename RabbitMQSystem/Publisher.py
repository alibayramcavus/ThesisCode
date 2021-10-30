#!/usr/bin/env python
from logging import log
from LogHandler import LogHandler
import pika
import time
import threading

class Publisher:
    def __init__(self, name, ip, port, topic, interval, logEnabled, logOnlyAtTheEnd, logBrokerIP, logBrokerPort):
        self.name = name
        self.ip = ip
        self.port = port
        self.topic = topic
        self.interval = interval / 1000.0
        self.logEnabled = logEnabled
        self.logOnlyAtTheEnd = logOnlyAtTheEnd
        if self.logEnabled and self.logOnlyAtTheEnd == False:
            self.logBrokerIP = logBrokerIP
            self.logBrokerPort = logBrokerPort
            self.logHandler = LogHandler(self.logBrokerIP, self.logBrokerPort)

        # create connection to message broker
        self.connection = pika.BlockingConnection(
                        pika.ConnectionParameters(
                            host=self.ip,
                            port=self.port))
        self.channel = self.connection.channel()

        self.channel.exchange_declare(exchange=self.topic, exchange_type='fanout')

        self.isPublishing = False

    def current_milli_time(self):
        return round(time.time() * 1000)

    def __publishMessage(self, message):
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

    def __publishContinously(self):
        while(self.isPublishing):
            ptime = self.current_milli_time()
            message = self.name + ":-:" + self.topic + ":-:" + str(ptime)
            self.__publishMessage(message)
            
            if self.logEnabled and self.logOnlyAtTheEnd == False:
                self.logHandler.publisherLog(message)

            time.sleep(self.interval)

    def startPublishing(self):
        self.isPublishing = True
        thread = threading.Thread(target=self.__publishContinously)
        thread.start()

    def stopPublishing(self):
        self.isPublishing = False
