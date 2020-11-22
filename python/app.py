import requests
import csv
from datetime import datetime


def fetchData(url):
  data = requests.get(url)
  saveTempFile(data.text)

def saveTempFile(data):
  f = open('tmp.csv','w+')
  f.write(data)
  f.close()
  cleanData()

def cleanData():
  try:
    reader = csv.DictReader(open('tmp.csv','r'))
    cases = []
    for line in reader:
      line["date"] = datetime.strptime(line["date"],'%Y-%m-%d').date()
      cases.append(line)
  except Exception as e: 
    print("Exception occured file " + str(e))

if __name__ == "__main__":
  fetchData("https://raw.githubusercontent.com/nytimes/covid-19-data/master/us.csv")