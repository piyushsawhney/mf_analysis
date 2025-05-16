import pandas as pd
import requests

from db.db_functions import match_string_in_mf_scheme_name, session, perform_query, perform_insert
from models import MFBenchmark

# API endpoint
url = "https://polling.crisil.com/gateway/pollingsebi/api/amfi/fundperformance"


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

# Make the POST request
# response = requests.post(url, json=payload, headers=headers)

def update_benchmark_code(benchmark_code):
    benchmark = perform_query(MFBenchmark, benchmark_code)
    if not benchmark:
        benchmark = MFBenchmark(code=benchmark_code)
        perform_insert(benchmark)

def update_amfi_scheme_benchmarks(scheme_name, benchmark_code):
    schemes= match_string_in_mf_scheme_name(scheme_name)
    for scheme in schemes:
        scheme.benchmark_code = benchmark_code.upper()
    session.commit()


# Check if the request was successful
# if response.status_code == 200:
#     data = response.json()
#
#     if data["validationStatus"] == "SUCCESS":
#         funds = data["data"]
#
#         # Convert to DataFrame
#         df = pd.DataFrame(funds)

        # Optional: Select key performance columns
        # selected_columns = [
        #     "schemeName", "benchmark", "navDate", "navRegular", "navDirect",
        #     "return1YearRegular", "return1YearDirect", "return1YearBenchmark",
        #     "return3YearRegular", "return3YearDirect", "return3YearBenchmark",
        #     "return5YearRegular", "return5YearDirect", "return5YearBenchmark",
        #     "return10YearRegular", "return10YearDirect", "return10YearBenchmark",
        #     "dailyAUM"
        # ]
        # df_selected = df[selected_columns]

        # Save to CSV
#         df.to_csv("amfi_fund_performance.csv", index=False)
#         print("Data saved to amfi_fund_performance.csv")
#
#     else:
#         print("API responded but validation failed:", data["validationMsg"])
# else:
#     print("Failed to fetch data. Status Code:", response.status_code)
