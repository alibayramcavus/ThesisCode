#!/usr/bin/env python
from LogManager import LogManager
import os

def getDbIP():
    dbIP = "localhost"
    try:
        dbIP = os.environ["DB_IP"]
    except:
        print("DB_IP is NOT set")

    return dbIP

def getDbPort():
    dbPort = 5432
    try:
        dbPort = (int) (os.environ["DB_PORT"])
    except:
        print("DB_PORT is NOT set")

    return dbPort


def getDbName():
    dbName = "masterdb"
    try:
        dbName = os.environ["DB_NAME"]
    except:
        print("DB_NAME is NOT set")

    return dbName

def getDbPassword():
    dbPassword = "masterdbpassword"
    try:
        dbPassword = os.environ["DB_PASSWORD"]
    except:
        print("DB_PASSWORD is NOT set")

    return dbPassword

def getBrokerIP():
    brokerIP = "localhost"
    try:
        brokerIP = os.environ["BROKER_IP"]
    except:
        print("BROKER_IP is NOT set")

    return brokerIP

def getBrokerPort():
    brokerPort = 5670
    try:
        brokerPort = (int) (os.environ["BROKER_PORT"])
    except:
        print("BROKER_PORT is NOT set")

    return brokerPort

if __name__ == "__main__":
    logManager = LogManager(
        getDbIP(),
        getDbPort(),
        getDbName(),
        getDbPassword(),
        getBrokerIP(), 
        getBrokerPort())
    # logManager = LogManager('localhost', 5670)