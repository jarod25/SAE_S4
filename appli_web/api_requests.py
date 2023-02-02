import pandas as pd
import requests
import json


def request_countries():
    req = requests.get('https://api.covid19api.com/summary').json()
    country = req['Countries']
    return country
