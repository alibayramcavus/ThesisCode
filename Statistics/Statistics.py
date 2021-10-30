#!/usr/bin/env python

import psycopg2
import sys
import matplotlib.pyplot as plt

class Statistics:
    def __init__(self, dbIP, dbPort, dbName, dbPassword):
        self.dbIP = dbIP
        self.dbPort = dbPort
        self.dbName = dbName
        self.dbPassword = dbPassword

        self.conn = psycopg2.connect(
            host=self.dbIP,
            port=self.dbPort,
            database=self.dbName,
            user="postgres",
            password=self.dbPassword)

        self.cur = self.conn.cursor()

    def getLogFromSameSystemForSys1(self):
        sql = """SELECT * FROM logstable WHERE firstmanagername is NULL and publishername ilike '%\sys1%' order by publishtime asc;"""
        firstPublishTime = sys.maxsize
        try:
            output_PublishTime = []
            output_TimePassed = []
            totalTimePassed = 0
            self.cur.execute(sql)

            rows = self.cur.fetchall()
            firstPublishTime = rows[0][3]
            for row in rows:
                publishTime = row[3] - firstPublishTime
                timePassed = row[14] - row[3]
                output_PublishTime.append(publishTime)
                output_TimePassed.append(timePassed)
                totalTimePassed += timePassed

            print("A")
            print("Sys1 Pub - Sys1 Sub")
            print("Number of samples: " + str(len(rows)))
            print("Average time between Publisher(Sys1) - Subscriber(Sys1): " + str(totalTimePassed / len(rows)))
            print("--------------------------------------------------------------------")

            plt.plot(output_PublishTime, output_TimePassed)
            plt.title('From Pub(Sys1) - To Sub(Sys1)')
            plt.xlabel('Publishedtime')
            plt.ylabel('Time Passed')
            plt.show()
            
        except Exception as e:
            print(e)

    def getLogFromSameSystemForSys2(self):
        sql = """SELECT * FROM logstable WHERE firstmanagername is NULL and publishername ilike '%\sys2%' order by publishtime asc;"""
        firstPublishTime = sys.maxsize
        try:
            output_PublishTime = []
            output_TimePassed = []
            totalTimePassed = 0
            self.cur.execute(sql)

            rows = self.cur.fetchall()
            firstPublishTime = rows[0][3]
            for row in rows:
                publishTime = row[3] - firstPublishTime
                timePassed = row[14] - row[3]
                output_PublishTime.append(publishTime)
                output_TimePassed.append(timePassed)
                totalTimePassed += timePassed

            print("B")
            print("Sys2 Pub - Sys2 Sub")
            print("Number of samples: " + str(len(rows)))
            print("Average time between Publisher(Sys2) - Subscriber(Sys2): " + str(totalTimePassed / len(rows)))
            print("--------------------------------------------------------------------")

            plt.plot(output_PublishTime, output_TimePassed)
            plt.title('From Pub(Sys2) - To Sub(Sys2)')
            plt.xlabel('Publishedtime')
            plt.ylabel('Time Passed')
            plt.show()
            
        except Exception as e:
            print(e)

    def getLogFromDifferentSystemForSys1(self):
        sql = """SELECT * FROM logstable WHERE firstmanagername is not NULL and publishername ilike '%\sys1%' order by publishtime asc;"""
        firstPublishTime = sys.maxsize
        try:
            output_PublishTime = []

            output_TimePassed_Total = []
            output_TimePassed_Publisher_FirstManager = []
            output_TimePassed_FirstManager_SecondManager = []
            output_TimePassed_SecondManager_Subscriber = []

            sumTimePassed_Total = 0
            sumTimePassed_Publisher_FirstManager = 0
            sumTimePassed_FirstManager_SecondManager = 0
            sumTimePassed_SecondManager_Subscriber = 0
            self.cur.execute(sql)

            rows = self.cur.fetchall()
            firstPublishTime = rows[0][3]
            for row in rows:
                # row[3] -> publishTime from original publisher
                # row[7] -> firstManager time
                # row[11] -> secondManager time
                # row[14] -> subscriber time
                publishTime = row[3] - firstPublishTime
                timePassed_Total = row[14] - row[3]
                timePassed_Publisher_FirstManager = row[7] - row[3]
                timePassed_FirstManager_SecondManager = row[11] - row[7]
                timePassed_SecondManager_Subscriber = row[14] - row[11]
                
                output_PublishTime.append(publishTime)

                output_TimePassed_Total.append(timePassed_Total)
                sumTimePassed_Total += timePassed_Total

                output_TimePassed_Publisher_FirstManager.append(timePassed_Publisher_FirstManager)
                sumTimePassed_Publisher_FirstManager += timePassed_Publisher_FirstManager

                output_TimePassed_FirstManager_SecondManager.append(timePassed_FirstManager_SecondManager)
                sumTimePassed_FirstManager_SecondManager += timePassed_FirstManager_SecondManager

                output_TimePassed_SecondManager_Subscriber.append(timePassed_SecondManager_Subscriber)
                sumTimePassed_SecondManager_Subscriber += timePassed_SecondManager_Subscriber

            print("C")
            print("Sys1 Pub - Sys2 Sub")
            print("Number of samples: " + str(len(rows)))
            print("Average time between Publisher(Sys1) - Subscriber(Sys2):       " + str(sumTimePassed_Total / len(rows)))
            print("Average time between Publisher(Sys1) - FirstManager(Sys1):     " + str(sumTimePassed_Publisher_FirstManager / len(rows)))
            print("Average time between FirstManager(Sys1) - SecondManager(Sys2): " + str(sumTimePassed_FirstManager_SecondManager / len(rows)))
            print("Average time between SecondManager(Sys2) - Subscriber(Sys2):   " + str(sumTimePassed_SecondManager_Subscriber / len(rows)))
            print("--------------------------------------------------------------------")

            plt.plot(output_PublishTime, output_TimePassed_Total)
            plt.title('From Pub(Sys1) - To Sub(Sys2) Arrival Time')
            plt.xlabel('Publishedtime in ms')
            plt.ylabel('Time Passed in ms')
            plt.show()

            plt.plot(output_PublishTime, output_TimePassed_Publisher_FirstManager)
            plt.title('From Pub(Sys1) - To FirstManager(Sys1) Arrival Time')
            plt.xlabel('Publishedtime in ms')
            plt.ylabel('Time Passed in ms')
            plt.show()

            plt.plot(output_PublishTime, output_TimePassed_FirstManager_SecondManager)
            plt.title('From FirstManager(Sys1) - To SecondManager(Sys2) Arrival Time')
            plt.xlabel('Publishedtime in ms')
            plt.ylabel('Time Passed in ms')
            plt.show()

            plt.plot(output_PublishTime, output_TimePassed_SecondManager_Subscriber)
            plt.title('From SecondManager(Sys2) - To Sub(Sys2) Arrival Time')
            plt.xlabel('Publishedtime in ms')
            plt.ylabel('Time Passed in ms')
            plt.show()
            
        except Exception as e:
            print(e)

    def getLogFromDifferentSystemForSys2(self):
        sql = """SELECT * FROM logstable WHERE firstmanagername is not NULL and publishername ilike '%\sys2%' order by publishtime asc;"""
        firstPublishTime = sys.maxsize
        try:
            output_PublishTime = []

            output_TimePassed_Total = []
            output_TimePassed_Publisher_FirstManager = []
            output_TimePassed_FirstManager_SecondManager = []
            output_TimePassed_SecondManager_Subscriber = []

            sumTimePassed_Total = 0
            sumTimePassed_Publisher_FirstManager = 0
            sumTimePassed_FirstManager_SecondManager = 0
            sumTimePassed_SecondManager_Subscriber = 0
            self.cur.execute(sql)

            rows = self.cur.fetchall()
            firstPublishTime = rows[0][3]
            for row in rows:
                # row[3] -> publishTime from original publisher
                # row[7] -> firstManager time
                # row[11] -> secondManager time
                # row[14] -> subscriber time
                publishTime = row[3] - firstPublishTime
                timePassed_Total = row[14] - row[3]
                timePassed_Publisher_FirstManager = row[7] - row[3]
                timePassed_FirstManager_SecondManager = row[11] - row[7]
                timePassed_SecondManager_Subscriber = row[14] - row[11]
                
                output_PublishTime.append(publishTime)

                output_TimePassed_Total.append(timePassed_Total)
                sumTimePassed_Total += timePassed_Total

                output_TimePassed_Publisher_FirstManager.append(timePassed_Publisher_FirstManager)
                sumTimePassed_Publisher_FirstManager += timePassed_Publisher_FirstManager

                output_TimePassed_FirstManager_SecondManager.append(timePassed_FirstManager_SecondManager)
                sumTimePassed_FirstManager_SecondManager += timePassed_FirstManager_SecondManager

                output_TimePassed_SecondManager_Subscriber.append(timePassed_SecondManager_Subscriber)
                sumTimePassed_SecondManager_Subscriber += timePassed_SecondManager_Subscriber

            print("D")
            print("Sys2 Pub - Sys1 Sub")
            print("Number of samples: " + str(len(rows)))
            print("Average time between Publisher(Sys2) - Subscriber(Sys1):       " + str(sumTimePassed_Total / len(rows)))
            print("Average time between Publisher(Sys2) - FirstManager(Sys2):     " + str(sumTimePassed_Publisher_FirstManager / len(rows)))
            print("Average time between FirstManager(Sys2) - SecondManager(Sys1): " + str(sumTimePassed_FirstManager_SecondManager / len(rows)))
            print("Average time between SecondManager(Sys1) - Subscriber(Sys1):   " + str(sumTimePassed_SecondManager_Subscriber / len(rows)))
            print("--------------------------------------------------------------------")

            plt.plot(output_PublishTime, output_TimePassed_Total)
            plt.title('From Pub(Sys2) - To Sub(Sys1) Arrival Time')
            plt.xlabel('Publishedtime in ms')
            plt.ylabel('Time Passed in ms')
            plt.show()

            plt.plot(output_PublishTime, output_TimePassed_Publisher_FirstManager)
            plt.title('From Pub(Sys2) - To FirstManager(Sys2) Arrival Time')
            plt.xlabel('Publishedtime in ms')
            plt.ylabel('Time Passed in ms')
            plt.show()

            plt.plot(output_PublishTime, output_TimePassed_FirstManager_SecondManager)
            plt.title('From FirstManager(Sys2) - To SecondManager(Sys1) Arrival Time')
            plt.xlabel('Publishedtime in ms')
            plt.ylabel('Time Passed in ms')
            plt.show()

            plt.plot(output_PublishTime, output_TimePassed_SecondManager_Subscriber)
            plt.title('From SecondManager(Sys1) - To Sub(Sys1) Arrival Time')
            plt.xlabel('Publishedtime in ms')
            plt.ylabel('Time Passed in ms')
            plt.show()
            
        except Exception as e:
            print(e)



if __name__ == "__main__":
    # statisticsTest = Statistics("127.0.0.1", 5000, "logDB-test1-pub1-sub1-25ms-5hours", "masterdbpassword")
    # statisticsTest = Statistics("127.0.0.1", 5000, "logDB-test2-pub1-sub1-10ms-5hours", "masterdbpassword")
    # statisticsTest = Statistics("127.0.0.1", 5000, "logDB-test3-pub1-sub1-5ms-2hours-30mins", "masterdbpassword")
    # statisticsTest = Statistics("127.0.0.1", 5000, "logDB-test4-pub1-sub1-2ms-1hour", "masterdbpassword")
    # statisticsTest = Statistics("127.0.0.1", 5000, "logDB-test5-pub2-sub1-2ms-1hour", "masterdbpassword")
    # statisticsTest = Statistics("127.0.0.1", 5000, "logDB-NewTest5-pub1-sub1-1ms-1hour", "masterdbpassword")
    # statisticsTest = Statistics("127.0.0.1", 5000, "logDB-NewTest4-pub1-sub1-2ms-1hour", "masterdbpassword")
    # statisticsTest = Statistics("127.0.0.1", 5000, "logDB-NewTest3-pub1-sub1-5ms-1hour", "masterdbpassword")
    # statisticsTest = Statistics("127.0.0.1", 5000, "logDB-NewTest2-pub1-sub1-10ms-1hour", "masterdbpassword")
    statisticsTest = Statistics("127.0.0.1", 5000, "logDB-NewTest1-pub1-sub1-25ms-1hour", "masterdbpassword")
    statisticsTest.getLogFromSameSystemForSys1()
    statisticsTest.getLogFromSameSystemForSys2()
    statisticsTest.getLogFromDifferentSystemForSys1()
    statisticsTest.getLogFromDifferentSystemForSys2()