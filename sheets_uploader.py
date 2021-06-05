# Script to upload lines to Sheets

from __future__ import print_function
import os.path
from googleapiclient.discovery import build
from google.oauth2 import service_account
from array import array

SCOPES = ['https://www.googleapis.com/auth/spreadsheets']

sheet_ID = '1OiZkOEvs0-2Bpp-w0wfSy-F_tyALjMwypx8ebmDJFXY'
creds = None
if os.path.exists('weathercritic_token.json'):
        creds = service_account.Credentials.from_service_account_file('weathercritic_token.json', scopes=SCOPES)



spreadsheet_service = build('sheets', 'v4', credentials=creds)

# Read data
range_name = 'Sheet1!A1:H10'
result = spreadsheet_service.spreadsheets().values().get(spreadsheetId=sheet_ID, range=range_name).execute()
rows = result.get('values', [])
print(f'{len(rows)} rows retrieved.')
print(f'{rows} rows retrieved.')


def append_list(list_to_append):
    array_to_append = []
    for item in list_to_append:
        array_to_append.append([item])
    json_input = {'majorDimension':'COLUMNS', 'values':array_to_append}
    append_setup = spreadsheet_service.spreadsheets().values().append(spreadsheetId=sheet_ID,
                                                                   range='Sheet1!A:H',
                                                                   body=json_input,
                                                                   valueInputOption='USER_ENTERED')
    respone = append_setup.execute()

append_list([1,2,3])