import urllib3
import json
import csv
from datetime import datetime

rawCases = []

def fetchData(url):
  http = urllib3.PoolManager()
  request = http.request('GET', url)
  if request.status == 200:
    return request.data.decode('utf-8')
  else:
    raise Exception()

def parseData(url):
  try: 
    data = fetchData(url)
    reader = csv.DictReader(data.split("\n"), delimiter=',')
    for row in reader:
      rawCases.append(row)
  except Exception as e:
    print("Failed to parse data from url " + str(e))

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
  parseData(url)

if __name__ == "__main__":
  try :
    parseData("https://raw.githubusercontent.com/nytimes/covid-19-data/master/us.csv")
    cleanData()
  except Exception as e:
    print("An error occured while fetching data" + str(e))