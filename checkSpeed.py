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

dataDir = "/home/pi/speedtestResults"

def list2obj(currentDate, currentTime, ping, download, upload, ssid, freq, signal, bitrate, hostname):
	outputObj = {}
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
  response = subprocess.Popen('speedtest-cli --simple', shell=True, stdout=subprocess.PIPE).stdout.read()

  ping = re.findall('Ping:\s(.*?)\s', response, re.MULTILINE)
  download = re.findall('Download:\s(.*?)\s', response, re.MULTILINE)
  upload = re.findall('Upload:\s(.*?)\s', response, re.MULTILINE)

  ping[0] = ping[0].replace(',', '.')
  download[0] = download[0].replace(',', '.')
  upload[0] = upload[0].replace(',', '.')
  
  wifiResponse = subprocess.Popen('iw dev wlan0 link', shell=True, stdout=subprocess.PIPE).stdout.read()
  ssid = re.findall('SSID:\s(.*?)\s', wifiResponse, re.MULTILINE)
  freq = re.findall('freq:\s(.*?)\s', wifiResponse, re.MULTILINE)
  signal = re.findall('signal:\s(.*?)\s', wifiResponse, re.MULTILINE)
  bitrate = re.findall('tx bitrate:\s(.*?)\s', wifiResponse, re.MULTILINE)

  ssid[0] = ssid[0].replace(',', '.')
  freq[0] = freq[0].replace(',', '.')
  signal[0] = signal[0].replace(',', '.')
  bitrate[0] = bitrate[0].replace(',', '.')

  hostname = subprocess.Popen('hostname', shell=True, stdout=subprocess.PIPE).stdout.read()

  tmpObj = {}
  tmpObj["results"] = list2obj(currentDate, currentTime, ping[0], download[0], upload[0], ssid[0], freq[0], signal[0], bitrate[0], hostname)
  filePath = dataDir + "/" + str(currentData) + "-" + str(currentTime) + "-" + hostname + ".json"

  print tmpObj["results"]
  try:
    open(filePath, "wb").write(json.dumps(tmpObj))
  except:
    print "Error writing results..."
    pass

  #try:
  #  if os.stat('/home/pi/speedtestResults/speedtest.csv').st_size == 0:
  #      print 'Date,Time,Ping (ms),Download (Mbit/s),Upload (Mbit/s),SSID,Frequency (MHz),Signal (dBm),Bitrate (MBit/s), Hostname'
  #except:
  #  pass

  #print '{},{},{},{},{},{},{},{},{},{}'.format(currentDate, currentTime, ping[0], download[0], upload[0], ssid[0], freq[0], signal[0], bitrate[0], hostname)

if __name__ == '__main__':
	main()
