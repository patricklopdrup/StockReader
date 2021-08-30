import requests, hmac, hashlib, time, json, creds
from urllib.parse import urlencode
from pprint import pprint

API_KEY = creds.binance_api_key
API_SECRET = creds.binance_api_secret


class Binance():
    api_url = 'https://api.binance.com/'

    def __init__(self, api_key, secret_key):
        self.api_key = api_key
        self.secret_key = secret_key

    def hashing(self, query_string):
        return hmac.new(self.secret_key.encode('utf8'), query_string.encode('utf8'), hashlib.sha256).hexdigest()

    def get_timestamp(self):
        '''
        Return the local time minus the diff between
        local time and server time.
        '''
        server_time = (int)(b.api_call("api/v3/time")['serverTime'])
        my_time = int(time.time() * 1000)
        diff = my_time - server_time
        t = my_time - diff
        return t

    def request_type(self, http_method):
        session = requests.Session()
        session.headers.update({
            'Content-Type': 'application/json;charset=utf-8',
            'X-MBX-APIKEY': self.api_key
        })
        return {
            'GET': session.get,
            'DELETE': session.delete,
            'PUT': session.put,
            'POST': session.post,
        }.get(http_method, 'GET')

    def send_signed_request(self, http_method, url_path, payload={}):
        query_string = urlencode(payload, True)
        if query_string:
            query_string = f"{query_string}&timestamp={self.get_timestamp()}"
        else:
            query_string = f"timestamp={self.get_timestamp()}"

        url = self.api_url + url_path + '?' + query_string + '&signature=' + self.hashing(query_string)
        params = {'url': url, 'params': {}}
        response = self.request_type(http_method)(**params)
        return response.json()


    def api_call(self, endpoint: str, body: str = "", symbol = []):
        if body:
            r = requests.post(self.api_url + endpoint, data = body)
        elif symbol:
            if len(symbol) == 1:
                endpoint += f"?symbol={symbol[0]}"
            else:
                endpoint += "?symbols=["
                # Add all symbols
                for sym in symbol:
                    endpoint += sym + ","
                endpoint.replace(endpoint[-1], ']')
            r = requests.post(self.api_url + endpoint)
        else:
            r = requests.get(self.api_url + endpoint)
        print(r.url)
        return r.json()


if __name__ == '__main__':
    b = Binance(API_KEY, API_SECRET)
    #server_time = b.api_call("api/v3/time")
    test = b.send_signed_request('GET', 'api/v3/account')

    #test2 = b.api_call('api/v3/exchangeInfo', symbol=["BNBBTC"])
    test2 = b.api_call('api/v3/exchangeInfo?symbol=BNBBTC')
    #test2 = b.send_signed_request('GET', 'api/v3/exchangeInfo')
    pprint(test2)

    # wallets = []
    # balances = test['balances']
    # for b in balances:
    #     if (float)(b['free']) > 0.0:
    #         wallets.append(b)

    # pprint(wallets)