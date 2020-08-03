import os
from dotenv import load_dotenv
import requests
import json
import pwaqi
from pyowm import OWM
import meteomatics.api as api
from weatherbit.api import Api

load_dotenv('secrets.env')
usernameM = os.getenv('usernameM')
passwordM = os.getenv('passwordM')
token = os.getenv('token')
openWeatherToken = os.getenv('openWeatherToken')
weatherbitToken = os.getenv('weatherBitToken')



class Climate:
    def __init__(self, username, password, token, openWeatherToken, weatherbit):
        self.username = username
        self.password = password
        self.token = token
        self.owm = OWM(openWeatherToken)
        self.weatherbit = weatherbit
    def getAQI(self, x, y):
        try:
            res = pwaqi.get_location_observation(x, y, self.token)
            print(res)
            if res == 'None' or res is None:
                res = 0
            return res['aqi']
        except Exception as e:
            print("Failed, the exception is {}".format(e))
            return 0
    def getTemp(self, x, y):
        try:
            res = api.query_api("https://api.meteomatics.com/now/t_2m:C/{},{}/json".format(x, y), self.username, self.password)
            print(res.headers)
            print(res.content)
            if res == 'None' or res is None:
                res = 25
            return res.json()['data'][0]['coordinates'][0]['dates'][0]['value']
        except Exception as e:
            print("Failed, the exception is {}".format(e))
            return 25
    def getDust(self, x, y):
        try:
            res = api.query_api("https://api.meteomatics.com/now/dust_aod_550nm:idx/{},{}/json".format(x, y), self.username, self.password)
            print(res.headers)
            print(res.content)
            if res == 'None' or res is None:
                res = 0
            return res.json()['data'][0]['coordinates'][0]['dates'][0]['value']
        except Exception as e:
            print("Failed, the exception is {}".format(e))
            return 0
    # Broken
    def getPollen(self, x, y):
        try:
            res = requests.get(url="https://api.weatherbit.io/v2.0/current/airquality?lat={x}&lon={y}&key={API_KEY}".format(x = x, y = y, API_KEY = self.weatherbit))
            res = res.json()['data'][0]['pollen_level_weed']
            if res == 'None' or res is None:
                res = 0
            return res
        except Exception as e:
            print("Failed, the exception is {}".format(e))
            return 0
    def getHumidity(self, x, y):
        try:
            mgr = self.owm.weather_manager()
            observation_list = mgr.weather_around_coords(x, y)
            res = observation_list[0].weather.humidity
            if res == 'None' or res is None:
                res = 50
            return res
        except Exception as e:
            print("Failed, the exception is {}".format(e))
            return 50
    def getCloudCover(self, x, y):
        try:
            res = api.query_api("https://api.meteomatics.com/now/effective_cloud_cover:octas/{},{}/json".format(x, y), self.username, self.password)
            print(res.headers)
            print(res.content)
            res = res.json()['data'][0]['coordinates'][0]['dates'][0]['value']
            if res == 'None' or res is None:
                res = 0
            return res
        except Exception as e:
            print("Failed, the exception is {}".format(e))
            return 0
    def getHeatIndex(self, x, y):
        try:
            res = api.query_api("https://api.meteomatics.com/now/heat_index:C/{},{}/json".format(x, y), self.username, self.password)
            print(res.headers)
            print(res.content)
            res = res.json()['data'][0]['coordinates'][0]['dates'][0]['value']
            if res == 'None' or res is None:
                res = 25
            return res
        except Exception as e:
            print("Failed, the exception is {}".format(e))
            return 25
    def getSO2(self, x, y):
        try:
            res = api.query_api("https://api.meteomatics.com/now/sulphate_aod_550nm:idx/{},{}/json".format(x, y), self.username, self.password)
            print(res.headers)
            print(res.content)
            res = res.json()['data'][0]['coordinates'][0]['dates'][0]['value']
            if res == 'None' or res is None:
                res = 0
            return res
        except Exception as e:
            print("Failed, the exception is {}".format(e))
            return 0
    def getUVI(self, x, y):
        try:
            x= int(x)
            y=int(y)
            mgr = self.owm.uvindex_manager()
            observation_list = mgr.uvindex_around_coords(x, y)
            res = observation_list.value
            if res == 'None' or res is None:
                res = 3
            return res
        except Exception as e:
            print("Failed, the exception is {}t".format(e))
            return 3

    def getAllMetrics(self, x, y):
        climateData = []
        # flip x and y cuz lat and long
        climateData.append(self.getAQI(y, x))
        climateData.append(self.getPollen(y, x))
        climateData.append(self.getDust(y, x))
        climateData.append(self.getTemp(y, x))
        climateData.append(self.getHumidity(y, x))
        climateData.append(self.getCloudCover(y, x))
        climateData.append(self.getHeatIndex(y, x))
        climateData.append(self.getSO2(y, x))
        climateData.append(self.getUVI(y, x))
        return dict(zip(['AQI','Pollen','Dust',"Temperature",'Humidity','CloudCover','HeatIndex','S02','UVI'],climateData)),climateData


#climate = Climate(usernameM, passwordM, token, openWeatherToken, weatherbitToken)
# Use 35, -80
