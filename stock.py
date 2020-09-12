import requests
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
    currency = ''
    conversion_rate = 0
    total_cost = 0
    broker = ''
    stock_id = 0

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

    def convert_all_to_dkk(self):
        rate = self.conversion_rate
        self.cost *= rate
        self.market_value *= rate
        self.dividend *= rate
        self.value *= rate
        self.total_cost *= rate
        self.profit *= rate
        self.div_exp *= rate
    
    def cost_in_dkk(self):
        return self.cost * self.conversion_rate

    def market_value_in_dkk(self):
        return self.market_value * self.conversion_rate

    def dividend_in_dkk(self):
        return self.dividend * self.conversion_rate

    def value_in_dkk(self):
        return self.value * self.conversion_rate

    def total_cost_in_dkk(self):
        return self.total_cost * self.conversion_rate

    def profit_in_dkk(self):
        return self.profit * self.conversion_rate

    def div_exp_in_dkk(self):
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
        
    @classmethod
    def test_stock(self):
        return Stock('Coca-Cola', 'KO', 3.0, 47.44, 50.65, 1.64, 'quarterly', date(2020,10,1), {'Sector': 'Consumer Defensive', 'SubSector': 'Beverages - Non-Alcoholic'}, 'USD', 6.2807, 307, 'saxo')

