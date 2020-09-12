# Offset for rows in "stocks" worksheet
stock_offset = 3

def stock_header():
    ''' Header values in Google Sheets '''
    return [
        'Name',
        'Symbol',
        'Shares',
        'Cost',
        'Market value',
        'Value',
        'Profit',
        'Profit %',
        'Div/share',
        'Yield %',
        'Freq',
        'Div exp',
        'Sector'
    ]
