import requests
import csv
from datetime import datetime
import logging

logging.basicConfig(level=logging.INFO,format='%(asctime)s:%(name)s:%(levelname)s:%(message)s', datefmt='%d-%m-%Y %I:%M:%S %p')
log = logging.getLogger("app")


def fetchData(url):
  data = requests.get(url)
  if data.status_code == 200:
    return data.text
  else:
    return data.text

def parseData(url):
  data = fetchData(url)
  rawCases = []
  reader = csv.DictReader(data.split("\n"), delimiter=',')
  for row in reader:
    rawCases.append(row)
  return rawCases

def parseDate(data):
  cases = []
  for line in data:
    line["date"] = datetime.strptime(line["date"],'%Y-%m-%d').date()
    cases.append(line)
  return cases

def joinData(cases):
  tempCases = []
  for johnCase in cases:
    if johnCase["Country/Region"] == "US":    
      tempCases.append(johnCase)
  return tempCases

def filterData(nyCases,johnHopkins):
  for case in nyCases:
    for johnCase in johnHopkins:
      if str(case["date"].strftime('%Y-%m-%d')) == johnCase["Date"]:
        case["Recovered"] = johnCase["Recovered"]
  return nyCases



if __name__ == "__main__":
  cases = parseData("https://raw.githubusercontent.com/nytimes/covid-19-data/master/us.csv")
  nyCases = parseDate(cases)
  johnHopkins = parseData("https://raw.githubusercontent.com/datasets/covid-19/master/data/time-series-19-covid-combined.csv")
  data = joinData(johnHopkins)
  print(filterData(nyCases,johnHopkins))