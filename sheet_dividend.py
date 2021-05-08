import payout_freq
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from datetime import date
from pprint import pprint
import load_stocks
import stock

scope = ['https://spreadsheets.google.com/feeds',
         'https://www.googleapis.com/auth/drive']
creds = ServiceAccountCredentials.from_json_keyfile_name(
    'client_secret.json', scope)
client = gspread.authorize(creds)

sheet = client.open('Aktier').get_worksheet(2)


sheet.update_cell(15, 2, "hej")


month_dict = {
    1: 'Jan',
    2: 'Feb',
    3: 'Mar',
    4: 'April',
    5: 'May',
    6: 'June',
    7: 'July',
    8: 'Aug',
    9: 'Sep',
    10: 'Oct',
    11: 'Nov',
    12: 'Dec'
}


def get_next_12_months():
    today = date.today()
    dates = []
    for i in range(12):
        cur_month = today.month + i
        cur_year = today.year
        # Start next year if cur_month > 12
        if cur_month > 12:
            cur_month -= 12
            cur_year += 1
        dates.append(date(cur_year, cur_month, 1))
    return dates


def get_dividend_per_month(all_stocks):
    div_per_month = [0] * 12
    div_stocks = get_dividend_stocks(all_stocks)
    upcoming_year = get_next_12_months()
    for stock in div_stocks:
        for i, date in enumerate(upcoming_year):
            if stock.payout_date.year == date.year and stock.payout_date.month == date.month:
                div_per_month[i] += stock.dividend_dkk() / stock.freq_as_num()
    return div_per_month


def get_dividend_stocks(all_stocks):
    ''' Return all stocks with a payout_date year > than default 1 for non-paying dividend stocks '''
    return [x for x in all_stocks if x.payout_date.year > 1]


if __name__ == '__main__':
    stocks = stock.Stock.test_data()

    pprint(get_dividend_stocks(stocks))

    print()

    pprint(get_dividend_per_month(stocks))
