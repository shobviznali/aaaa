from __future__ import print_function
import os.path
import pickle
import datetime
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from dateutil.parser import parse


class GoogleSheet:
    SPREADSHEET_ID = '1KEzZcQyyj70n47TtkH9DVfqp-WuTqn6LNtJjKczhFXk'
    SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
    service = None

    def __init__(self):
        creds = None
        if os.path.exists('token.pickle'):
            with open('token.pickle', 'rb') as token:
                creds = pickle.load(token)

        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    'creds.json', self.SCOPES)
                creds = flow.run_local_server(port=0)
            with open('token.pickle', 'wb') as token:
                pickle.dump(creds, token)

        self.service = build('sheets', 'v4', credentials=creds)

    def add_username(self, username):
        name_range = 'B1:Z1'  # Assuming names are in the range of columns B to Z in row 1 (adjust as needed)

        name_values = self.service.spreadsheets().values().get(
            spreadsheetId=self.SPREADSHEET_ID,
            range=name_range
        ).execute().get('values', [])

        if len(name_values) > 0:
            next_column = chr(ord('B') + len(name_values[0]))
        else:
            next_column = 'B'

        self._update_values(next_column + '2', [[username]])

    def add_id(self, user_id):
        name_range = 'B2:Z2'  # Assuming names are in the range of columns B to Z in row 2 (adjust as needed)

        name_values = self.service.spreadsheets().values().get(
            spreadsheetId=self.SPREADSHEET_ID,
            range=name_range
        ).execute().get('values', [])

        if len(name_values) > 0:
            next_column = chr(ord('B') + len(name_values[0]))
        else:
            next_column = 'B'

        self._update_values(next_column + '2', [[user_id]])

    from dateutil.parser import parse as parse_date

    from dateutil.parser import parse as parse_date

    def find_and_write_name(self, name_to_find, text_to_put):
        date_range = 'A3:A'  # Assuming dates are in column A starting from row 3 (adjust as needed)

        existing_dates = self.service.spreadsheets().values().get(
            spreadsheetId=self.SPREADSHEET_ID,
            range=date_range
        ).execute().get('values', [])

        existing_dates = [parse(date[0]).date() for date in existing_dates if date and date[0]]
        today = datetime.date.today()

        # Extract the date from text_to_put using a regular expression
        import re
        date_string = re.search(r'\b\d{1,2}\.\d{1,2}\.\d{2}\b', text_to_put)
        if date_string:
            parsed_date = parse(date_string.group(), dayfirst=True).date()
        else:
            parsed_date = today  # Use today's date if no valid date found in text_to_put

        # Check if the parsed date is not already present in the date_range
        if parsed_date not in existing_dates:
            # Find the last existing date and its row number
            last_date = existing_dates[-1] if existing_dates else today
            last_date_row = existing_dates.index(last_date) + 3 if last_date in existing_dates else 3

            # Insert a blank row below the last date
            self._insert_blank_row(last_date_row + 1)

            # Write the parsed date in the newly inserted row
            self._update_values('A{}'.format(last_date_row + 2), [[parsed_date.strftime("%Y-%m-%d")]])

            existing_dates.append(parsed_date)  # Add the parsed date to the existing_dates list

        # Rest of the method remains unchanged
        name_range = 'B1:Z1'  # Assuming names are in the range of columns B to Z in row 1 (adjust as needed)
        name_values = self.service.spreadsheets().values().get(
            spreadsheetId=self.SPREADSHEET_ID,
            range=name_range
        ).execute().get('values', [])

        if name_values:
            name_row_values = name_values[0]
            for i, name in enumerate(name_row_values):
                if name == name_to_find:
                    col = chr(ord('B') + i)
                    column_range = '{}3:{}'.format(col, col)
                    column_values = self.service.spreadsheets().values().get(
                        spreadsheetId=self.SPREADSHEET_ID,
                        range=column_range
                    ).execute().get('values', [])

                    # Find the first empty cell in the column below the last date

    def _update_values(self, range_, values, col=None):
        body = {'values': values}
        if col is not None:
            range_ = range_[:1] + str(col) + range_[1:]
        self.service.spreadsheets().values().update(
            spreadsheetId=self.SPREADSHEET_ID,
            range=range_,
            valueInputOption='RAW',
            body=body
        ).execute()


def _get_values(self, range_):
    result = self.service.spreadsheets().values().get(
        spreadsheetId=self.SPREADSHEET_ID,
        range=range_
    ).execute()
    values = result.get('values', [])
    return values

def _insert_blank_row(self, row_number):
    body = {
        'requests': [
            {
                'insertDimension': {
                    'range': {
                        'sheetId': 0,  # Assuming the sheet ID is 0
                        'dimension': 'ROWS',
                        'startIndex': row_number - 1,
                        'endIndex': row_number
                    },
                    'inheritFromBefore': False
                }
            }
        ]
    }

    self.service.spreadsheets().batchUpdate(
        spreadsheetId=self.SPREADSHEET_ID,
        body=body
    ).execute()
