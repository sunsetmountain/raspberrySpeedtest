import os
import time
from google.cloud import pubsub
from oauth2client.service_account import ServiceAccountCredentials
from tendo import singleton

me = singleton.SingleInstance() # will sys.exit(-1) if another instance of this script is already running

dataDir = "/home/pi/raspberrySpeedtest/speedtestResults"
keyfile = "/home/pi/enterYourKeyfileName.json" #change to your keyfile name

def publishBatch(msgList):

  scopesList = ["https://www.googleapis.com/auth/pubsub"]
  credentialsObj = ServiceAccountCredentials.from_json_keyfile_name(
    keyfile,
    scopes = scopesList
  )

  #credentials = GoogleCredentials.get_application_default()

  pubsubClient = pubsub.Client(
    project="[projectName]"
  )

  topicName = "raw-speedtest-data"
  topicObj = pubsubClient.topic(topicName)
  with topicObj.batch() as batchObj:
    for eachItem in msgList:
      eachItem = eachItem.encode("utf-8")
      batchObj.publish(eachItem)

  return


def loadList(fileList):
        msgList = []
        for fileName in fileList:
                filePath = dataDir + "/" + fileName
		with open(filePath) as fileObj:
                        fileContents = fileObj.read()
                        msgList.append(fileContents)

        return msgList


def main():
        while True:
                fileList = os.listdir(dataDir)
        	msgList = loadList(fileList)
        	print len(msgList)

                try:
                        if len(msgList) > 0:
                                publishBatch(msgList)
                                for fileName in fileList:
                                        filePath = dataDir + "/" + fileName
                                        os.remove(filePath)
                        else:
                                print "No messages to send..."
                        time.sleep(60)

                except KeyboardInterrupt:
                        quit()
                
                except Exception,e:
                        print "Encountered error..."
                        print e
                        continue


if __name__ == "__main__":
	main()
