import requests
import os
import creds
from datetime import datetime
from datetime import date
from pprint import pprint


class nordnet():

    # Hardcoded sectors because Nordnet returns in danish
    sector_dict = {
        'ASTGRP': 'Consumer Cyclical'
    }

    cookies = {}
    portfolio = []

    def __init__(self):
        self.login()
        self.portfolio = self.get_portfolio_info()

    #
    # Mostly taken from Morten Helmstedt: https://helmstedt.dk/2019/01/saadan-traekker-du-dine-transaktioner-ud-fra-nordnet-med-python/ 
    #

    def login(self):
        # First part of cookie setting prior to login
        url = 'https://www.nordnet.dk/mux/login/start.html?cmpi=start-loggain&state=signin'
        r = requests.get(url)

        self.cookies['LOL'] = r.cookies['LOL']
        self.cookies['TUX-COOKIE'] = r.cookies['TUX-COOKIE']

        # Second part of cookie setting prior to login
        url = 'https://classic.nordnet.dk/api/2/login/anonymous'
        r = requests.post(url, cookies=self.cookies)
        self.cookies['NOW'] = r.cookies['NOW']

        # Actual login that gets us cookies required for primary account extraction
        url = "https://classic.nordnet.dk/api/2/authentication/basic/login"
        r = requests.post(url, cookies=self.cookies, data={
            'username': creds.nordnet_username, 'password': creds.nordnet_password})
        self.cookies['NOW'] = r.cookies['NOW']
        self.cookies['xsrf'] = r.cookies['xsrf']
        self.cookies['NN-JWT'] = r.cookies['NN-JWT']

    def get_portfolio_info(self):
        url = "https://classic.nordnet.dk/oauth2/authorize?client_id=NEXT&response_type=code&redirect_uri=https%3A%2F%2Fwww.nordnet.dk%2Foauth2%2F&b=1"
        r = requests.get(url, cookies=self.cookies, allow_redirects=False)
        getNextUrl = r.headers["Location"]

        # Get NEXT from a redirectet URL. (from Location in header)
        r = requests.get(getNextUrl, cookies=self.cookies,
                         allow_redirects=False)
        self.cookies['NEXT'] = r.cookies['NEXT']

        # Add payload and headers to get portfolio data
        payload = {"batch": "[{\"relative_url\":\"indicators/201:172.10.OMXC25GI,201:172.10.OMXC25,201:172.10.OMXC20CAP,201:170.10.OMXS30,201:170.10.OMXSPI,201:174.10.OSEBX,201:174.10.OBX,201:176.10.OMXH25,201:176.10.OMXHPI,201:170.10.OMXN40,201:170.10.FN25,201:75.3.@ES0Y,201:29.10.NDX,201:29.10.@CCO,201:213.10.DAX,201:30.10.!W1DOW\",\"method\":\"GET\"},{\"relative_url\":\"accounts/1/ledgers\",\"method\":\"GET\"},{\"relative_url\":\"accounts/1/bank_account_info\",\"method\":\"GET\"},{\"relative_url\":\"banking/1/lending/info_extended\",\"method\":\"GET\"},{\"relative_url\":\"accounts/1/yield_tax/upcoming_transaction\",\"method\":\"GET\"},{\"relative_url\":\"accounts/1/positions?include_instrument_loans=true\",\"method\":\"GET\"}]"}
        headers = {'client-id': 'NEXT', 'ntag': self.cookies['xsrf']}

        # Get portfolio info
        url = "https://www.nordnet.dk/api/2/batch"
        r = requests.post(url, cookies=self.cookies,
                          data=payload, headers=headers)

        # Portfolio info as json
        json = r.json()
        # Return my data from json
        return json[5]['body']

    def get_single_stock_info(self, instrument_id):
        ''' TODO: does not work '''
        url = "https://classic.nordnet.dk/oauth2/authorize?client_id=NEXT&response_type=code&redirect_uri=https%3A%2F%2Fwww.nordnet.dk%2Foauth2%2F&b=1"
        r = requests.get(url, cookies=self.cookies, allow_redirects=False)
        getNextUrl = r.headers["Location"]

        # Get NEXT from a redirectet URL. (from Location in header)
        r = requests.get(getNextUrl, cookies=self.cookies,
                         allow_redirects=False)
        self.cookies['NEXT'] = r.cookies['NEXT']

        payload = {'[{"relative_url":"company_data/keyfigures/17150971","method":"GET"},{"relative_url":"company_data/yearlyfinancial/17150971","method":"GET"},{"relative_url":"company_data/summary/17150971","method":"GET"},{"relative_url":"instruments/17150971/fund/info","method":"GET"},{"relative_url":"user/settings/uitheme","method":"GET"},{"relative_url":"instruments/historical/prices/17150971?fields=open,high,low,last,volume&from=2020-08-29","method":"GET"},{"relative_url":"accounts/1/messages?mailbox=INBOX","method":"GET"}]'}
        headers = {'client-id': 'NEXT', 'ntag': self.cookies['xsrf']}

        url = 'https://www.nordnet.dk/api/2/batch'
        r = requests.post(url, cookies=self.cookies,
                          data=payload, headers=headers)
        # pprint(r.json())

    def get_stock_amount(self):
        return len(self.portfolio)

    #
    # Get arrays of data
    #
    def get_symbols(self):
        symbols = []
        for i in self.portfolio:
            symbols.append(i['instrument']['symbol'])
        return symbols

    def get_names(self):
        names = []
        for i in self.portfolio:
            names.append(i['instrument']['name'])
        return names

    def get_costs(self):
        costs = []
        for i in self.portfolio:
            costs.append(i['acq_price']['value'])
        return costs

    def get_share_amounts(self):
        shares = []
        for i in self.portfolio:
            shares.append(i['qty'])
        return shares

    def get_market_prices(self):
        prices = []
        for i in self.portfolio:
            prices.append(i['main_market_price']['value'])
        return prices

    def get_currencies(self):
        currencies = []
        for i in self.portfolio:
            currencies.append(i['instrument']['currency'])
        return currencies

    def get_asset_classes(self):
        asset_classes = []
        for i in self.portfolio:
            asset_classes.append(i['instrument']['asset_class'])
        return asset_classes

    def get_if_indexfond(self):
        is_index = []
        for i in self.portfolio:
            try:
                # If stock has an institute it is an indexfond
                institute = i['instrument']['institute']
                is_index.append(True)
            except:
                is_index.append(False)
        return is_index

    def get_sectors(self):
        sectors = []
        if_indexfond = self.get_if_indexfond()
        symbols = self.get_symbols()
        for i, val in enumerate(if_indexfond):
            if val:
                sectors.append('Index fond')
            else:
                sectors.append(self.sector_dict[symbols[i]])
        return sectors

    #
    # Get single data via symbol
    #
    def get_index_in_portfolio(self, symbol):
        for i, val in enumerate(self.portfolio):
            sym = val['instrument']['symbol']
            if symbol == sym:
                return i

    def get_name(self, symbol):
        index = self.get_index_in_portfolio(symbol)
        return self.portfolio[index]['instrument']['name']

    def get_cost(self, symbol):
        index = self.get_index_in_portfolio(symbol)
        return self.portfolio[index]['acq_price']['value']

    def get_share_amount(self, symbol):
        index = self.get_index_in_portfolio(symbol)
        return self.portfolio[index]['qty']

    def get_market_price(self, symbol):
        index = self.get_index_in_portfolio(symbol)
        return self.portfolio[index]['main_market_price']['value']

    def get_currency(self, symbol):
        index = self.get_index_in_portfolio(symbol)
        return self.portfolio[index]['instrument']['currency']

    def get_asset_class(self, symbol):
        index = self.get_index_in_portfolio(symbol)
        return self.portfolio[index]['instrument']['asset_class']


if __name__ == '__main__':
    hej = nordnet()
    print(hej.get_sectors())
    # instrument_id = 17150971
    # hej.get_single_stock_info(instrument_id)
