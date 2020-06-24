import requests
import json

headers = {"access_key": "7f5d2ac0d8e3f3ac7b9f572dcc3c9ecf",
           "Accept": "application/json"}


def getWeatherByLocation(location_name):
    data = {"access_key": "7f5d2ac0d8e3f3ac7b9f572dcc3c9ecf",
            "query": location_name}
    url = "http://api.weatherstack.com/current"
    data = requests.get(url, params=data)
    data = data.json()
    print()
    print('<=== API RETURNED ===>')
    print(data)
    print()

    if (data):
        return data
    else:
        return None
