#!/usr/bin/env python

from Subscriber import Subscriber
import psycopg2
import json

class LogManager:
    def __init__(self, dbIP, dbPort, dbName, dbPassword, logBrokerIP, logBrokerPort):
        self.dbIP = dbIP
        self.dbPort = dbPort
        self.dbName = dbName
        self.dbPassword = dbPassword
        self.logBrokerIP = logBrokerIP
        self.logBrokerPort = logBrokerPort
        self.topic = "log"

        self.subscriber = Subscriber('logSubscriber', self.logBrokerIP, self.logBrokerPort, self.topic, self.logCallback)

        self.conn = psycopg2.connect(
            host=self.dbIP,
            port=self.dbPort,
            database=self.dbName,
            user="postgres",
            password=self.dbPassword)

        self.cur = self.conn.cursor()

    def logCallback(self, ch, method, properties, body):
        req = json.loads(body.decode("utf-8"))
        type = req["type"]
        if type == "publisherLog":
            log = req["log"]
            self.publisherLog(log["message"])
        elif type == "firstManagerLog":
            log = req["log"]
            self.firstManagerLog(log["message"], log["firstManagerName"], log["firstManagerSubscribedTopic"], log["firstManagerPublishedTopic"], log["firstManagerTime"])
        elif type == "secondManagerLog":
            log = req["log"]
            self.secondManagerLog(log["message"], log["secondManagerName"], log["secondManagerSubscribedTopic"], log["secondManagerPublishedTopic"], log["secondManagerTime"])
        elif type == "subscriberLog":
            log = req["log"]
            self.subscriberLog(log["message"], log["subscriberName"], log["subscribedTopic"], log["subscriberTime"])
        elif type == "all_in_one":
            log = req["log"]
            self.all_in_one_from_actual_subscriber(log["messageWithLog"])


    def publisherLog(self, message):
        publisherName, publishedTopic, publishTime_str = message.split(":-:")
        publishTime = int(publishTime_str)

        sql = """INSERT INTO logstable(message, publishername, publishedtopic, publishtime) 
                VALUES (%s, %s, %s, %s);"""

        try:
            self.cur.execute(sql, (
                message, publisherName, publishedTopic, publishTime
            ))

            self.conn.commit()

        except Exception as e:
            print(e)

    def firstManagerLog(self, message, firstManagerName, firstManagerSubscribedTopic, firstManagerPublishedTopic, firstManagerTime):
        publisherName, publishedTopic, publishTime_str = message.split(":-:")
        publishTime = int(publishTime_str)

        sql = """INSERT INTO logstable(message, publishername, publishedtopic, publishtime, firstmanagername, firstmanagersubscribedtopic, firstmanagerpublishedtopic, firstmanagertime) 
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s);"""

        try:
            self.cur.execute(sql, (
                message, publisherName, publishedTopic, publishTime, firstManagerName, firstManagerSubscribedTopic, firstManagerPublishedTopic, firstManagerTime
            ))

            self.conn.commit()

        except Exception as e:
            print(e)

    def secondManagerLog(self, message, secondManagerName, secondManagerSubscribedTopic, secondManagerPublishedTopic, secondManagerTime):
        publisherName, publishedTopic, publishTime_str = message.split(":-:")
        publishTime = int(publishTime_str)

        sql = """INSERT INTO logstable(message, publishername, publishedtopic, publishtime, secondmanagername, secondmanagersubscribedtopic, secondmanagerpublishedtopic, secondmanagertime) 
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s);"""

        try:
            self.cur.execute(sql, (
                message, publisherName, publishedTopic, publishTime, secondManagerName, secondManagerSubscribedTopic, secondManagerPublishedTopic, secondManagerTime
            ))

            self.conn.commit()

        except Exception as e:
            print(e)


    def subscriberLog(self, message, subscriberName, subscribedTopic, subscriberTime):
        publisherName, publishedTopic, publishTime_str = message.split(":-:")
        publishTime = int(publishTime_str)

        sql = """INSERT INTO logstable(message, publishername, publishedtopic, publishtime, subscribername, subscribedtopic, subscribertime) 
                VALUES (%s, %s, %s, %s, %s, %s, %s);"""

        try:
            self.cur.execute(sql, (
                message, publisherName, publishedTopic, publishTime, subscriberName, subscribedTopic, subscriberTime
            ))

            self.conn.commit()

        except Exception as e:
            print(e)

    def all_in_one_from_actual_subscriber(self, messageWithLog):
        params = messageWithLog.split(":-:")
        if len(params) == 14:
            # subscriber to topic in different system
            publisherName, publishedTopic, publishTimeStr, firstManagerName, firstManagerSubscribedTopic, firstManagerPublishedTopic, firstManagerTimeStr, \
                secondManagerName, secondManagerSubscribedTopic, secondManagerPublishedTopic, secondManagerTimeStr, subscriberName, subscribedTopic, subscriberTimeStr = params
            publishTime = int(publishTimeStr)
            firstManagerTime = int(firstManagerTimeStr)
            secondManagerTime = int(secondManagerTimeStr)
            subscriberTime = int(subscriberTimeStr)
            message = publisherName + ":-:" + publishedTopic + ":-:" + publishTimeStr
            sql = """INSERT INTO logstable VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"""
            try:
                self.cur.execute(sql, (
                    message, publisherName, publishedTopic, publishTime, firstManagerName, firstManagerSubscribedTopic, firstManagerPublishedTopic, firstManagerTime, \
                        secondManagerName, secondManagerSubscribedTopic, secondManagerPublishedTopic, secondManagerTime, subscriberName, subscribedTopic, subscriberTime
                ))

                self.conn.commit()

            except Exception as e:
                print(e)

        elif len(params) == 6:
            # subscriber to topic in same system
            publisherName, publishedTopic, publishTimeStr, subscriberName, subscribedTopic, subscriberTimeStr = params
            publishTime = int(publishTimeStr)
            subscriberTime = int(subscriberTimeStr)
            message = publisherName + ":-:" + publishedTopic + ":-:" + publishTimeStr
            sql = """INSERT INTO logstable(message, publishername, publishedtopic, publishtime,subscribername, subscribedtopic, subscribertime) VALUES (%s, %s, %s, %s, %s, %s, %s)"""
            try:
                self.cur.execute(sql, (
                    message, publisherName, publishedTopic, publishTime, subscriberName, subscribedTopic, subscriberTime
                ))

                self.conn.commit()

            except Exception as e:
                print(e)
                