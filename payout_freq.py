import requests
from pprint import pprint
from datetime import datetime
from datetime import date

frequency = {
    'annual': 1,
    'semiannual': 2,
    'quarterly': 4,
    'monthly': 12
}


def get_next_payout_date(symbol):
    ''' Returns the next payout date for the stock '''
    pass


def get_upcoming_dividend(symbol):
    headers = {
        'authority': 'seekingalpha.com',
        'method': 'GET',
        'path': '/symbol/frt/dividends/upcoming_dividends',
        'scheme': 'https',
        'accept': '*/*',
        'accept-encoding': 'gzip, deflate, br',
        'accept-language': 'da,en;q=0.9,en-GB;q=0.8,en-US;q=0.7,sv;q=0.6',
        'referer': f'https://seekingalpha.com/symbol/{symbol}/dividends/scorecard',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.83 Safari/537.36 Edg/85.0.564.44'
    }

    url = f'https://seekingalpha.com/symbol/{symbol}/dividends/upcoming_dividends'
    r = requests.get(url, headers=headers)
    json = r.json()
    return json


def get_token():
    headers = {
        'authority': 'seekingalpha.com',
        'method': 'GET',
        'path': '/market_data/xignite_token',
        'scheme': 'https',
        'accept': '*/*',
        'accept-encoding': 'gzip, deflate, br',
        'accept-language': 'da,en;q=0.9,en-GB;q=0.8,en-US;q=0.7,sv;q=0.6',
        'referer': f'https://seekingalpha.com/symbol/{symbol}/dividends/scorecard?s={symbol}',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.83 Safari/537.36 Edg/85.0.564.44',
        'x-requested-with': 'XMLHttpRequest'
    }

    url = 'https://seekingalpha.com/market_data/xignite_token'
    r = requests.get(url, headers=headers)
    json = r.json()
    token = json['_token']
    token_userid = json['_token_userid']
    return (token, token_userid)


def get_last_dividend(symbol):
    tokens = get_token()
    token = tokens[0]
    token_userid = tokens[1]

    today = datetime.today()
    day = today.day
    month = today.month
    year = today.year + 1
    end_date = f'{month}/{day}/{year}'

    params = {
        'IdentifierType': 'Symbol',
        'Identifier': symbol,
        'StartDate': '01/01/2018',
        'EndDate': end_date,
        'IdentifierAsOfDate': '',
        'CorporateActionsAdjusted': 'true',
        '_token': token,
        '_token_userid': token_userid
    }
    url = 'https://globalhistorical.xignite.com/v3/xGlobalHistorical.json/GetCashDividendHistory'
    r = requests.get(url, params=params)
    json = r.json()
    return json['CashDividends'][0]

# Get frequency


def get_frequency_upcoming(symbol):
    json = get_upcoming_dividend(symbol)
    return json['data'][0]['frequency'].lower()


def get_frequency_last(symbol):
    json = get_last_dividend(symbol)
    return json['PaymentFrequency'].lower()

# Get pay date


def get_pay_date_upcoming(symbol):
    json = get_upcoming_dividend(symbol)
    return json['data'][0]['pay_date']


def get_pay_date_last(symbol):
    json = get_last_dividend(symbol)
    return json['PayDate']


if __name__ == '__main__':
    symbol = 'pfe'
    # print(get_pay_date(symbol))
    # last = get_last_dividend(symbol)
    # pprint(last)
    hej = get_pay_date_last(symbol)
    date = date.fromisoformat(hej)
    hej2 = get_pay_date_last('O')
    date2 = date.fromisoformat(hej2)
    print(date < date2)
    print(f'{date} < {date2}')
    print('-----')
    upcoming = get_upcoming_dividend(symbol)
    pprint(upcoming)
