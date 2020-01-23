import gspread
from oauth2client.service_account import ServiceAccountCredentials

# The tutorial to create credentials are in this website:
# https://www.twilio.com/blog/2017/02/an-easy-way-to-read-and-write-to-a-google-spreadsheet-in-python.html


def get_sheet(client_secret_json, url, sheet_name):
    # use creds to create a client to interact with the Google Drive API
    scope = ['https://spreadsheets.google.com/feeds']
    # creds = ServiceAccountCredentials.from_json_keyfile_name('client_secret.json', scope)
    creds = ServiceAccountCredentials.from_json_keyfile_name(client_secret_json, scope)
    client = gspread.authorize(creds)

    # Find a workbook by name and open the first sheet
    # Make sure you use the right name here.
    sheet = client.open_by_url(url).worksheet(sheet_name)    # sheet = client.open("Copy of Legislators 2017").sheet1

    # Extract and print all of the values
    return sheet
    # list_of_hashes = sheet.get_all_records()

