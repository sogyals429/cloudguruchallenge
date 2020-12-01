import urllib3
import json
import csv
from datetime import datetime
import logging

logging.basicConfig(level=logging.INFO,format='%(asctime)s:%(name)s:%(levelname)s:%(message)s', datefmt='%d-%m-%Y %I:%M:%S %p')
log = logging.getLogger("app")

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
  data = fetchData(url)
  try: 
    rawCases = []
    reader = csv.DictReader(data.split("\n"), delimiter=',')
    for row in reader:
      rawCases.append(row)
    logging.debug("Cases fetched and appended to array")
    return rawCases
  except Exception as e:
    logging.error("Failed to parse data from url " + str(e),exc_info=True)

def cleanData(rawCases):
  try:
    cleanedData = parseDate(rawCases)
    return cleanedData
  except Exception as e: 
    print("Exception occured while formatting data " + str(e))

def parseDate(csvData):
  try:
    cases = []
    for line in csvData:
      if line.get('date'):
        line["date"] = datetime.strptime(line["date"],'%Y-%m-%d').date()
        cases.append(line)
      elif line.get('Date'):
        line["Date"] = datetime.strptime(line["Date"],'%Y-%m-%d').date()
        cases.append(line)
    return cases
  except Exception as e:
    print("Exception occured while parsing date " + str(e))

def formatData(originalCases):
  url = "https://raw.githubusercontent.com/datasets/covid-19/master/data/time-series-19-covid-combined.csv"
  cases = parseData(url)
  usCases = cleanData(filterData(cases))

  for case in originalCases:
    for johnCase in usCases:
      if case["date"] == johnCase["Date"]:
        case["Recovered"] = johnCase["Recovered"]
  return originalCases

def filterData(cases):
  try:
    rawCases = []
    for case in cases:
      if case["Country/Region"] == "US":
        rawCases.append(case)
    return rawCases
  except Exception as e:
    print("Exception")


def logDebug(message):
  logging.debug(message)

if __name__ == "__main__":
  # nyTimesCases = parseData("https://raw.githubusercontent.com/nytimes/covid-19-data/master/us.csv")
  nyTimesCases = parseData("localhost")
  cleanedDataNy = cleanData(nyTimesCases)
  formatData(cleanedDataNy)