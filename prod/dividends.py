import requests
import json
import DivvyDiary

def getUpcomingDividends():
    headers = {
        'User-Agent': "DivvyDiary to ICS",
        'accept': 'application/json',
        'X-API-KEY': DivvyDiary.getAPIKey(),
    }

    params = (
        ('currency', DivvyDiary.getUserDetails()[0]),
        ('userId', DivvyDiary.getUserDetails()[1]),
    )

    response = requests.get('https://api.divvydiary.com/dividends/upcoming', headers=headers, params=params)
    json_data = json.loads(response.text)

    dividends=json_data['dividends']
    
    return dividends
