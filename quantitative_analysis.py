import numpy as np
import pandas as pd

from util import filter_data_for_period


def calculate_standard_deviation(fund_df, period):
    filtered_df = filter_data_for_period(fund_df, period)
    monthly_std = filtered_df['monthlyReturns'].std()
    annualized_std = monthly_std * np.sqrt(12)
    return annualized_std


def calculate_beta(fund_df, benchmark_df, period):
    filtered_fund_df = filter_data_for_period(fund_df, period)
    filtered_benchmark_df = filter_data_for_period(benchmark_df, period)

    returns_df = pd.DataFrame({
        'fund_return': filtered_fund_df['monthlyReturns'],
        'benchmark_return': filtered_benchmark_df['monthlyReturns']
    }).dropna()

    beta = returns_df['fund_return'].cov(returns_df['benchmark_return']) / returns_df['benchmark_return'].var()
    return beta


def calculate_sharpe_ratio(fund_df, annual_risk_free_rate, standard_deviation, period):
    risk_free_rate_monthly = annual_risk_free_rate / 12
    filtered_fund_df = filter_data_for_period(fund_df, period)

    returns_df = pd.DataFrame({
        'fund_return': filtered_fund_df['monthlyReturns'],
    }).dropna()

    returns_df['excessReturns'] = returns_df['fund_return'] - risk_free_rate_monthly
    average_excess_return = returns_df['excessReturns'].mean()
    sharpe_ratio = average_excess_return / standard_deviation
    annualized_sharpe_ratio = sharpe_ratio * np.sqrt(12)
    return annualized_sharpe_ratio

def calculate_treynor_ratio(returns_array_with_date, beta, annual_risk_free_rate, period):
    pass


def calculate_r_squared(returns_array_with_date, benchmark_return_array_with_date, annual_risk_free_rate, beta, period):
    pass


def calculate_max_drawdown(nav_array, period):
    pass


def calculate_upside_capture(returns_array_with_date, benchmark_return_array_with_date, period):
    pass


def calculate_downside_capture(returns_array_with_date, benchmark_return_array_with_date, period):
    pass
