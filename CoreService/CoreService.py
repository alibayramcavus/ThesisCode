from Manager import Manager
from flask import Flask, json, request
import requests

class CoreService:
    def __init__(self, coreServicePort, coreBrokerIP, coreBrokerPort):
        self.coreServicePort = coreServicePort
        self.coreBrokerIP = coreBrokerIP
        self.coreBrokerPort = coreBrokerPort
        
        self.managers = {}
        self.subscribersForCoreTopics = []

        self.test = 'hehe'

        self.startCoreService()


    def startCoreService(self):
        self.api = Flask(__name__)

        @self.api.route('/registerManager', methods=['POST'])
        def manager():
            ret = {"isSuccess": False}
            try:
                systemName = request.json["systemName"]
                managerIP = request.json["managerIP"]
                managerPort = request.json["managerPort"]
                systemBrokerIP = request.json["systemBrokerIP"]
                systemBrokerPort = request.json["systemBrokerPort"]

                print("Resgiter")
                print("SystemName: " + systemName)

                manager = Manager(systemName, managerIP, managerPort, systemBrokerIP, systemBrokerPort)
                if systemName not in self.managers:
                    # a manager using this system name does not exist, so
                    # it is safe to use this system name
                    self.managers[systemName] = manager
                    ret['isSuccess'] = True
                else:
                    ret["reason"] = "Existing"
            except:
                ret["reason"] = "Missing parameters"

            print (ret)
            return json.dumps(ret)

        @self.api.route('/publishToCoreBroker', methods=['POST'])
        def publishToSystemBroker():
            ret = {"isSuccess": False}
            try:
                print("publishToCoreBroker")
                print(request.json)
                systemName = request.json["systemName"]
                systemBrokerTopic = request.json["systemBrokerTopic"]
                coreBrokerTopic = request.json["coreBrokerTopic"]
                print(systemName, systemBrokerTopic, coreBrokerTopic)
                
                topicPair = (systemBrokerTopic, coreBrokerTopic)
                manager = self.managers[systemName]
                if manager.containTopicPairFromSystemToCore(topicPair) == False:
                    # Topic in system broker is not currently published to core broker with given topic name
                    # it is safe to continue
                    uri = "http://" + manager.managerIP + ":" + str(manager.managerPort) + "/publishToCore"
                    req = {
                        "systemBrokerTopic": systemBrokerTopic,
                        "coreBrokerTopic": coreBrokerTopic
                    }
                    response = requests.post(uri, json=req).json()
                    if response["isSuccess"] == False:
                        ret["reason"] = "Manager could not handle request"
                    else:
                        isAdded = manager.addTopicPairFromSystemToCore(topicPair)
                        if isAdded:
                            ret["isSuccess"] = True
                        else:
                            ret["reason"] = "Topic pair could not added to manager's fromsystemtocore list"
                else:
                    # this topic pair is already mapped, no need to go forward
                    ret["reason"] = "Given topic pair is already existing"
          
            except Exception as e:
                ret["reason"] = "Missing parameters OR Manager with given name not exist"

            return json.dumps(ret)

        @self.api.route('/subscribeToCoreBroker', methods=['POST'])
        def subscribeToCoreBroker():
            ret = {"isSuccess": False}
            try:
                print("subscribeToCoreBroker")
                print(request.json)
                systemName = request.json["systemName"]
                coreBrokerTopic = request.json["coreBrokerTopic"]
                systemBrokerTopic = request.json["systemBrokerTopic"]
                print(systemName, coreBrokerTopic, systemBrokerTopic)
                
                topicPair = (coreBrokerTopic, systemBrokerTopic)
                manager = self.managers[systemName]
                if manager.containTopicPairFromCoreToSystem(topicPair) == False:
                    # Topic in system broker is not currently published to core broker with given topic name
                    # it is safe to continue
                    uri = "http://" + manager.managerIP + ":" + str(manager.managerPort) + "/publishToSystem"
                    req = {
                        "coreBrokerTopic": coreBrokerTopic,
                        "systemBrokerTopic": systemBrokerTopic
                    }
                    response = requests.post(uri, json=req).json()
                    if response["isSuccess"] == False:
                        ret["reason"] = "Manager could not handle request"
                    else:
                        isAdded = manager.addTopicPairFromCoreToSystem(topicPair)
                        if isAdded:
                            ret["isSuccess"] = True
                        else:
                            ret["reason"] = "Topic pair could not added to manager's fromsystemtocore list"
                else:
                    # this topic pair is already mapped, no need to go forward
                    ret["reason"] = "Given topic pair is already existing"
          
            except Exception as e:
                ret["reason"] = "Missing parameters OR Manager with given name not exist"

            return json.dumps(ret)

        @self.api.route('/test', methods=['GET'])
        def getCoreBrokerIP():
            ret = self.test
            self.test = "gegegege"
            return json.dumps(ret)


        self.api.run(host='0.0.0.0', port=self.coreServicePort)