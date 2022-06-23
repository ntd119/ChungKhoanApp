import pandas as pd
import gspread

ss_cred_path = r'hoiphadaock.json'
from oauth2client.service_account import ServiceAccountCredentials

def read_google_sheet():
    scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
    creds = ServiceAccountCredentials.from_json_keyfile_name(ss_cred_path, scope)
    gc = gspread.authorize(creds)
    spreadsheet_id = "1k_q0M8LmAaOgbWqv0GzoBuxd-vuViIvWpqYIiV-iNVM"
    wks = gc.open_by_key(spreadsheet_id)
    worksheet = wks.worksheet('cp_da_mua')
    df = pd.DataFrame(worksheet.get_all_records())
    data = df.to_json()
    print(data)

read_google_sheet()