#!/usr/bin/env python
# encoding: utf-8

import os
import re
import subprocess
import json
import time
import socket
import datetime
import calendar
from tendo import singleton

me = singleton.SingleInstance() # will sys.exit(-1) if another instance of this script is already running

dataDir = "/home/pi/raspberrySpeedtest/speedtestResults"

def mkEpoch(inputDatestamp, inputTimestamp):
	inputDatestamp = inputDatestamp.replace("/", "-")
	inputStr = inputDatestamp + " " + inputTimestamp

	datetimeObj = datetime.datetime.strptime(inputStr, "%Y-%m-%d %H:%M:%S")
	epochVal = calendar.timegm(datetimeObj.timetuple())
	epochString = str(epochVal)
	return epochString

def list2obj(timestamp, currentDate, currentTime, ping, download, upload, ssid, freq, signal, bitrate, hostname):
	outputObj = {}
	outputObj["timestamp"] = timestamp
	outputObj["collectiondate"] = currentDate
	outputObj["collectiontime"] = currentTime
	outputObj["ping"] = ping
	outputObj["download"] = download
	outputObj["upload"] = upload
	outputObj["ssid"] = ssid
	outputObj["frequency"] = freq
	outputObj["signal"] = signal
	outputObj["bitrate"] = bitrate
	outputObj["hostname"] = hostname
	return outputObj

def main():
  currentDate = datetime.datetime.utcnow().strftime('%Y-%m-%d')
  currentTime = datetime.datetime.utcnow().strftime('%H:%M:%S')
  timestamp = str(currentDate) + " " + str(currentTime)

  #Run the speed test
  response = subprocess.Popen('speedtest-cli --simple', shell=True, stdout=subprocess.PIPE).stdout.read()

  #Collect speed test results
  ping = re.findall('Ping:\s(.*?)\s', response, re.MULTILINE)
  download = re.findall('Download:\s(.*?)\s', response, re.MULTILINE)
  upload = re.findall('Upload:\s(.*?)\s', response, re.MULTILINE)
  ping[0] = ping[0].replace(',', '.')
  download[0] = download[0].replace(',', '.')
  upload[0] = upload[0].replace(',', '.')

  #Collect wifi information
  wifiResponse = subprocess.Popen('iw dev wlan0 link', shell=True, stdout=subprocess.PIPE).stdout.read()
  ssid = re.findall('SSID:\s(.*?)\s', wifiResponse, re.MULTILINE)
  freq = re.findall('freq:\s(.*?)\s', wifiResponse, re.MULTILINE)
  signal = re.findall('signal:\s(.*?)\s', wifiResponse, re.MULTILINE)
  bitrate = re.findall('tx bitrate:\s(.*?)\s', wifiResponse, re.MULTILINE)
  ssid[0] = ssid[0].replace(',', '.')
  freq[0] = freq[0].replace(',', '.')
  signal[0] = signal[0].replace(',', '.')
  bitrate[0] = bitrate[0].replace(',', '.')

  #Determine the hostname of this computer
  hostname = subprocess.Popen('hostname', shell=True, stdout=subprocess.PIPE).stdout.read().rstrip()

  tmpObj = {}
  tmpObj = list2obj(timestamp, currentDate, currentTime, ping[0], download[0], upload[0], ssid[0], freq[0], signal[0], bitrate[0], hostname)
  #tmpObj["results"] = list2obj(timestamp, currentDate, currentTime, ping[0], download[0], upload[0], ssid[0], freq[0], signal[0], bitrate[0], hostname)
  #print tmpObj["results"]

  #Create a unique filename to write to
  filename = hostname + "-" + mkEpoch(str(currentDate), str(currentTime))
  filePath = dataDir + "/" + filename + ".json"
  #print filePath


  #Make sure there is a directory to put the results into
  try:
    os.mkdir(dataDir)
  except OSError:  
    print ("Results directory exists")
  else:  
    print ("Successfully created the directory %s " % dataDir)

  #Write the results to a JSON file
  try:
    open(filePath, "wb").write(json.dumps(tmpObj))
    print "Successfully wrote results to " + filePath
  except:
    print "Error writing results..."
    pass

if __name__ == '__main__':
	main()
