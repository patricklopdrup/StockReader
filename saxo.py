import requests
import json
import creds
from datetime import datetime
from datetime import date
from bs4 import BeautifulSoup
from pprint import pprint


class Saxo():
    portfolio = []
    bearer = ''
    clientkey = ''
    headers = {}

    # Saxo user account credentials
    user = creds.saxo_username
    password = creds.saxo_password

    def __init__(self):
        self.login()
        self.portfolio = self.get_portfolio_info()

    #
    # Mostly taken from Morten Helmstedt: https://helmstedt.dk/2019/05/saadan-traekker-du-dine-data-ud-fra-saxo-bank-med-python/
    #

    def login(self):
        # LOGIN TO SAXO BANK

        # Visit login page and get AuthnRequest token value from input form
        url = 'https://www.saxoinvestor.dk/Login/da/'
        r = requests.get(url)

        soup = BeautifulSoup(r.text, "html.parser")
        input = soup.find_all('input', {"id": "AuthnRequest"})
        authnrequest = input[0]["value"]

        # Login step 1: Submit username, password and token and get another token back
        url = 'https://www.saxoinvestor.dk/Login/da/'
        r = requests.post(url, data={
            'field_userid': self.user, 'field_password': self.password, 'AuthnRequest': authnrequest})

        soup = BeautifulSoup(r.text, "html.parser")
        input = soup.find_all('input', {"name": "SAMLResponse"})
        # Most of the time this works
        if input:
            samlresponse = input[0]["value"]
        # But sometimes there's a disclaimer that Saxo Bank would like you to accept
        else:
            input = soup.find_all('input')
            inputs = {}
            try:
                for i in input:
                    inputs[i['name']] = i['value']
            except:
                pass
            url = 'https://www.saxotrader.com/disclaimer'
            request = requests.post(url, data=inputs)
            cook = request.cookies['DisclaimerApp']
            returnurl = cook[cook.find(
                "ReturnUrl")+10:cook.find("&IsClientStation")]
            url = 'https://live.logonvalidation.net/complete-app-consent/' + \
                returnurl[returnurl.find("complete-app-consent/")+21:]
            request = requests.get(url)
            soup = BeautifulSoup(request.text, "html.parser")
            input = soup.find_all('input', {"name": "SAMLResponse"})
            samlresponse = input[0]["value"]

        # Login step 2: Get bearer token necessary for API requests
        url = 'https://www.saxoinvestor.dk/investor/login.sso.ashx'
        r = requests.post(url, data={'SAMLResponse': samlresponse})
        print(f'login: {r}')

        self.bearer = r.history[0].headers['Location']
        self.bearer = self.bearer[self.bearer.find(
            "BEARER"):self.bearer.find("/exp/")]
        self.bearer = self.bearer.replace("%20", " ")

    def get_portfolio_info(self):
        # START API CALLS

        # Set bearer token as header
        self.headers = {'Authorization': self.bearer}

        # First API request gets Client Key which is used for most API calls
        # See https://www.developer.saxo/openapi/learn/the-tutorial for expected return data
        url = 'https://www.saxoinvestor.dk/openapi/port/v1/clients/me'
        r = requests.get(url, headers=self.headers)

        clientdata = r.json()
        self.clientkey = clientdata['ClientKey']

        # Get my stocks
        url = 'https://www.saxoinvestor.dk/openapi/port/v1/netpositions/me/'
        r = requests.get(url, headers=self.headers)
        json = r.json()
        # pprint(json)
        return json['Data']

    def get_stock_amount(self):
        return len(self.portfolio)

    #
    # Get arrays of data
    #
    def get_symbols(self):
        symbols = []
        for i in self.portfolio:
            temp_sym = i['NetPositionId']
            symbols.append(temp_sym.split(':')[0])
        return symbols

    def get_names(self):
        names = []
        for i in self.portfolio:
            names.append(i['NetPositionBase']['IssuerName'])
        return names

    def get_costs(self):
        costs = []
        for i in self.portfolio:
            costs.append(i['NetPositionView']['AverageOpenPrice'])
        return costs

    def get_share_amounts(self):
        shares = []
        for i in self.portfolio:
            shares.append(i['NetPositionBase']['Amount'])
        return shares

    def get_market_prices(self):
        prices = []
        for i in self.portfolio:
            prices.append(i['NetPositionView']['CurrentPrice'])
        return prices

    def get_currencies(self):
        currencies = []
        for i in self.portfolio:
            currencies.append(i['NetPositionView']['ExposureCurrency'])
        return currencies

    def get_conversion_rates(self):
        rates = []
        for i in self.portfolio:
            rates.append(i['NetPositionView']['ConversionRateCurrent'])
        return rates

    def get_asset_classes(self):
        asset_classes = []
        for i in self.portfolio:
            asset_classes.append(i['NetPositionBase']['AssetType'])
        return asset_classes

    def get_uics(self):
        uics = []
        for i in self.portfolio:
            uics.append(i['NetPositionBase']['Uic'])
        return uics

    #
    # Data for one stock
    #
    def get_sector(self, uic):
        ''' Returns a dict with 'Sector' and 'SubSector' '''
        url = f'https://www.saxoinvestor.dk/openapi/mkt/v1/marketdata/Stock/{uic}/?FieldGroups=GeneralInfo'
        r = requests.get(url, headers=self.headers)
        json = r.json()
        # Pull sector and sebsector out of json
        sector = json['GeneralInfo']['StockInfo']['Sector']['Key']
        sub_sector = json['GeneralInfo']['StockInfo']['SubSector']['Key']
        # Return sector
        # TODO return sub sector only for saxo
        return sector

    def get_div_yield_pct(self, uic):
        url = f'https://www.saxoinvestor.dk/openapi/mkt/v1/marketdata/Stock/{uic}/?FieldGroups=GeneralInfo'
        r = requests.get(url, headers=self.headers)
        json = r.json()
        # Return the div yield pct if the stock pays dividend
        try:
            return json['GeneralInfo']['StockInfo']['DividentYieldPct']
        except:
            return 0.0


if __name__ == '__main__':
    saxo = saxo()
    saxo.load_data()
    print(saxo.get_uics())
    print(saxo.get_sector(117271))
