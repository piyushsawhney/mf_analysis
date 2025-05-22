import pandas as pd


def prepare_payload(category, sub_category, report_date):
    return {
        "maturityType": 1,
        "category": category,
        "subCategory": sub_category,
        "mfid": 0,
        "reportDate": report_date.strftime("%d-%b-%Y")
    }


headers = {
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/136.0.0.0 Safari/537.36",
    "accept": "application/json, text/plain, */*",
    "accept-language": "en-US,en;q=0.9",
    "accept-encoding": "gzip, deflate, br, zstd",
    "content-type": "application/json"
}

def match_scheme_name():
    pass


def retrieve_ir_performance_data_as_pd():
    df = pd.read_csv("../amfi_fund_performance.csv")
    print(df.columns)

retrieve_ir_performance_data_as_pd()