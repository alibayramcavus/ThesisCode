#!/usr/bin/env python
from Manager import Manager
import os


def getSystemName():
    systemName = "sys1"
    try:
        systemName = os.environ["SYSTEM_NAME"]
    except:
        print("SYSTEM_NAME is NOT set")

    return systemName

def getManagerIP():
    managerIP = "localhost"
    try:
        managerIP = os.environ["MANAGER_IP"]
    except:
        print("MANAGER_IP is NOT set")

    return managerIP

def getManagerPort():
    managerPort = 8081
    try:
        managerPort = (int) (os.environ["MANAGER_PORT"])
    except:
        print("MANAGER_PORT is NOT set")

    return managerPort

def getSystemBrokerIP():
    systemBrokerIP = "localhost"
    try:
        systemBrokerIP = os.environ["SYSTEM_BROKER_IP"]
    except:
        print("SYSTEM_BROKER_IP is NOT set")

    return systemBrokerIP

def getSystemBrokerPort():
    systemBrokerPort = 5681
    try:
        systemBrokerPort = (int) (os.environ["SYSTEM_BROKER_PORT"])
    except:
        print("SYSTEM_BROKER_PORT is NOT set")

    return systemBrokerPort


def getCoreBrokerIP():
    coreBrokerIP = "localhost"
    try:
        coreBrokerIP = os.environ["CORE_BROKER_IP"]
    except:
        print("CORE_BROKER_IP is NOT set")

    return coreBrokerIP

def getCoreBrokerPort():
    coreBrokerPort = 5680
    try:
        coreBrokerPort = (int) (os.environ["CORE_BROKER_PORT"])
    except:
        print("CORE_BROKER_PORT is NOT set")

    return coreBrokerPort

def getCoreServiceIP():
    coreServiceIP = "localhost"
    try:
        coreServiceIP = os.environ["CORE_SERVICE_IP"]
    except:
        print("CORE_SERVICE_IP is NOT set")

    return coreServiceIP

def getCoreServicePort():
    coreServicePort = 8080
    try:
        coreServicePort = (int) (os.environ["CORE_SERVICE_PORT"])
    except:
        print("CORE_SERVICE_PORT is NOT set")

    return coreServicePort


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

if __name__ == '__main__':
    manager = Manager(
        getSystemName(),
        getManagerIP(),
        getManagerPort(),
        getSystemBrokerIP(),
        getSystemBrokerPort(),
        getCoreBrokerIP(),
        getCoreBrokerPort(),
        getCoreServiceIP(),
        getCoreServicePort(),
        getLogEnabled(),
        getLogOnlyAtTheEnd(),
        getLogBrokerIP(),
        getLogBrokerPort()
    )