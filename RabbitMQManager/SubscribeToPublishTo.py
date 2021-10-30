#!/usr/bin/env python
from LogHandler import LogHandler
from Publisher import Publisher
from Subscriber import Subscriber
import time

class SubscribeToPublishTo:
    def __init__(self, systemName, subBrokerIP, subBrokerPort, subBrokerTopic, pubBrokerIP, pubBrokerPort, pubBrokerTopic, logEnabled, logOnlyAtTheEnd, logBrokerIP, logBrokerPort, type):
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
        self.type = type
        # type = 0 means system -> core (sub system, publish core)
        # type = 1 means core -> system (sub core, publish system)

        self.subscriber = Subscriber('rabbitmqmanager-subscriber', self.subBrokerIP, self.subBrokerPort, self.subBrokerTopic, self.subscriptionCallback) 
        self.publisher = Publisher('rabbitmqmanager-publisher', self.pubBrokerIP, self.pubBrokerPort, self.pubBrokerTopic)

    def current_milli_time(self):
        return round(time.time() * 1000)

    def subscriptionCallback(self, ch, method, properties, body):
        message = body.decode("utf-8")
        messageWithLog = message
        time = self.current_milli_time()

        if self.logEnabled and self.logOnlyAtTheEnd:
            messageWithLog = message + ":-:" + self.systemName + ":-:" + self.subscriber.topic + ":-:" + self.publisher.topic + ":-:" + str(time)

        self.publisher.publish(messageWithLog)

        if self.logEnabled and self.logOnlyAtTheEnd == False:
            if self.type == 0:
                self.logHandler.firstManagerLog(message, self.systemName, self.subscriber.topic, self.publisher.topic, time)
            elif self.type == 1:
                self.logHandler.secondManagerLog(message, self.systemName, self.subscriber.topic, self.publisher.topic, time)