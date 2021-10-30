#!/usr/bin/env python
from SubscribeToPublishTo import SubscribeToPublishTo
from flask import Flask, json, request
import requests

class Manager:
    def __init__(self, systemName, managerIP, managerPort, systemBrokerIP, systemBrokerPort, coreBrokerIP, coreBrokerPort, coreServiceIP, coreServicePort, logEnabled, logOnlyAtTheEnd, logBrokerIP, logBrokerPort):
        
        if (systemBrokerIP == coreBrokerIP and systemBrokerPort == coreBrokerPort):
            raise Exception('MANAGER CANNOT USE SAME BROKER AS BOTH SYSTEM BROKER AND CORE BROKER')
        
        self.systemName = systemName
        self.managerIP = managerIP
        self.managerPort = managerPort
        self.systemBrokerIP = systemBrokerIP
        self.systemBrokerPort = systemBrokerPort
        self.coreBrokerIP = coreBrokerIP
        self.coreBrokerPort = coreBrokerPort
        self.coreServiceIP = coreServiceIP
        self.coreServicePort = coreServicePort
        self.logEnabled = logEnabled
        self.logOnlyAtTheEnd = logOnlyAtTheEnd
        self.logBrokerIP = logBrokerIP
        self.logBrokerPort = logBrokerPort

        self.fromSystemToCore = []
        self.fromCoreToSystem = []

        self.registerToCore()

    def registerToCore(self):
        uri = "http://" + self.coreServiceIP + ":" + str(self.coreServicePort) + "/registerManager"
        req = {
            "systemName": self.systemName,
            "managerIP": self.managerIP,
            "managerPort": self.managerPort,
            "systemBrokerIP": self.systemBrokerIP,
            "systemBrokerPort": self.systemBrokerPort
        }
        response = requests.post(uri, json=req).json()
        if response["isSuccess"] == False:
            raise Exception('COULD NOT REGISTER TO CORE SERVICE. REASON: ' + response["reason"])
        else:
            self.startManagerService()

    def subToSystemPublishToCore(self, systemTopic, coreTopic):
        systemSub = SubscribeToPublishTo(
                        self.systemName, self.systemBrokerIP, self.systemBrokerPort, systemTopic,
                        self.coreBrokerIP, self.coreBrokerPort, coreTopic, self.logEnabled, self.logOnlyAtTheEnd, self.logBrokerIP, self.logBrokerPort, 0)

        self.fromSystemToCore.append(systemSub)

    def subToCorePublishToSystem(self, coreTopic, systemTopic):
        coreSub = SubscribeToPublishTo(
                        self.systemName, self.coreBrokerIP, self.coreBrokerPort, coreTopic,
                        self.systemBrokerIP, self.systemBrokerPort, systemTopic, self.logEnabled, self.logOnlyAtTheEnd, self.logBrokerIP, self.logBrokerPort, 1)

        self.fromCoreToSystem.append(coreSub)

    
    def startManagerService(self):
        print("start srevice")
        self.api = Flask(__name__)

        @self.api.route('/publishToCore', methods=['POST'])
        def publishToCore():
            ret = {"isSuccess": False}
            try:
                systemBrokerTopic = request.json["systemBrokerTopic"]
                coreBrokerTopic = request.json["coreBrokerTopic"]
                self.subToSystemPublishToCore(systemBrokerTopic, coreBrokerTopic)
                ret["isSuccess"] = True
            except:
                ret["reason"] = "Missing parameters"
            return json.dumps(ret)

        @self.api.route('/publishToSystem', methods=['POST'])
        def publishToSystem():
            ret = {"isSuccess": False}
            try:
                coreBrokerTopic = request.json["coreBrokerTopic"]
                systemBrokerTopic = request.json["systemBrokerTopic"]
                self.subToCorePublishToSystem(coreBrokerTopic, systemBrokerTopic)
                ret["isSuccess"] = True
            except:
                ret["reason"] = "Missing parameters"
            return json.dumps(ret)


        self.api.run(host='0.0.0.0', port=self.managerPort)