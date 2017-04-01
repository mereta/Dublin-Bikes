import urllib
import json
import urllib.request
import requests

def GetLocationData():
    ''' Retrieves Data in JSON format from the Dublin Bikes API'''
    
    link = "https://api.jcdecaux.com/vls/v1/stations?contract=dublin&apiKey=858b04c120b7c1371e65f9d5528cf4a57858f3cd"

    try:
        r = requests.get(link)
    except requests.ConnectionError:
        logger.log(datetime.now, "Connection Error")
    else:
        return r.json()
