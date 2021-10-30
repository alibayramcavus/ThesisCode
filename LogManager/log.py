#!/usr/bin/env python

class log:
    def __init__(self, publisherName, publishedTopic, publishTime, messageBody):
        self.publisherName = publisherName
        self.publishedTopic = publishedTopic
        self.publishTime = publishTime
        self.firstManagerName = ""
        self.firstManagerGetTime = -1
        self.firstManagerPublishTime = -1
        self.messageBody = messageBody
        self.secondManagerName = ""
        self.secondManagerGetTime = -1
        self.secondManagerPublishTime = -1
        self.subscriberGetTime = -1
        self.subscriberTopic = ""
        self.subscriberName = ""

    def getAsJson(self):
        return self.__dict__

def loadFromJson(json):
    ret = log("", "", -1, "")
    ret.publisherName = json["publisherName"]
    ret.publishedTopic = json["publishedTopic"]
    ret.publishTime = json["publishTime"]
    ret.firstManagerName = json["firstManagerName"]
    ret.firstManagerGetTime = json["firstManagerGetTime"]
    ret.firstManagerPublishTime = json["firstManagerPublishTime"]
    ret.messageBody = json["messageBody"]
    ret.secondManagerName = json["secondManagerName"]
    ret.secondManagerGetTime = json["secondManagerGetTime"]
    ret.secondManagerPublishTime = json["secondManagerPublishTime"]
    ret.subscriberGetTime = json["subscriberGetTime"]
    ret.subscriberTopic = json["subscriberTopic"]
    ret.subscriberName = json["subscriberName"]

    return ret