#!/usr/bin/env python

class Manager:
    def __init__(self, systemName, managerIP, managerPort, systemBrokerIP, systemBrokerPort):
        self.systemName = systemName
        self.managerIP = managerIP
        self.managerPort = managerPort
        self.systemBrokerIP = systemBrokerIP
        self.systemBrokerPort = systemBrokerPort

        self.fromSystemToCoreTopicPairs = []
        self.fromCoreToSystemTopicPairs = []

    def containTopicPairFromSystemToCore(self, topicPair):
        ret = False
        if (topicPair in self.fromSystemToCoreTopicPairs):
            ret = True
        return ret

    def containTopicPairFromCoreToSystem(self, topicPair):
        ret = False
        if (topicPair in self.fromCoreToSystemTopicPairs):
            ret = True
        return ret

    def addTopicPairFromSystemToCore(self, topicPair):
        ret = False
        if self.containTopicPairFromSystemToCore(topicPair) == False:
            self.fromSystemToCoreTopicPairs.append(topicPair)
            ret = True
        return ret

    def addTopicPairFromCoreToSystem(self, topicPair):
        ret = False
        if self.containTopicPairFromCoreToSystem(topicPair) == False:
            self.fromCoreToSystemTopicPairs.append(topicPair)
            ret = True
        return ret