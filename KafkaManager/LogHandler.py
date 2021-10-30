#!/usr/bin/env python
import pika
import json

class LogHandler:
    def __init__(self, logBrokerIP, logBrokerPort):
        self.logBrokerIP = logBrokerIP
        self.logBrokerPort = logBrokerPort

        self.logConnection = pika.BlockingConnection(
                            pika.ConnectionParameters(
                                host=self.logBrokerIP,
                                port=self.logBrokerPort))
        self.logChannel = self.logConnection.channel()
        self.logChannel.exchange_declare(exchange="log", exchange_type='fanout')

    def firstManagerLog(self, message, systemName, subscribedTopic, publishedTopic, time):
        req = {
            "type": "firstManagerLog",
            "log": {
                "message": message,
                "firstManagerName": systemName,
                "firstManagerSubscribedTopic": subscribedTopic,
                "firstManagerPublishedTopic": publishedTopic,
                "firstManagerTime": time
            }
        }
        self.__publishLog(req)

    def secondManagerLog(self, message, systemName, subscribedTopic, publishedTopic, time):
        req = {
            "type": "secondManagerLog",
            "log": {
                "message": message,
                "secondManagerName": systemName,
                "secondManagerSubscribedTopic": subscribedTopic,
                "secondManagerPublishedTopic": publishedTopic,
                "secondManagerTime": time
            }
        }
        self.__publishLog(req)

    def __publishLog(self, log):
        try:
            self.logChannel.basic_publish(
                                exchange="log",
                                routing_key='',
                                body=json.dumps(log))
        except:
            # connection reset, connect again then send
            self.logConnection = pika.BlockingConnection(
                                pika.ConnectionParameters(
                                    host=self.logBrokerIP,
                                    port=self.logBrokerPort))
            self.logChannel = self.logConnection.channel()
            self.logChannel.exchange_declare(exchange="log", exchange_type='fanout')
            self.logChannel.basic_publish(
                                exchange="log",
                                routing_key='',
                                body=json.dumps(log))
