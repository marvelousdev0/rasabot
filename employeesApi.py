import requests
import json

headers = {"Accept": "application/json"}

def getEmployeeDetails(employeeid):
    url = 'http://localhost:8000/api/v1/employees/{}'.format(employeeid)
    print()
    print("<==== Employee api ====>")
    data = requests.get(url)
    data = data.json()
    print(data)
    print()

    if (data):
        return data
    else:
        return None