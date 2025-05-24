import json

import pandas as pd

from data_retrieval.amfi.ir_performance.data_processor import get_category_average
from data_retrieval.amfi.ir_performance.data_retrieve import get_data_as_pd
from data_retrieval.amfi.ir_performance.scheme_selector import get_amfi_code_from_scheme_name, \
    get_all_schemes_in_subcategory
from db.db_functions import perform_upsert_update_on_conflict
from models import SchemeMetric


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


def retrieve_ir_performance_data():
    with open('config/category.json', 'r') as file:
        category_json = json.load(file)

    for category_id, category_info in category_json.items():
        subcategories = category_info.get("subcategories", {})
        if subcategories:
            for subcategory_id, subcategory_name in subcategories.items():
                df = get_data_as_pd(category_id, subcategory_id)
                # df = pd.read_csv("amfi_fund_performance.csv")

                average_return = {
                    3: get_category_average(df, "return3YearRegular"),
                    5: get_category_average(df, "return5YearRegular"),
                    10: get_category_average(df, "return10YearRegular"),
                }
                average_ir = {
                    3: get_category_average(df, "ir3YrRegular"),
                    5: get_category_average(df, "ir5YrRegular"),
                    10: get_category_average(df, "ir10YrRegular"),
                }
                for _, row in df.iterrows():
                    amfi_code = get_amfi_code_from_scheme_name(get_all_schemes_in_subcategory(subcategory_name),
                                                               row['schemeName'].upper())
                    for period in [3, 5, 10]:
                        performance_row_name = f"return{period}YearRegular"
                        ir_row_name = f"ir{period}YrRegular"
                        performance_benchmark_row_name = f"return{period}YearBenchmark"
                        if amfi_code:
                            if pd.notna(row[ir_row_name]):
                                update_ir_to_db(amfi_code, row[ir_row_name], average_ir[period], period)
                            if pd.notna(row[performance_row_name]):
                                update_performance_to_db(amfi_code, row[performance_row_name],
                                                         row[performance_benchmark_row_name],
                                                         average_return[period], period)
