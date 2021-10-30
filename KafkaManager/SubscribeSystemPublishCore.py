#!/usr/bin/env python
from LogHandler import LogHandler
from KafkaSubscriber import KafkaSubscriber
from RabbitMQPublisher import RabbitMQPublisher
import time

class SubscribeSystemPublishCore:
    def __init__(self, systemName, subBrokerIP, subBrokerPort, subBrokerTopic, pubBrokerIP, pubBrokerPort, pubBrokerTopic, logEnabled, logOnlyAtTheEnd, logBrokerIP, logBrokerPort):
        self.systemName = systemName
        self.subBrokerIP = subBrokerIP
        self.subBrokerPort = subBrokerPort
        self.subBrokerTopic = subBrokerTopic
        self.pubBrokerIP = pubBrokerIP
        self.pubBrokerPort = pubBrokerPort
        self.pubBrokerTopic = pubBrokerTopic
        self.logEnabled = logEnabled
        self.logOnlyAtTheEnd = logOnlyAtTheEnd
        if self.logEnabled and self.logOnlyAtTheEnd == False:
            self.logBrokerIP = logBrokerIP
            self.logBrokerPort = logBrokerPort
            self.logHandler = LogHandler(self.logBrokerIP, self.logBrokerPort)

        self.subscriber = KafkaSubscriber('rabbitmqmanager-subscriber', self.subBrokerIP, self.subBrokerPort, self.subBrokerTopic, self.subscriptionCallback) 
        self.publisher = RabbitMQPublisher('rabbitmqmanager-publisher', self.pubBrokerIP, self.pubBrokerPort, self.pubBrokerTopic)

    def current_milli_time(self):
        return round(time.time() * 1000)

    def subscriptionCallback(self, body):
        message = body.decode("utf-8")
        messageWithLog = message
        time = self.current_milli_time()

        if self.logEnabled and self.logOnlyAtTheEnd:
            messageWithLog = message + ":-:" + self.systemName + ":-:" + self.subscriber.topic + ":-:" + self.publisher.topic + ":-:" + str(time)

        self.publisher.publish(messageWithLog)

        if self.logEnabled and self.logOnlyAtTheEnd == False:
            self.logHandler.firstManagerLog(message, self.systemName, self.subscriber.topic, self.publisher.topic, time)