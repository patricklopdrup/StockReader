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
        self.cost = cost * conversion_rate
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

    def __str__(self):
        return f'{self.name} ({self.symbol}): {self.market_value}. Div: {self.dividend}'

    def __repr__(self):
        return str(self)

    def calc_value(self, shares, market_value):
        return shares * market_value
