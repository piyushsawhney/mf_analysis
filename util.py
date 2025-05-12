import pandas as pd


def filter_data_for_period(df, period):
    period_ago = pd.Timestamp.today() - pd.DateOffset(years=period)
    df_period = df[df.index >= period_ago]
    return df_period


def create_df_with_monthly_values(value_array_with_date, date_column_name, value_column_name, is_benchmark = False):
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

