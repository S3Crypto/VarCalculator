import json
import numpy as np
from data_fetcher import fetch_historical_data
from var_calculator import iqr_filter, calculate_var, historical_var
from plotter import plot_distribution, plot_var, show_plots

# Load API key from config file
with open('config.json', 'r') as f:
    config = json.load(f)
    api_key = config['api_key']

# Collect user inputs
symbol = input("Enter the stock symbol: ")
time_horizon = int(input("Enter the time horizon in days: "))

# Fetch historical data from Alpha Vantage
try:
    df = fetch_historical_data(symbol, api_key)
except ValueError as e:
    print(e)
    exit(1)

# Calculate daily returns
df['Return'] = df['Price'].pct_change().dropna()
returns = df['Return'].dropna()

# Filter the returns using IQR to mitigate the impact of outliers
filtered_returns = iqr_filter(returns)

# Calculate VaR for different confidence levels
confidence_levels = np.arange(0.90, 1.00, 0.01)
var_values, adjusted_var_values = calculate_var(filtered_returns, confidence_levels, time_horizon)

# Detailed output
print("\n========== VaR Calculation Details ==========")
print(f"Stock Symbol: {symbol}")
print(f"Time Horizon: {time_horizon} day(s)")
print("\nSummary Statistics of Filtered Returns:")
summary_stats = filtered_returns.describe()
print(summary_stats)
print("\nIntermediate Calculations:")
print(f"Sorted Filtered Returns:\n{filtered_returns.sort_values().values}")
print(f"Index for 95.0% confidence level: {int((1 - 0.95) * len(filtered_returns))}")
var = historical_var(filtered_returns, 0.95)
adjusted_var = var * (min(time_horizon, 100) ** 0.5)
print(f"VaR for 1 day at 95% confidence level: {var:.2%}")
print(f"VaR adjusted for {time_horizon} day(s) at 95% confidence level: {adjusted_var:.2%}")

print("\nVaR at Multiple Confidence Levels:")
for cl, adj_var in zip(confidence_levels, adjusted_var_values):
    print(f"VaR at {cl * 100:.1f}% confidence level: {adj_var:.2%}")

print("\n=============================================")

# Plotting the results
plot_distribution(filtered_returns, symbol)
plot_var(confidence_levels, adjusted_var_values, symbol)
show_plots()
