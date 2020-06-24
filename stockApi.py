import requests
import json

headers = {"Accept": "application/json"}


def getStockData():
    access_key = "pk_d397206ec9004c4c826bb2aa114b32b9"
    url = "https://cloud.iexapis.com/stable/stock/AAPL/quote?token={}".format(
        access_key)
    data = requests.get(url)
    data = data.json()
    print()
    print('<=== API RETURNED ===>')
    print(data)
    print()

    if (data):
        return data
    else:
        return None
