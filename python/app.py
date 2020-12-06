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
    raise Exception()

def parseData(url):
  data = fetchData(url)
  f = open('tmp.csv','w+')
  f.write(data)
  f.close()
  
def cleanData():
  reader = csv.DictReader(open('tmp.csv','r'))
  cases = []
  for line in reader:
    line["date"] = datetime.strptime(line["date"],'%Y-%m-%d').date()
    cases.append(line)
    # formatData()
    print(cases)

def formatData():
  url = "https://raw.githubusercontent.com/datasets/covid-19/master/data/time-series-19-covid-combined.csv"
  cases = parseData(url)
  usCases = cleanData(filterData(cases))


if __name__ == "__main__":
  parseData("https://raw.githubusercontent.com/nytimes/covid-19-data/master/us.csv")
  cleanData()