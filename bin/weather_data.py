import os,sys
import csv
import requests
import json

splunk_home=os.getenv("SPLUNK_HOME")
apps_path=os.path.join(splunk_home,'etc','apps')
app_name="my_weather_monitoring"
app_path=os.path.join(apps_path,app_name)
locations_csv_path=os.path.join(app_path,'lookups','locations.csv')
api_key="apikey" # your api key

def get_weather_detials(city,latitute,longitude):
    response=requests.get(url=f"https://api.openweathermap.org/data/2.5/weather?lat={latitute}&lon={longitude}&appid={api_key}&units=metric")
    response=json.loads(response.text)
    response['name']=city
    response=json.dumps(response)
    print(response)

def get_latitude_longitude(city,state,country):
    response=requests.get(url=f"http://api.openweathermap.org/geo/1.0/direct?q={city},{state}&limit=1&appid={api_key}")
    if response.status_code==200:
        latitude=response.json()[0].get("lat")
        longitude=response.json()[0].get("lon")
        return latitude,longitude

with open(locations_csv_path,'r') as location_csv_file:
    csv_reader=csv.DictReader(location_csv_file)
    for row in csv_reader:
        city=row.get('city')
        state=row.get('state')
        country=row.get('country')
        disabled=int(row.get('disable'))
        if not disabled:
            latitude,longitude=get_latitude_longitude(city,country,state)
            get_weather_detials(city,latitude,longitude)