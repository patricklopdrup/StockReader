import requests
from pprint import pprint

def get_dividend_nasdaq(symbol):
    # Make header
    headers = {
        "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.106 Safari/537.36",
        'authority': 'api.nasdaq.com',
        'accept': 'application/json, text/plain, */*',
        'method': 'GET',
        'scheme': 'https',
        'accept-encoding': 'gzip, deflate, br',
        'accept-language': 'da,en;q=0.9,en-GB;q=0.8,en-US;q=0.7,sv;q=0.6',
        'origin': 'https://www.nasdaq.com',
        'referer': f'https://www.nasdaq.com/market-activity/stocks/{symbol}/dividend-history',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-site'
    }
    params = {
        'assetclass': 'stocks'
    }
    url = f'https://api.nasdaq.com/api/quote/{symbol}/dividends'

    r = requests.get(url, headers=headers, params=params, timeout=5)
    json = r.json()
    annualized_dividend = json['data']['annualizedDividend']
    if annualized_dividend == 'N/A':
        return 0
    return float(annualized_dividend)

def get_dividend_seekingalpha(symbol):
    pass