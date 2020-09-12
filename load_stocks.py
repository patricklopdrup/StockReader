import nordnet
import saxo
import stock
import payout_freq
import dividend
import re


nordnet = nordnet.Nordnet()
saxo = saxo.Saxo()

stocks = []


def fix_names(names):
    new_names = []
    for name in names:
        if 'INDEX' in name:
            name = re.sub(r"(\s+)INDEX(\s+)", " ", name)
        new_names.append(name)
    return new_names


def load_dividends(stock_amount, symbols, names, is_index_fond):
    dividends = []
    for i in range(stock_amount):
        if is_index_fond[i]:
            dividends.append(dividend.get_index_fond_dividend(names[i]))
        else:
            dividends.append(dividend.get_dividend(symbols[i]))
    return dividends


def load_frequencies(stock_amount, currencies, symbols):
    frequencies = [''] * stock_amount
    for i in range(stock_amount):
        if currencies[i].lower() == 'usd':
            frequencies[i] = payout_freq.get_frequency(symbols[i])
    return frequencies


def load_payout_dates(stock_amount, currencies, symbols):
    payout_dates = [''] * stock_amount
    for i in range(stock_amount):
        if currencies[i].lower() == 'usd':
            payout_dates[i] = payout_freq.get_next_payout_date(symbols[i])
    return payout_dates


def get_stocks():
    get_nordnet_stocks()
    get_saxo_stocks()


def get_nordnet_stocks():
    # Nordnet
    stock_amount = nordnet.get_stock_amount()
    temp_names = nordnet.get_names()
    names = fix_names(temp_names)
    symbols = nordnet.get_symbols()
    shares = nordnet.get_share_amounts()
    costs = nordnet.get_costs()
    market_values = nordnet.get_market_prices()
    currencies = nordnet.get_currencies()
    conversion_rates = nordnet.get_conversion_rates()
    ids = nordnet.get_ids()
    sectors = nordnet.get_sectors()
    broker = 'nordnet'
    is_index_fond = nordnet.get_if_indexfond()

    dividends = load_dividends(stock_amount, symbols, names, is_index_fond)

    frequencies = load_frequencies(stock_amount, currencies, symbols)
    payout_dates = load_payout_dates(stock_amount, currencies, symbols)

    print(payout_dates)

    for i in range(stock_amount):
        stocks.append(stock.Stock(names[i], symbols[i], shares[i], costs[i], market_values[i], dividends[i],
                                  frequencies[i], payout_dates[i], sectors[i], currencies[i], conversion_rates[i], ids[i], broker))
    return stocks


def get_saxo_stocks():
    # Saxo
    stock_amount = saxo.get_stock_amount()
    names = saxo.get_names()
    symbols = saxo.get_symbols()
    shares = saxo.get_share_amounts()
    costs = saxo.get_costs()
    market_values = saxo.get_market_prices()
    currencies = saxo.get_currencies()
    conversion_rates = saxo.get_conversion_rates()
    ids = saxo.get_uics()
    broker = 'saxo'
    sectors = []
    is_index_fond = [False] * stock_amount
    for i in range(stock_amount):
        sectors.append(saxo.get_sector(ids[i]))

    dividends = load_dividends(stock_amount, symbols, names, is_index_fond)
    frequencies = load_frequencies(stock_amount, currencies, symbols)
    payout_dates = load_payout_dates(stock_amount, currencies, symbols)

    for i in range(stock_amount):
        stocks.append(stock.Stock(names[i], symbols[i], shares[i], costs[i], market_values[i], dividends[i],
                                  frequencies[i], payout_dates[i], sectors[i], currencies[i], conversion_rates[i], ids[i], broker))
    return stocks


if __name__ == '__main__':
    print(get_saxo_stocks())
