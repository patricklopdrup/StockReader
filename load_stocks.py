import nordnet
import saxo
import stock
import payout_freq
import dividend
import re
from datetime import date
from pprint import pprint
import my_debug

payout = payout_freq.Payout_freq()
if not my_debug.is_debug:
    nordnet = nordnet.Nordnet()
    saxo = saxo.Saxo()


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
            frequencies[i] = payout.get_frequency(symbols[i])
    return frequencies


def load_payout_dates(stock_amount, currencies, symbols):
    payout_dates = [date.min] * stock_amount
    for i in range(stock_amount):
        if currencies[i].lower() == 'usd':
            print(f'Her: {symbols[i]}')
            payout_dates[i] = payout.get_next_payout_date(symbols[i])
    return payout_dates


def get_all_stocks():
    ''' Returns a list of all stocks '''
    nordnet_list = get_nordnet_stocks()
    saxo_list = get_saxo_stocks()
    return nordnet_list + saxo_list


def get_nordnet_stocks():
    # Nordnet
    stocks = []
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

    for i in range(stock_amount):
        stocks.append(stock.Stock(names[i], symbols[i], shares[i], costs[i], market_values[i], dividends[i],
                                  frequencies[i], payout_dates[i], sectors[i], currencies[i], conversion_rates[i], ids[i], broker))
    return stocks


def get_saxo_stocks():
    # Saxo
    stocks = []
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
    # hej = stock.Stock.test_stock()
    # print(f'sector: {hej.sector}')
    # print(f'freq: {hej.freq_as_num()}')
    # print(hej.get_row())
    

    # hej = get_nordnet_stocks()
    hej = get_saxo_stocks()
    # hej = get_all_stocks()
    pprint(hej)
    # print()
    # hej.sort(key=lambda x: x.payout_date)
    # pprint(hej)