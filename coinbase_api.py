import json, hmac, hashlib, time, requests, creds, my_debug, datetime
from pprint import pprint
from requests.auth import AuthBase

API_KEY = creds.coinbase_api_key
API_SECRET = creds.coinbase_api_secret

class CoinbaseWalletAuth(AuthBase):
    def __init__(self, api_key, secret_key):
        self.api_key = api_key
        self.secret_key = secret_key

    def __call__(self, request):
        timestamp = str(int(time.time()))
        message = timestamp + request.method + request.path_url + (request.body or '')
        signature = hmac.new(self.secret_key.encode('utf8'), message.encode('utf8'), hashlib.sha256).hexdigest()
        date = datetime.datetime.now()

        request.headers.update({
            'CB-ACCESS-SIGN': signature,
            'CB-ACCESS-TIMESTAMP': timestamp,
            'CB-ACCESS-KEY': self.api_key,
            'CB-VERSION': f"{date.year:04d}-{date.month:02d}-{date.day:02d}"
        })
        return request


class CoinbaseApi():
    def __init__(self, api_key, secret_key):
        self.api_url = 'https://api.coinbase.com/v2/'
        self.auth = CoinbaseWalletAuth(API_KEY, API_SECRET)

    def get_call(self, to_get:str):
        """
        Generic method to call the api with a specified parameter.
        Should only be used as private function.

        Fx:
        api_url = "https://api.coinbase.com/v2/"
        to_get  = "accounts"
        This will return a json object of all a accounts/crypto-coins
        for the user.

        ...
        Parameters
        to_get : str
            The endpoint to get.
            Fx. user, accounts, prices
            (https://developers.coinbase.com/api/v2/)
        """
        r = requests.get(self.api_url + to_get, auth=self.auth)
        if my_debug.is_debug:
            print(self.api_url + to_get)
        return r.json()

    def get_balance(self):
        coins = []
        r = self.get_call('accounts')
        data_arr = r['data']
        for data in data_arr:
            if (float)(data['balance']['amount']) > 0.0:
                pprint(data)
                coins.append(data)
            # if data['balance']['amount'] != 0:
            #     coins.append(data)
            #     print(data['name'])
        #pprint(data)


if __name__ == '__main__':
    coinbase = CoinbaseApi(API_KEY, API_SECRET)
    coinbase.get_balance()

# api_url = 'https://api.coinbase.com/v2/'
# auth = CoinbaseWalletAuth(API_KEY, API_SECRET)

# r = requests.get(api_url + 'user', auth=auth)
# print(r.json())