import requests
import stock
from pprint import pprint
from datetime import datetime
from datetime import date

class Payout_freq():
    frequency = {
        'annual': 1,
        'semiannual': 2,
        'quarterly': 4,
        'monthly': 12
    }

    is_first_time = True
    token = ''
    token_userid = ''

    def __init__(self):
        ''' Get tokens once with random symbol (AT&T here) '''
        self.get_token('T')

    def get_next_payout_date(self, symbol):
        ''' Returns the next payout date for the stock '''
        try:
            return self.get_pay_date_upcoming(symbol)
        except:
            # If there is no last paydate it crashes and we calc outself
            try:
                # Find frequency and date from last payout date and calc
                last_freq = self.get_frequency_last(symbol)
                last_pay_date = self.get_pay_date_last(symbol)
                return self.calc_next_exp_pay_date(last_pay_date, last_freq)
            except:
                return date.min
        return date.min


    def get_frequency(self, symbol):
        try:
            return self.get_frequency_upcoming(symbol)
        except:
            try:
                return self.get_frequency_last(symbol)
            except:
                return 0
        return 0


    def calc_next_exp_pay_date(self, last_pay_date, freq):
        month_offset = 12 // self.frequency[freq]
        next_pay_date_month = last_pay_date.month + month_offset
        next_pay_date_year = last_pay_date.year
        if next_pay_date_month > 12:
            next_pay_date_month %= 12
            next_pay_date_year += 1
        return date(next_pay_date_year, next_pay_date_month, 1)


    def get_upcoming_dividend(self, symbol):
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


    def get_token(self, symbol):
        ''' Tokens used to find last payout date '''
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
        self.token = json['_token']
        self.token_userid = json['_token_userid']


    def get_last_dividend(self, symbol):
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
            '_token': self.token,
            '_token_userid': self.token_userid
        }
        url = 'https://globalhistorical.xignite.com/v3/xGlobalHistorical.json/GetCashDividendHistory'
        r = requests.get(url, params=params)
        json = r.json()
        return json['CashDividends'][0]


    # Get frequency from upcoming dividend
    def get_frequency_upcoming(self, symbol):
        json = self.get_upcoming_dividend(symbol)
        return json['data'][0]['frequency'].lower()


    # Get frequency from last dividend
    def get_frequency_last(self, symbol):
        json = self.get_last_dividend(symbol)
        return json['PaymentFrequency'].lower()


    # Get pay date from upcoming dividend
    def get_pay_date_upcoming(self, symbol):
        json = self.get_upcoming_dividend(symbol)
        pay_date = json['data'][0]['pay_date']
        return date.fromisoformat(pay_date)


    # Get pay date from last dividend
    def get_pay_date_last(self, symbol):
        json = self.get_last_dividend(symbol)
        pay_date = json['PayDate']
        return date.fromisoformat(pay_date)


if __name__ == '__main__':
    payout = Payout_freq()
    hej = stock.Stock.test_stock()
    symbol = 'T'
    print('Next:')
    print(payout.get_next_payout_date(symbol))
