### Thesis Code ###

We have tried to make an interoperability tool among different message brokers such as RabbitMQ, Kafka, etc.

## How to use ##
First start all of the message brokers:
  * cd RabbitMQManager
  * docker-compose up
  
Then start first system:
  * cd RabbitMQSystem
  * docker-compose up

Then start second system:  
  * cd RabbitMQManager
  * docker-compose up
  
Then start log system
  * cd LogManager
  * docker-compose up
  
Then start the interoperability part:
  * cd CoreService
  * docker-compose up
