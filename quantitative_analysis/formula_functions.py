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
    risk_free_rate_monthly = (1 + annual_risk_free_rate) ** (1 / 12) - 1
    filtered_fund_df = filter_data_for_period(fund_df, period)

    returns_df = pd.DataFrame({
        'fund_return': filtered_fund_df['monthlyReturns'],
    }).dropna()

    returns_df['excessReturns'] = returns_df['fund_return'] - risk_free_rate_monthly
    average_excess_return = returns_df['excessReturns'].mean()
    monthly_standard_deviation = standard_deviation / np.sqrt(12)
    sharpe_ratio = average_excess_return / monthly_standard_deviation
    annualized_sharpe_ratio = sharpe_ratio * np.sqrt(12)
    return annualized_sharpe_ratio


def calculate_treynor_ratio(fund_df, annual_risk_free_rate, beta, period):
    filtered_fund_df = filter_data_for_period(fund_df, period)
    returns_df = pd.DataFrame({
        'fund_return': filtered_fund_df['monthlyReturns'],
    }).dropna()
    avg_monthly_return = returns_df['fund_return'].mean()
    annual_return = (1 + avg_monthly_return) ** 12 - 1
    treynor_ratio = (annual_return - annual_risk_free_rate) / beta
    return treynor_ratio


def calculate_r_squared(fund_df, benchmark_df, period):
    filtered_fund_df = filter_data_for_period(fund_df, period)
    filtered_benchmark_df = filter_data_for_period(benchmark_df, period)
    fund_annualized_returns = (1 + filtered_fund_df['monthlyReturns']) ** 12 - 1
    benchmark_annualized_returns = (1 + filtered_benchmark_df['monthlyReturns']) ** 12 - 1

    returns_df = pd.DataFrame({
        'fund_annualized_return': fund_annualized_returns,
        'benchmark_annualized_return': benchmark_annualized_returns
    }).dropna()
    correlation = np.corrcoef(returns_df['fund_annualized_return'], returns_df['benchmark_annualized_return'])[0, 1]
    r_squared = correlation ** 2
    return r_squared


def calculate_max_drawdown(fund_df, period):
    filtered_fund_df = filter_data_for_period(fund_df, period)

    fund_returns = filtered_fund_df['monthlyReturns']
    # Calculate cumulative returns
    cumulative_returns = (1 + fund_returns).cumprod()

    # Calculate the running peak (maximum cumulative return up to each point)
    running_peak = cumulative_returns.cummax()

    # Calculate drawdowns (percentage decline from peak)
    drawdowns = (cumulative_returns - running_peak) / running_peak

    # The maximum drawdown is the lowest point of the drawdowns
    max_drawdown = drawdowns.min()

    # Find the peak and trough
    # Peak is the last date where cumulative return was higher before the drawdown started
    peak_index = cumulative_returns[:drawdowns.idxmin()].idxmax()  # Peak before max drawdown
    peak_date = peak_index
    peak_value = cumulative_returns.loc[peak_index]

    # Filter the cumulative returns after the peak to find the trough
    cumulative_returns_after_peak = cumulative_returns.loc[peak_date:]

    # Trough is the minimum cumulative return after the peak date
    trough_index = cumulative_returns_after_peak.idxmin()
    trough_date = trough_index
    trough_value = cumulative_returns.loc[trough_index]

    # Calculate the duration of the drawdown (from peak to trough)
    drawdown_duration = (trough_date.year - peak_date.year) * 12 + (
            trough_date.month - peak_date.month)  # Duration in months
    return {
        'max_drawdown': max_drawdown,
        'peak_date': peak_date,
        'peak_value': peak_value,
        'trough_date': trough_date,
        'trough_value': trough_value,
        'drawdown_duration': drawdown_duration
    }


def calculate_upside_capture(fund_df, benchmark_df, period):
    filtered_fund_df = filter_data_for_period(fund_df, period)
    filtered_benchmark_df = filter_data_for_period(benchmark_df, period)

    returns_df = pd.DataFrame({
        'fund_return': filtered_fund_df['monthlyReturns'],
        'benchmark_return': filtered_benchmark_df['monthlyReturns']
    }).dropna()

    # Filter months when the benchmark return is positive
    positive_benchmark = returns_df[returns_df['benchmark_return'] > 0]

    # Calculate the total returns of the fund and benchmark for those positive benchmark months
    fund_positive_return = positive_benchmark['fund_return'].sum()
    benchmark_positive_return = positive_benchmark['benchmark_return'].sum()

    # Calculate the Upside Capture Ratio
    upside_capture_ratio = (fund_positive_return / benchmark_positive_return) * 100 if benchmark_positive_return != 0 else 0

    return upside_capture_ratio


def calculate_downside_capture(fund_df, benchmark_df, period):
    filtered_fund_df = filter_data_for_period(fund_df, period)
    filtered_benchmark_df = filter_data_for_period(benchmark_df, period)

    returns_df = pd.DataFrame({
        'fund_return': filtered_fund_df['monthlyReturns'],
        'benchmark_return': filtered_benchmark_df['monthlyReturns']
    }).dropna()

    # Filter months when the benchmark return is negative
    negative_benchmark  = returns_df[returns_df['benchmark_return'] < 0]

    # Calculate the total returns of the fund and benchmark for those negative benchmark months
    fund_negative_return = negative_benchmark['fund_return'].sum()
    benchmark_negative_return = negative_benchmark['benchmark_return'].sum()

    # Calculate the Upside Capture Ratio
    upside_capture_ratio = (fund_negative_return / benchmark_negative_return) * 100 if benchmark_negative_return != 0 else 0

    return upside_capture_ratio
