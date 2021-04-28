import os
import requests
import json

# Create API-key file if not exist
def createAPIFile():
    jsonString = {'apiKey': 'insert here'}
    json.dump(jsonString, open(os.getcwd() + "/src/config.json", 'w'))

# Check if API-key file exists
def apiKeyExists():
    if(os.path.isfile(os.getcwd() + "/src/config.json")):
        with open(os.getcwd() + "/src/config.json", 'r') as config:
            apiFile=config.read()

        apiKey = json.loads(apiFile)
        
        if(apiKey['apiKey'] == 'insert here'):
            return False
        else:
            return True
    else:
        return False

# Get API-key from config file
def getAPIKey():
    if(apiKeyExists()):
        with open(os.getcwd() + "/src/config.json", 'r') as config:
            apiFile=config.read()

        apiKey = json.loads(apiFile)
        return apiKey['apiKey']
    else:
        createAPIFile()

# Get user id and local currency from DivvyDiary
def getUserDetails():
    headers = {
        'User-Agent': "DivvyDiary to ICS",
        'accept': 'application/json',
        'X-API-KEY': getAPIKey(),
    }

    response = requests.get("https://api.divvydiary.com/session", headers=headers)
    json_data = json.loads(response.text)

    return [json_data['currency'], str(json_data['id'])]
