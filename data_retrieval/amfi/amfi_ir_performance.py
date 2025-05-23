import pandas as pd
from rapidfuzz import process, fuzz

from db.db_functions import perform_upsert_update_on_conflict, session
from models import SchemeMetric, MFScheme


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


def update_ir_to_db(amfi_code, ir, average, period):
    data_array = [{
        "amfi_code": amfi_code,
        "time_horizon": period,
        "metric_name": "INFORMATION RATIO",
        "investment": ir,
        "category": average
    }]
    perform_upsert_update_on_conflict(SchemeMetric, data_array, ['amfi_code', 'time_horizon', 'metric_name'])


def update_performance_to_db(amfi_code, investment_return, benchmark_return, average, period):
    data_array = [{
        "amfi_code": amfi_code,
        "time_horizon": period,
        "metric_name": "RETURN",
        "investment": investment_return,
        "category": average,
        "index": benchmark_return
    }]
    perform_upsert_update_on_conflict(SchemeMetric, data_array, ['amfi_code', 'time_horizon', 'metric_name'])


def get_category_average(df, column_name):
    df[column_name] = pd.to_numeric(df[column_name], errors='coerce')
    return df[column_name].mean()


def get_all_schemes_with_amfi_code():
    # TODO: Organise this function
    schemes = session.query(MFScheme.scheme_name, MFScheme.amfi_code).all()
    return {scheme.scheme_name: scheme.amfi_code for scheme in schemes}


def get_amfi_code_from_scheme_name(scheme_code_map, scheme_name, threshold=80):
    best_match = process.extractOne(
        scheme_name.strip().upper(),  # your input
        scheme_code_map,  # dictionary of choices
        scorer=fuzz.token_sort_ratio,
        score_cutoff=threshold,
    )
    if best_match and best_match[1] >= threshold:
        matched_name = best_match[0]
        return scheme_code_map[matched_name]
    else:
        return None


def retrieve_ir_performance_data():
    df = pd.read_csv("../amfi_fund_performance.csv")
    print(df.columns)
    average_return = {
        3: get_category_average(df, "return3YearRegular"),
        5: get_category_average(df, "return5YearRegular"),
        10: get_category_average(df, "return10YearRegular"),
    }
    average_ir = {
        3: get_category_average(df, "ir3YearRegular"),
        5: get_category_average(df, "ir5YearRegular"),
        10: get_category_average(df, "ir10YearRegular"),
    }
    for _, row in df.iterrows():
        for period in [3, 5, 10]:
            ir_row_name = f"return{period}YearRegular"
            performance_row_name = f"ir{period}YrRegular"
            performance_benchmark_row_name = f"return{period}YearBenchmark"
            amfi_code = get_amfi_code_from_scheme_name(row['schemeName'])
            update_ir_to_db(amfi_code, row[ir_row_name], average_ir[period], period)
            update_performance_to_db(amfi_code, row[performance_row_name], performance_benchmark_row_name,
                                     average_return[period], period)


retrieve_ir_performance_data()
