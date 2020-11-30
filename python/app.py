import urllib3
import json
import csv
from datetime import datetime

def fetchData(url):
  http = urllib3.PoolManager()
  request = http.request('GET', url)
  if request.status == 200:
    return request.data.decode('utf-8')
  else:
    raise Exception()

def parseData(url):
  rawCases = []
  try: 
    data = fetchData(url)
    reader = csv.DictReader(data.split("\n"), delimiter=',')
    for row in reader:
      rawCases.append(row)
    return rawCases
  except Exception as e:
    print("Failed to parse data from url " + str(e))

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
        print(case)
  

def filterData(cases):
  rawCases = []
  for case in cases:
    if case["Country/Region"] == "US":
      rawCases.append(case)
  return rawCases

if __name__ == "__main__":
  try :
    nyTimesCases = parseData("https://raw.githubusercontent.com/nytimes/covid-19-data/master/us.csv")
    cleanedDataNy = cleanData(nyTimesCases)
    formatData(cleanedDataNy)
  except Exception as e:
    print("An error occured while fetching data " + str(e))