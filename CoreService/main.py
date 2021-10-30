#!/usr/bin/env python
from CoreService import CoreService
import os

def getCoreServicePort():
    coreServicePort = 8080
    try:
        coreServicePort = (int) (os.environ["CORE_SERVICE_PORT"])
    except:
        print("CORE_SERVICE_PORT is NOT set")

    return coreServicePort

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


if __name__ == "__main__":
    coreService = CoreService(
        getCoreServicePort(),
        getCoreBrokerIP(),
        getCoreBrokerPort()
    )
    # coreService = CoreService(
    #     8080,
    #     "localhost",
    #     5680
    # )
