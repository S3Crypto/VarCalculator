import pandas as pd
from scipy.stats import mstats

def historical_var(returns, confidence_level=0.95):
    sorted_returns = returns.sort_values()
    index = int((1 - confidence_level) * len(sorted_returns))
    return abs(sorted_returns.iloc[index])

def iqr_filter(returns, multiplier=1.5):
    Q1 = returns.quantile(0.25)
    Q3 = returns.quantile(0.75)
    IQR = Q3 - Q1
    lower_bound = Q1 - (IQR * multiplier)
    upper_bound = Q3 + (IQR * multiplier)
    filtered_returns = returns[(returns >= lower_bound) & (returns <= upper_bound)]
    return filtered_returns

def calculate_var(filtered_returns, confidence_levels, time_horizon):
    capped_time_horizon = min(time_horizon, 100)
    var_values = [historical_var(filtered_returns, cl) for cl in confidence_levels]
    adjusted_var_values = [var * (capped_time_horizon ** 0.5) for var in var_values]
    return var_values, adjusted_var_values
