#import pandas as pd
#df = pd.read_csv (r'nycoordinates1.csv')
#df.to_json (r'nycoordinates1.json')

#mydict1 = df.to_dict()
#print(mydict1)
from csv import DictReader
from csv import reader
import json
import requests
import time
from random import randrange

# open file in read mode
with open('nycoordinates2.csv', 'r') as read_obj:
    # pass the file object to reader() to get the reader object
    csv_dict_reader = DictReader(read_obj)
    for row in csv_dict_reader:
        # row variable is a list that represents a row in csv
        #print(round(float(row['slat']),2))
        #print(row['slon'])
        #print(row['dlat'])
        #print(row['dlon'])
        GeopointTelemetrydict={'origin': str(round(float(row['slon']),5))+','+str(round(float(row['slat']),5))}
        GeopointTelemetrydict.update({'destination': str(round(float(row['dlon']),5))+','+str(round(float(row['dlat']),5))})
        GeopointTelemetrydict.update({'key': 'XXXXXXXXXXXXXXX'})
        payload = json.dumps(GeopointTelemetrydict) 
        print(payload)
        #queryres = requests.post(url = "http://localhost:7071/api/GenerateCoordinates", data = payload, headers = {'Content-type': 'application/json'})
        #queryres = requests.post(url = "https://fngeoloc.azurewebsites.net/api/GenerateCoordinates?code=XXXXXXXXXXXXXXX", data = payload, headers = {'Content-type': 'application/json'})
        queryres = requests.post(url = "https://fngeneratetripdata.azurewebsites.net/api/GenerateCoordinates?code=XXXXXXXXXXXXXXX", data = payload, headers = {'Content-type': 'application/json'})
        print(queryres.text)
        time.sleep(randrange(2))