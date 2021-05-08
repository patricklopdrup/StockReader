import payout_freq
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import load_stocks
import sheet_header

scope = ['https://spreadsheets.google.com/feeds',
         'https://www.googleapis.com/auth/drive']
creds = ServiceAccountCredentials.from_json_keyfile_name(
    'client_secret.json', scope)
client = gspread.authorize(creds)

sheet = client.open('Aktier').sheet1

def get_row_end_letter(columns):
    return chr(ord('A')+(columns)-1)

def update_header():
    # Get start row
    offset = sheet_header.stock_offset
    # Get headers to place
    headers = sheet_header.stock_header()
    # Get second letter (end of row)
    second_letter = get_row_end_letter(len(headers))
    cell_list = sheet.range(f'A{offset}:{second_letter}{offset}')
    for i, cell in enumerate(cell_list):
        cell.value = headers[i]
    # Update the whole row
    sheet.update_cells(cell_list)

def update_stocks():
    update_header()

    all_stocks = load_stocks.get_all_stocks()
    print("All stocks loaded")
    # Start right below header
    start_row = sheet_header.stock_offset + 1
    for i, stock in enumerate(all_stocks):
        # Row with values for the stock
        row = stock.get_row()
        # Create range for each row
        second_letter = get_row_end_letter(len(row))
        # Update cur_row for each iteration
        cur_row = start_row + i
        cell_list = sheet.range(f'A{cur_row}:{second_letter}{cur_row}')

        # Add a value to each cell in the row
        for j, cell in enumerate(cell_list):
            cell.value = row[j]

        # Update in batch
        sheet.update_cells(cell_list)

    print(f'Updated {len(all_stocks)} stocks')

    
    
if __name__ == '__main__':
    update_stocks()