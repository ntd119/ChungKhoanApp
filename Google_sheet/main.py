import pandas as pd
import gspread
import json

from oauth2client.service_account import ServiceAccountCredentials

def read_google_sheet():
    scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
    creds = ServiceAccountCredentials.from_json_keyfile_name(r'hoiphadaock.json', scope)
    gc = gspread.authorize(creds)
    spreadsheet_id = "1k_q0M8LmAaOgbWqv0GzoBuxd-vuViIvWpqYIiV-iNVM"
    wks = gc.open_by_key(spreadsheet_id)
    worksheet = wks.worksheet('cp_da_mua')
    df = pd.DataFrame(worksheet.get_all_records())
    json_list = json.loads(df.to_json(orient="records"))
    cp_da_mua = {}
    for item in json_list:
        cp_da_mua[item["MaCK"]] = {
            "should_buy": 0,
            "enable_sound": 0,
            "bought": item["GiaMua"],
            "percent_cut_loss": "4.0",
            "percent_sell": "4.0",
            "follow": 1
        }
    print(cp_da_mua)

read_google_sheet()