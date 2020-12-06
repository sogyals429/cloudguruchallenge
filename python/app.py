import urllib3
import json
import csv
from datetime import datetime
import logging

logging.basicConfig(level=logging.INFO,format='%(asctime)s:%(name)s:%(levelname)s:%(message)s', datefmt='%d-%m-%Y %I:%M:%S %p')
log = logging.getLogger("app")

rawCases = []

def fetchData(url):
  try:
    http = urllib3.PoolManager()
    request = http.request('GET', url)
    if request.status == 200:
      logDebug(request.data.decode('utf-8'))
      log.info('Fetching Data from %s', url)
      return request.data.decode('utf-8')
    else:
      log.error('Website not available: ' + request.status)
  except Exception as e:
    log.error('Failed to fetch data',exc_info=True)

def parseData(url):
    for row in reader:
      rawCases.append(row)
  except Exception as e:
    logging.error("Failed to parse data from url " + str(e),exc_info=True)

def cleanData():
  try:
    cleanedData = parseDate(rawCases)
  except Exception as e: 
    print("Exception occured while formatting data " + str(e))

def parseDate(csvData):
  cases = []
  for line in csvData:
    line["date"] = datetime.strptime(line["date"],'%Y-%m-%d').date()
    cases.append(line)
  return cases

def formatData():
  url = "https://raw.githubusercontent.com/datasets/covid-19/master/data/time-series-19-covid-combined.csv"
  cases = parseData(url)
  usCases = cleanData(filterData(cases))

    parseData("https://raw.githubusercontent.com/nytimes/covid-19-data/master/us.csv")
    cleanData()
  except Exception as e:
    print("An error occured while fetching data" + str(e))