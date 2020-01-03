############
#  Pull from google shet
#  Save as json
#  https://console.developers.google.com/
############

import json
import gspread
from pathlib import Path

from oauth2client.service_account import ServiceAccountCredentials


def pull_from_gsheet():
    auth_json_path = 'db/google-app-name-1234567.json'
    gss_scopes = ['https://spreadsheets.google.com/feeds']

    #connect
    credentials = ServiceAccountCredentials.from_json_keyfile_name(auth_json_path,gss_scopes)
    gss_client = gspread.authorize(credentials)

    #Opne Google Sheet
    spreadsheet_key = '25635726536725367526' 

    #New a sheet
    sheet = gss_client.open_by_key(spreadsheet_key).sheet1

    row_number = len(sheet.col_values(1))

    # Save as Json
    data = []

    for row_ind in range(2, row_number + 1):
        row ={}
        row['country'] = sheet.cell(row_ind, 1).value
        row['location']  = sheet.cell(row_ind, 2).value
        row['name'] = sheet.cell(row_ind, 3).value
        row['url']  = sheet.cell(row_ind, 7).value
        data.append(row)

    print("[DBG] pullFilybotCsv")
    print(data)
    return data