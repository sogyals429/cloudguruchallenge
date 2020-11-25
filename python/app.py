import requests
import csv
from datetime import datetime


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
  try:
    reader = csv.DictReader(open('tmp.csv','r'))
    cases = []
    for line in reader:
      line["date"] = datetime.strptime(line["date"],'%Y-%m-%d').date()
      cases.append(line)
      # formatData()
      print(cases)
  except Exception as e: 
    print("Exception occured file " + str(e))

def formatData():
  url = "https://raw.githubusercontent.com/datasets/covid-19/master/data/time-series-19-covid-combined.csv"
  parseData(url)

if __name__ == "__main__":
  try :
    parseData("https://raw.githubusercontent.com/nytimes/covid-19-data/master/us.csv")
    cleanData()
  except Exception as e:
    print("An error occured while fetching data")