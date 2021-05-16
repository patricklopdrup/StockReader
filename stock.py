import requests
import payout_freq
from pprint import pprint
from datetime import datetime
from datetime import date


class Stock():
    name = ''
    symbol = ''
    shares = 0
    cost = 0
    market_value = 0
    value = 0
    profit = 0
    dividend = 0
    div_yield_pct = 0
    freq = 0
    div_exp = 0
    payout_date = date.today()
    sector = ''
    sub_sector = ''
    currency = ''
    conversion_rate = 0
    total_cost = 0
    profit_pct = 0
    broker = ''
    stock_id = 0

    __currency_prefix = {
        'usd': '$',
        'eur': '€',
        'dkk': 'kr.',
        'nok': 'nok',
        'sek': 'sek'
    }

    def __init__(self, name, symbol, shares, cost, market_value, dividend, freq, payout_date: datetime, sector, currency, conversion_rate, stock_id, broker):
        self.name = name
        self.symbol = symbol
        self.shares = shares
        self.cost = cost
        self.market_value = market_value
        self.dividend = dividend
        self.freq = freq
        self.payout_date = payout_date
        self.sector = sector
        self.currency = currency
        self.conversion_rate = conversion_rate
        self.stock_id = stock_id
        self.broker = broker

        self.value = shares * market_value
        self.total_cost = shares * cost
        self.profit = self.value - self.total_cost
        self.div_yield_pct = dividend / market_value
        self.div_exp = dividend * shares
        self.profit_pct = self.profit / self.total_cost

    def get_row(self):
        '''
        Row for the stock in Google Sheets.
        Matching the stock_header.
        '''
        return [
            self.name,
            self.symbol,
            self.shares,
            self.cost_dkk(),
            self.market_value_dkk(),
            self.value_dkk(),
            self.profit_dkk(),
            self.profit_pct,
            self.dividend_dkk(),
            self.div_yield_pct,
            self.freq_as_num(),
            self.div_exp_dkk(),
            self.sector
        ]

    def get_currency_prefix(self):
        return self.__currency_prefix[self.currency.lower()]

    def convert_all_to_dkk(self):
        rate = self.conversion_rate
        self.cost *= rate
        self.market_value *= rate
        self.dividend *= rate
        self.value *= rate
        self.total_cost *= rate
        self.profit *= rate
        self.div_exp *= rate

    def freq_as_num(self):
        try:
            if self.freq:
                return payout_freq.Payout_freq.frequency[self.freq]
            else:
                return ''
        except:
            return ''

    def cost_dkk(self):
        return self.cost * self.conversion_rate

    def market_value_dkk(self):
        return self.market_value * self.conversion_rate

    def dividend_dkk(self):
        return self.dividend * self.conversion_rate

    def value_dkk(self):
        return self.value * self.conversion_rate

    def total_cost_dkk(self):
        return self.total_cost * self.conversion_rate

    def profit_dkk(self):
        return self.profit * self.conversion_rate

    def div_exp_dkk(self):
        return self.div_exp * self.conversion_rate

    def __str__(self):
        return f'{self.name} ({self.symbol}): {self.market_value}. Div: {self.dividend}'

    def __repr__(self):
        return str(self)

    def print_all(self):
        print(f'Name: {self.name}')
        print(f'Symbol: {self.symbol}')
        print(f'Shares: {self.shares}')
        print(f'Cost: {self.cost}')
        print(f'Market value: {self.market_value}')
        print(f'Value: {self.value}')
        print(f'Profit: {self.profit}')
        print(f'Dividend: {self.dividend}')
        print(f'Div yield %: {self.div_yield_pct}')
        print(f'Freq: {self.freq}')
        print(f'Div exp: {self.div_exp}')
        print(f'Payout date: {self.payout_date}')
        print(f'Sector: {self.sector}')
        print(f'Currency: {self.currency}')
        print(f'Convertion rate: {self.conversion_rate}')
        print(f'Total cost: {self.total_cost}')
        print(f'Broker: {self.broker}')
        print(f'Stock id: {self.stock_id}')

    def print_as_obj(self):
        print(f'\'{self.name}\', \'{self.symbol}\', {self.shares}, {self.cost}, {self.market_value}, {self.dividend}, \'{self.freq}\', date({self.payout_date.year},{self.payout_date.month},{self.payout_date.day}), \'{self.sector}\', \'{self.currency}\', {self.conversion_rate}, {self.stock_id}, \'{self.broker}\'')

    @classmethod
    def test_stock(self):
        return Stock('Coca-Cola', 'KO', 3.0, 47.44, 50.65, 1.64, 'quarterly', date(2020, 10, 1), 'Consumer Defensive', 'USD', 6.2807, 307, 'saxo')

    @classmethod
    def test_data(self):
        return [
            Stock('Sparindex Emerging Markets KL', 'SPIEMIKL', 4.0, 124.19, 123.0,
                  1.9, '', date(1, 1, 1), 'Index fond', 'DKK', 1.0, 16102899, 'nordnet'),
            Stock('Sparindex Globale Aktier KL', 'SPVIGAKL', 18.0, 113.99444444444444,
                  113.55, 10.2, '', date(1, 1, 1), 'Index fond', 'DKK', 1.0, 16670431, 'nordnet'),
            Stock('Astralis Group A/S', 'ASTGRP', 60.0, 5.39, 4.77, 0, '',
                  date(1, 1, 1), 'Consumer Cyclical', 'DKK', 1.0, 17150971, 'nordnet'),
            Stock('Sparindex DJSI World KL', 'SPIDJWKL', 11.0, 163.38, 162.95, 4.6, '', date(
                1, 1, 1), 'Index fond', 'DKK', 1.0, 16099858, 'nordnet'),
            Stock('Sparindex Globale Akt Min Risk KL', 'SPIGLAMRIKL', 6.0, 137.45833333333334,
                  136.95, 6.4, '', date(1, 1, 1), 'Index fond', 'DKK', 1.0, 16100293, 'nordnet'),
            Stock('Coca-Cola', 'KO', 3.0, 47.44, 50.65, 1.64, 'quarterly',
                  date(2020, 10, 1), 'Consumer Defensive', 'USD', 6.283305, 307, 'saxo'),
            Stock('BMW', 'BMW', 2.0, 54.62, 64.37, 0, '', date(1, 1, 1),
                  'Consumer Cyclical', 'EUR', 7.44065, 117271, 'saxo'),
            Stock('Novo Nordisk', 'NOVOb', 4.0, 410.95, 419.15, 0, '',
                  date(1, 1, 1), 'Healthcare', 'DKK', 1.0, 15629, 'saxo'),
            Stock('SAS', 'SAS', 180.0, 5.63, 4.644, 0, '', date(
                1, 1, 1), 'Industrials', 'DKK', 1.0, 5901, 'saxo'),
            Stock('Simon Property Grp', 'SPG', 8.0, 61.505, 64.14, 5.2, 'quarterly', date(
                2020, 10, 1), 'Real Estate', 'USD', 6.283305, 3957, 'saxo'),
            Stock('AT&T', 'T', 9.0, 29.807111111111112, 29.0, 2.08, 'quarterly', date(
                2020, 11, 1), 'Communication Services', 'USD', 6.283305, 303, 'saxo'),
            Stock('Maersk Drilling', 'DRLCO', 10.0, 154.0, 137.2, 0, '',
                  date(1, 1, 1), 'Energy', 'DKK', 1.0, 13456564, 'saxo'),
            Stock('Nikola', 'NKLA', 5.0, 42.0, 32.14, 0, '0', date(1, 1, 1),
                  'Consumer Cyclical', 'USD', 6.283305, 17854349, 'saxo'),
            Stock('Vale', 'VALE', 20.0, 11.065, 11.67, 0.222, 'semiannual', date(
                2021, 2, 1), 'Basic Materials', 'USD', 6.283305, 37840, 'saxo'),
            Stock('Exxon Mobil', 'XOM', 9.0, 39.888888888888886, 36.9, 3.48, 'quarterly', date(
                2020, 12, 1), 'Energy', 'USD', 6.283305, 311, 'saxo'),
            Stock('Apple', 'AAPL', 4.0, 128.7775, 112.01, 0.82, 'quarterly', date(
                2020, 11, 1), 'Technology', 'USD', 6.283305, 211, 'saxo'),
            Stock('Main Street Cap', 'MAIN', 8.0, 29.9, 30.28, 2.46, 'monthly', date(
                2020, 10, 15), 'Financial Services', 'USD', 6.283305, 48957, 'saxo'),
            Stock('Chimera Invt', 'CIM', 20.0, 8.7, 8.6, 1.2, 'quarterly', date(
                2020, 10, 1), 'Real Estate', 'USD', 6.283305, 30721, 'saxo'),
            Stock('NVIDIA', 'NVDA', 1.0, 572.0, 486.7, 0.64, 'quarterly', date(
                2020, 9, 24), 'Technology', 'USD', 6.283305, 1249, 'saxo'),
            Stock('Pembina Pipeline', 'PBA', 7.0, 23.807142857142857, 23.75, 1.931,
                  'monthly', date(2020, 9, 15), 'Energy', 'USD', 6.283305, 1132835, 'saxo'),
            Stock('Cronos Group', 'CRON', 11.0, 5.25, 5.22, 0, '0', date(
                1, 1, 1), 'Healthcare', 'USD', 6.283305, 9140177, 'saxo'),
            Stock('Fed Rlty Inv Tr', 'FRT', 6.0, 76.4, 77.12, 4.24, 'quarterly', date(
                2020, 10, 15), 'Real Estate', 'USD', 6.283305, 44575, 'saxo'),
        ]
