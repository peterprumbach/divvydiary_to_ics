import os
import requests
import json
from ics import Calendar, Event
import arrow
from dateutil import tz
import datetime

def createAPIFile():
    jsonString = {'apiKey': 'insert here'}
    json.dump(jsonString, open('config.json', 'w'))

def apiKeyExists():
    if(os.path.isfile('config.json')):
        with open('config.json', 'r') as config:
            apiFile=config.read()

        apiKey = json.loads(apiFile)
        
        if(apiKey['apiKey'] == 'insert here'):
            return False
        else:
            return True
    else:
        return False

def getAPIKey():
    with open('config.json', 'r') as config:
        apiFile=config.read()

    apiKey = json.loads(apiFile)
    return apiKey['apiKey']    

def getUserDetails(apiKey):
    headers = {
        'User-Agent': "DivvyDiary to ICS",
        'accept': 'application/json',
        'X-API-KEY': apiKey,
    }

    response = requests.get("https://api.divvydiary.com/session", headers=headers)
    json_data = json.loads(response.text)

    return [json_data['currency'], str(json_data['id'])]

def getDividends(currency, userid):
    headers = {
        'User-Agent': "DivvyDiary to ICS",
        'accept': 'application/json',
        'X-API-KEY': getAPIKey(),
    }

    params = (
        ('currency', currency),
        ('userId', userid),
    )

    response = requests.get('https://api.divvydiary.com/dividends/upcoming', headers=headers, params=params)
    json_data = json.loads(response.text)

    dividends=json_data['dividends']

    c = Calendar()

    for asset in dividends:
        e = Event()
        e.name = asset['name']
        e.begin = arrow.get(asset['payDate'], tzinfo='Europe/Berlin')
        e.duration = {"hours": 24}
        payment = round((float(asset['amount'])*float(asset['quantity'])*float(asset['exchangeRate'])), 2)
        exDate = arrow.get(asset['exDate'], tzinfo='Europe/Berlin').format('DD.MM.YYYY')
        payDate = arrow.get(asset['payDate'], tzinfo='Europe/Berlin').format('DD.MM.YYYY')
        e.description = f"Dividende: " + str(payment).replace(".", ",") + " EUR" + "\n\nEx-Dividende: " + exDate + "\n\nZahltag: " + payDate
        e.make_all_day
        c.events.add(e)

    with open('calendar.ics', 'w') as f:
        f.writelines(c)

def main():
    if(apiKeyExists()):
        userDetails = getUserDetails(getAPIKey())
        getDividends(userDetails[0], userDetails[1])
    else:
        createAPIFile()

if __name__ == '__main__':
    main()
