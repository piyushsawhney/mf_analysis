import pandas as pd
import requests

from quantitative_analysis.formula_functions import *

moneycontrol_url = "https://www.moneycontrol.com/mc/widget/mfnavonetimeinvestment/get_chart_value?isin={{isin}}&dur=10Y&ind_id=&classic=true&type=benchmark"


def create_df_with_monthly_values(value_array_with_date, date_column_name, value_column_name, is_benchmark=False):
    df = pd.DataFrame(value_array_with_date)
    df[date_column_name] = pd.to_datetime(df[date_column_name])
    df.set_index(date_column_name, inplace=True)
    monthly_values = df[value_column_name].resample('ME').last().astype(float)
    monthly_returns = monthly_values.pct_change().dropna()
    monthly_df = pd.DataFrame({
        'monthlyValues': monthly_values,
        'monthlyReturns': monthly_returns,
    })
    monthly_df.index.name = 'monthDate'
    today = pd.Timestamp.today()
    last_date_in_data = monthly_df.index.max()
    if last_date_in_data.month == today.month and last_date_in_data.year == today.year:
        monthly_df = monthly_df[:-1]
    monthly_df.sort_index(inplace=True)
    return monthly_df


def get_data_from_moneycontrol(isin):
    updated_url = moneycontrol_url.replace("{{isin}}", isin)
    response = requests.get(updated_url)

    if response.status_code == 200:
        data = response.json()
        nav_data = data.get('g1', [])
        benchmark_data = data.get('n50', [])

        monthly_fund_df = create_df_with_monthly_values(nav_data, "navDate", "navValue")
        monthly_benchmark_df = create_df_with_monthly_values(benchmark_data, "_time", "_value", True)
        return monthly_fund_df, monthly_benchmark_df


def beta3_for_row(row):
    monthly_fund_df, monthly_benchmark_df = get_data_from_moneycontrol(row['isin_growth'])
    beta = calculate_beta(monthly_fund_df, monthly_benchmark_df, 3)
    print(beta)
    return beta

def metrics_for_row(row):
    isin = row.get('isin_growth', None)
    if not isin:
        return pd.Series({
            'std3': None,
            'std5': None,
            'std7': None,
            'std10': None,
            'beta3': None,
            'beta5': None,
            'beta7': None,
            'beta10': None,
            'sharpe3': None,
            'sharpe5': None,
            'sharpe7': None,
            'sharpe10': None,
            'treynor3': None,
            'treynor5': None,
            'treynor7': None,
            'treynor10': None,
            'r23': None,
            'r25': None,
            'r27': None,
            'r210': None,
            'max_d3': None,
            'max_d5': None,
            'max_d7': None,
            'max_d10': None,
            'up_cap3': None,
            'up_cap5': None,
            'up_cap7': None,
            'up_cap10': None,
            'down_cap3': None,
            'down_cap5': None,
            'down_cap7': None,
            'down_cap10': None
        })

    fund_df, benchmark_df = get_data_from_moneycontrol(isin)
    if fund_df is None or benchmark_df is None:
        return pd.Series({
            'std3': None,
            'std5': None,
            'std7': None,
            'std10': None,
            'beta3': None,
            'beta5': None,
            'beta7': None,
            'beta10': None,
            'sharpe3': None,
            'sharpe5': None,
            'sharpe7': None,
            'sharpe10': None,
            'treynor3': None,
            'treynor5': None,
            'treynor7': None,
            'treynor10': None,
            'r23': None,
            'r25': None,
            'r27': None,
            'r210': None,
            'max_d3': None,
            'max_d5': None,
            'max_d7': None,
            'max_d10': None,
            'up_cap3': None,
            'up_cap5': None,
            'up_cap7': None,
            'up_cap10': None,
            'down_cap3': None,
            'down_cap5': None,
            'down_cap7': None,
            'down_cap10': None
        })

    try:
        std3 = calculate_standard_deviation(fund_df,  3)
        std5 = calculate_standard_deviation(fund_df,  5)
        std7 = calculate_standard_deviation(fund_df,  7)
        std8 = calculate_standard_deviation(fund_df,  10)
        # beta3 = calculate_beta(fund_df, benchmark_df, period)
        # sharpe = calculate_sharpe_ratio(fund_df, period)
        # beta5 = calculate_beta5(fund_df, benchmark_df, period)  # or different period
    except Exception as e:
        print(f"Error calculating metrics for ISIN {isin}: {e}")
        return pd.Series({
            'std3': None,
            'std5': None,
            'std7': None,
            'std10': None,
            'beta3': None,
            'beta5': None,
            'beta7': None,
            'beta10': None,
            'sharpe3': None,
            'sharpe5': None,
            'sharpe7': None,
            'sharpe10': None,
            'treynor3': None,
            'treynor5': None,
            'treynor7': None,
            'treynor10': None,
            'r23': None,
            'r25': None,
            'r27': None,
            'r210': None,
            'max_d3': None,
            'max_d5': None,
            'max_d7': None,
            'max_d10': None,
            'up_cap3': None,
            'up_cap5': None,
            'up_cap7': None,
            'up_cap10': None,
            'down_cap3': None,
            'down_cap5': None,
            'down_cap7': None,
            'down_cap10': None
        })

    return pd.Series({
        'beta3': beta3,
        'sharpe_ratio': sharpe,
        'beta5': beta5
    })
excel_file = '../test.xlsx'
output_file = '../modified_test.xlsx'

# Read all sheets into dict of DataFrames
sheets_dict = pd.read_excel(excel_file, sheet_name=None)

for sheet_name, df in sheets_dict.items():
    print(sheet_name)
    # Create new column 'beta3' by applying update_value to each row
    df['beta3'] = df.apply(beta3_for_row, axis=1)
    sheets_dict[sheet_name] = df

# Save all sheets back to a new Excel file
with pd.ExcelWriter(output_file) as writer:
    for sheet_name, df in sheets_dict.items():
        df.to_excel(writer, sheet_name=sheet_name, index=False)
