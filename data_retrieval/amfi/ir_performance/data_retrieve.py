import pandas as pd
import requests

from helpers.urls import AMFI_CRISIL
from helpers.utils import get_last_month_last_working_day


def prepare_payload(category, sub_category, report_date):
    payload = {
        "maturityType": 1,
        "category": category,
        "subCategory": sub_category,
        "mfid": 0,
        "reportDate": report_date.strftime("%d-%b-%Y")
    }
    return payload


headers = {
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/136.0.0.0 Safari/537.36",
    "accept": "application/json, text/plain, */*",
    "accept-language": "en-US,en;q=0.9",
    "accept-encoding": "gzip, deflate, br, zstd",
    "content-type": "application/json"
}


def get_data_as_pd(category, subcategory):
    response = requests.post(AMFI_CRISIL, headers=headers,
                             json=prepare_payload(category, subcategory, get_last_month_last_working_day()))
    if response.status_code == 200:
        response_json = response.json()
        data_list = response_json.get("data", [])
        if data_list:  # this is a Python list, safe to check truth value
            df = pd.DataFrame(data_list)
            return df
