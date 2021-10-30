#!/usr/bin/env python
from Publisher import Publisher
from Subscriber import Subscriber
import os

class ServiceSimulator:
    def __init__(self, name, ip, port, publishersConf, subscribersConf, logEnabled, logOnlyAtTheEnd, logBrokerIP, logBrokerPort):
        self.name = name
        self.ip = ip
        self.port = port
        self.publishers = []
        self.subscribers = []
        self.logEnabled = logEnabled
        self.logOnlyAtTheEnd = logOnlyAtTheEnd
        self.logBrokerIP = logBrokerIP
        self.logBrokerPort = logBrokerPort
        self.__parsePubConf(publishersConf)
        self.__parseSubConf(subscribersConf)

    def __parsePubConf(self, publishersConf):
        try:
            conf = publishersConf.split("***")
            for con in conf:
                if len(con) == 0:
                    continue
                topic_and_interval = con.split("--")
                topic = topic_and_interval[0]
                interval = (int) (topic_and_interval[1])
                if len(topic) == 0:
                    continue
                tempPub = Publisher(self.name, self.ip, self.port, topic, interval, self.logEnabled, self.logOnlyAtTheEnd, self.logBrokerIP, self.logBrokerPort)
                self.publishers.append(tempPub)
        except Exception as e:
            print("PUBLISHERS_CONF is NOT proper")
            print(e)

    def __parseSubConf(self, subscribersConf):
        try:
            conf = subscribersConf.split("***")
            for topic in conf:
                if len(topic) == 0:
                    continue
                tempSub = Subscriber(self.name, self.ip, self.port, topic, self.logEnabled, self.logOnlyAtTheEnd, self.logBrokerIP, self.logBrokerPort)
                self.subscribers.append(tempSub)
        except Exception as e:
            print("SUBSCRIBERS_CONF is NOT proper")
            print(e)

    def startSimulation(self):
        for publisher in self.publishers:
            publisher.startPublishing()
        
        for subscriber in self.subscribers:
            subscriber.startConsuming()

    def stopSimulation(self):
        for publisher in self.publishers:
            publisher.stopPublishing()
        
        for subscriber in self.subscribers:
            subscriber.stopConsuming()

def getName():
    name = "service"
    try:
        name = os.environ["SERVICE_NAME"]
    except:
        print("SERVICE_NAME is NOT set")

    return name

def getIP():
    ip = "localhost"
    try:
        ip = os.environ["RABBITMQ_IP"]
    except:
        print("RABBITMQ_IP is NOT set")

    return ip

def getPort():
    port = 5672
    try:
        port = (int) (os.environ["RABBITMQ_PORT"])
    except:
        print("RABBITMQ_PORT is NOT set")

    return port

def getPublishersConf():
    publishersConf = ""
    try:
        publishersConf = os.environ["PUBLISHERS_CONF"]
    except:
        print("PUBLISHERS_CONF is NOT set")

    return publishersConf

def getSubscribersConf():
    subscribersConf = ""
    try:
        subscribersConf = os.environ["SUBSCRIBERS_CONF"]
    except:
        print("SUBSCRIBERS_CONF is NOT set")

    return subscribersConf

def getLogEnabled():
    logEnabled = False
    try:
        logEnabledStr = os.environ["LOG_ENABLED"]
        logEnabled = logEnabledStr == 'True'
    except:
        print("LOG_ENABLE is NOT set")

    return logEnabled

def getLogOnlyAtTheEnd():
    logOnlyAtTheEnd = False
    try:
        logOnlyAtTheEndStr = os.environ["LOG_ONLY_AT_THE_END"]
        logOnlyAtTheEnd = logOnlyAtTheEndStr == 'True'
    except:
        print("LOG_ONLY_AT_THE_END is NOT set")

    return logOnlyAtTheEnd


def getLogBrokerIP():
    ip = "localhost"
    try:
        ip = os.environ["LOGBROKER_IP"]
    except:
        print("LOGBROKER_IP is NOT set")

    return ip

def getLogBrokerPort():
    port = 5670
    try:
        port = (int) (os.environ["LOGBROKER_PORT"])
    except:
        print("LOGBROKER_PORT is NOT set")

    return port

if __name__ == "__main__":
    name = getName()
    ip = getIP()
    port = getPort()
    publishersConf = getPublishersConf()
    subscribersConf = getSubscribersConf()
    logEnabled = getLogEnabled()
    logOnlyAtTheEnd = getLogOnlyAtTheEnd()
    logBrokerIP = getLogBrokerIP()
    logBrokerPort = getLogBrokerPort()

    try:
        serviceSimulator = ServiceSimulator(name, ip, port, publishersConf, subscribersConf, logEnabled, logOnlyAtTheEnd, logBrokerIP, logBrokerPort)
        serviceSimulator.startSimulation()
    except:
        print("Service could NOT be startted")
        