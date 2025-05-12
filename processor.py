import requests

from quantitative_analysis import calculate_standard_deviation, calculate_beta, calculate_sharpe_ratio, \
    calculate_treynor_ratio, calculate_r_squared, calculate_max_drawdown, calculate_upside_capture, \
    calculate_downside_capture
from util import create_df_with_monthly_values

moneycontrol_url = "https://www.moneycontrol.com/mc/widget/mfnavonetimeinvestment/get_chart_value?isin={{isin}}&dur=10Y&ind_id=&classic=true&type=benchmark"
import pandas as pd

excel_file = 'TestPython.xlsx'
sheet_names = pd.ExcelFile(excel_file).sheet_names

for sheet_name in sheet_names:
    df = pd.read_excel(excel_file, sheet_name=sheet_name)

    for row in df.itertuples():
        isin = str(row.isin_growth)
        scheme_name = str(row.scheme_name).upper()

        updated_url = moneycontrol_url.replace("{{isin}}", isin)
        response = requests.get(updated_url)

        if response.status_code == 200:
            data = response.json()
            nav_data = data.get('g1', [])
            benchmark_data = data.get('n50', [])

            monthly_fund_df = create_df_with_monthly_values(nav_data, "navDate", "navValue")
            monthly_benchmark_df = create_df_with_monthly_values(benchmark_data, "_time", "_value", True)

            std_dev_3 = calculate_standard_deviation(monthly_fund_df, 3)
            print(std_dev_3)
            std_dev_5 = calculate_standard_deviation(monthly_fund_df, 5)
            std_dev_7 = calculate_standard_deviation(monthly_fund_df, 7)
            std_dev_10 = calculate_standard_deviation(monthly_fund_df, 10)

            beta_3 = calculate_beta(monthly_fund_df, monthly_benchmark_df, 3)
            print(beta_3)
            sharpe_ratio_3 = calculate_sharpe_ratio(monthly_fund_df, 0.072, std_dev_3, 3)
            print(sharpe_ratio_3)
            treynor_ratio_3 = calculate_treynor_ratio(monthly_fund_df, 0.072, beta_3, 3)
            print(treynor_ratio_3)
            r_squared_3 = calculate_r_squared(monthly_fund_df, monthly_benchmark_df, 3)
            print(r_squared_3)
            r_max_drawdown_3 = calculate_max_drawdown(monthly_fund_df, 3)
            print(r_max_drawdown_3)
            upside_capture_3 = calculate_upside_capture(monthly_fund_df, monthly_benchmark_df, 3)
            print(upside_capture_3)
            downside_capture_3 = calculate_downside_capture(monthly_fund_df, monthly_benchmark_df, 3)
            print(downside_capture_3)

# Step 2: Get Fund and Benchmark data for last 10Y
# Step 3: Calculate the data
