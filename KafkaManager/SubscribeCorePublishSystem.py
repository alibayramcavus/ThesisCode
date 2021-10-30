#!/usr/bin/env python
from LogHandler import LogHandler
from KafkaPublisher import KafkaPublisher
from RabbitMQSubscriber import RabbitMQSubscriber
import time

class SubscribeCorePublishSystem:
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

        self.subscriber = RabbitMQSubscriber('rabbitmqmanager-subscriber', self.subBrokerIP, self.subBrokerPort, self.subBrokerTopic, self.subscriptionCallback) 
        self.publisher = KafkaPublisher('rabbitmqmanager-publisher', self.pubBrokerIP, self.pubBrokerPort, self.pubBrokerTopic)

    def current_milli_time(self):
        return round(time.time() * 1000)

    def subscriptionCallback(self, ch, method, properties, body):
        message = body.decode("utf-8")
        messageWithLog = message
        time = self.current_milli_time()

        if self.logEnabled and self.logOnlyAtTheEnd:
            messageWithLog = message + ":-:" + self.systemName + ":-:" + self.subscriber.topic + ":-:" + self.publisher.topic + ":-:" + str(time)

        # Kafka publisher gets byte array, not string
        self.publisher.publish(messageWithLog.encode("utf-8"))

        if self.logEnabled and self.logOnlyAtTheEnd == False:
            self.logHandler.secondManagerLog(message, self.systemName, self.subscriber.topic, self.publisher.topic, time)