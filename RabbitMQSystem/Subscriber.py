#!/usr/bin/env python
from LogHandler import LogHandler
import pika
import time
import threading

class Subscriber:
    def __init__(self, name, ip, port, topic, logEnabled, logOnlyAtTheEnd, logBrokerIP, logBrokerPort):
        self.name = name
        self.ip = ip
        self.port = port
        self.topic = topic
        self.logEnabled = logEnabled
        self.logOnlyAtTheEnd = logOnlyAtTheEnd
        if self.logEnabled:
            self.logBrokerIP = logBrokerIP
            self.logBrokerPort = logBrokerPort
            self.logHandler = LogHandler(self.logBrokerIP, self.logBrokerPort)

        # create connection to message broker
        self.connection = pika.BlockingConnection(
                        pika.ConnectionParameters(
                            host=self.ip,
                            port=self.port))
        self.channel = self.connection.channel()

    def __callback(self, ch, method, properties, body):
        message = body.decode("utf-8")
        time = self.current_milli_time()
        if self.logEnabled:
            if self.logOnlyAtTheEnd == False:
                self.logHandler.subscriberLog(message, self.name, self.topic, time)
            else:
                messageWithLog = message + ":-:" + self.name + ":-:" + self.topic + ":-:" + str(time)
                self.logHandler.all_in_one_from_actual_subscriber(messageWithLog)
        print(message)

    def current_milli_time(self):
        return round(time.time() * 1000)

    def __consumeContinously(self):
        self.channel.exchange_declare(exchange=self.topic, exchange_type='fanout')

        self.result = self.channel.queue_declare(queue='', exclusive=True)
        self.queue_name = self.result.method.queue
        self.channel.queue_bind(exchange=self.topic, queue=self.queue_name)

        self.channel.basic_consume(queue=self.queue_name, 
                        on_message_callback=self.__callback, 
                        auto_ack=True)

        self.channel.start_consuming()

    def startConsuming(self):
        thread = threading.Thread(target=self.__consumeContinously)
        thread.start()

    def stopConsuming(self):
        self.channel.stop_consuming()