import requests, json, creds
from pprint import pprint

API_KEY = creds.binance_api_key
API_SECRET = creds.binance_api_secret


class Binance():
    api_url = 'https://api.binance.com/api/v3/'

    def __init__(self, api_key, secret_key):
        self.api_key = api_key
        self.secret_key = secret_key

    def api_call(self, endpoint: str):
        r = requests.get(self.api_url + endpoint)
        return r.json()  


if __name__ == '__main__':
    b = Binance(API_KEY, API_SECRET)
    test = b.api_call("time")
    pprint(test)