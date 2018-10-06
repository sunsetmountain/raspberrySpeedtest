import os
import time
from google.cloud import storage
from oauth2client.service_account import ServiceAccountCredentials
from tendo import singleton

me = singleton.SingleInstance() # will sys.exit(-1) if another instance of this script is already running

dataDir = "/home/pi/raspberrySpeedtest/speedtestResults"
bucket_name = "bucketnamegoeshere"
keyfile = "/home/pi/enterYourKeyfileName.json" #change to your keyfile name

def upload_blob(fileList):

  scopesList = ["https://www.googleapis.com/auth/storage"]
  credentialsObj = ServiceAccountCredentials.from_json_keyfile_name(
    keyfile,
    scopes = scopesList
  )

  #credentials = GoogleCredentials.get_application_default()

  """Uploads a file to the bucket."""
  storage_client = storage.Client()
  bucket = storage_client.get_bucket(bucket_name)

  numberOfFiles = 0
  for fileName in fileList:
    numberOfFiles = numberOfFiles + 1
    destination_blob_name = fileName
    source_file_name = dataDir + "/" + fileName
      
    blob = bucket.blob(destination_blob_name)
    blob.upload_from_filename(source_file_name)

    print('File {} uploaded to {}.'.format(
      source_file_name,
      destination_blob_name))

  print "Uploaded " + str(numberOfFiles) + " files"
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
          #msgList = loadList(fileList)
          #print len(msgList)

          try:
	    if len(fileList) > 0:
              upload_blob(fileList)
              for fileName in fileList:
                filePath = dataDir + "/" + fileName
                os.remove(filePath)
            else:
              print "No files to send..."
            time.sleep(60)

          except KeyboardInterrupt:
            quit()

          except Exception,e:
            print "Encountered error..."
            print e
            continue


if __name__ == "__main__":
	main()
