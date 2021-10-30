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

    def publisherLog(self, message):
        req = {
            "type": "publisherLog",
            "log": {
                "message": message
            }
        }
        self.__publishLog(req)

    def subscriberLog(self, message, subscriberName, subscriberTopic, subscriberTime):
        req = {
            "type": "subscriberLog",
            "log": {
                "message": message,
                "subscriberName": subscriberName,
                "subscribedTopic": subscriberTopic,
                "subscriberTime": subscriberTime
            }
        }
        self.__publishLog(req)

    def all_in_one_from_actual_subscriber(self, messageWithLog):
        req = {
            "type": "all_in_one",
            "log": {
                "messageWithLog": messageWithLog
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