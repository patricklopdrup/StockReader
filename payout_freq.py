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
    try:
        return get_pay_date_upcoming(symbol)
    except:
        # If there is no last paydate it crashes and we calc outself
        try:
            last_freq = get_frequency_last(symbol)
            last_pay_date = get_pay_date_last(symbol)
            return calc_next_exp_pay_date(last_pay_date, last_freq)
        except:
            return 0
    return 0


def calc_next_exp_pay_date(last_pay_date, freq):
    month_offset = 12 // frequency[freq]
    next_pay_date_month = last_pay_date.month + month_offset
    next_pay_date_year = last_pay_date.year
    if next_pay_date_month > 12:
        next_pay_date_month %= 12
        next_pay_date_year += 1
    return date(next_pay_date_year, next_pay_date_month, 1)


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

    # Creating an enddate that looks like the one the website uses
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


# Get frequency from upcoming dividend
def get_frequency_upcoming(symbol):
    json = get_upcoming_dividend(symbol)
    return json['data'][0]['frequency'].lower()


# Get frequency from last dividend
def get_frequency_last(symbol):
    json = get_last_dividend(symbol)
    return json['PaymentFrequency'].lower()


# Get pay date from upcoming dividend
def get_pay_date_upcoming(symbol):
    json = get_upcoming_dividend(symbol)
    pay_date = json['data'][0]['pay_date']
    return date.fromisoformat(pay_date)


# Get pay date from last dividend
def get_pay_date_last(symbol):
    json = get_last_dividend(symbol)
    pay_date = json['PayDate']
    return date.fromisoformat(pay_date)


if __name__ == '__main__':
    symbol = 'aapl'
    hej = get_pay_date_last(symbol)
    print(hej)
    print(get_next_payout_date('aapl'))
