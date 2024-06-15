import pandas as pd
import numpy as np
import requests
import json
import matplotlib.pyplot as plt
import seaborn as sns
from scipy.stats import mstats

def fetch_historical_data(symbol, api_key, outputsize='full'):
    url = f"https://www.alphavantage.co/query"
    params = {
        'function': 'TIME_SERIES_DAILY',
        'symbol': symbol,
        'outputsize': outputsize,
        'apikey': api_key
    }
    response = requests.get(url, params=params)
    data = response.json()

    if 'Time Series (Daily)' not in data:
        print("API response:", data)  # Debugging line to print the raw API response
        raise ValueError(f"Error fetching data for {symbol}: {data.get('Note', 'Unknown error')}")

    tsd = data['Time Series (Daily)']
    df = pd.DataFrame.from_dict(tsd, orient='index')
    df.index = pd.to_datetime(df.index)
    df = df.sort_index()
    df = df[['4. close']]
    df.columns = ['Price']
    
    # Convert Price column to numeric, forcing errors to NaN and then dropping them
    df['Price'] = pd.to_numeric(df['Price'], errors='coerce')
    df = df.dropna()

    return df

def historical_var(returns, confidence_level=0.95):
    sorted_returns = returns.sort_values()
    index = int((1 - confidence_level) * len(sorted_returns))
    return abs(sorted_returns.iloc[index])

def regularize_confidence_level(confidence_input):
    # Remove any '%' symbols and convert to a float
    confidence_str = confidence_input.replace('%', '')
    confidence_value = float(confidence_str)

    # If the value is greater than 1, assume it is a percentage and convert to decimal
    if confidence_value > 1:
        confidence_value /= 100

    return confidence_value

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

# Winsorize the returns to mitigate the impact of outliers
winsorized_returns = mstats.winsorize(returns, limits=[0.025, 0.025])

# Convert MaskedArray back to pandas Series
winsorized_returns = pd.Series(winsorized_returns, index=returns.index)

# Calculate VaR for different confidence levels
confidence_levels = np.arange(0.90, 1.00, 0.01)
var_values = [historical_var(winsorized_returns, cl) for cl in confidence_levels]
adjusted_var_values = [var * (time_horizon ** 0.5) for var in var_values]

# Detailed output
print("\n========== VaR Calculation Details ==========")
print(f"Stock Symbol: {symbol}")
print(f"Time Horizon: {time_horizon} day(s)")
print("\nSummary Statistics of Winsorized Returns:")
summary_stats = winsorized_returns.describe()
print(summary_stats)
print("\nIntermediate Calculations:")
print(f"Sorted Winsorized Returns:\n{winsorized_returns.sort_values().values}")
print(f"Index for 95.0% confidence level: {int((1 - 0.95) * len(winsorized_returns))}")
var = historical_var(winsorized_returns, 0.95)
adjusted_var = var * (time_horizon ** 0.5)
print(f"VaR for 1 day at 95% confidence level: {var:.2%}")
print(f"VaR adjusted for {time_horizon} day(s) at 95% confidence level: {adjusted_var:.2%}")

print("\nVaR at Multiple Confidence Levels:")
for cl, adj_var in zip(confidence_levels, adjusted_var_values):
    print(f"VaR at {cl * 100:.1f}% confidence level: {adj_var:.2%}")

print("\n=============================================")

# Plotting the distribution of returns
plt.figure(figsize=(10, 6))
sns.histplot(winsorized_returns, bins=50, kde=True)
plt.title(f'Distribution of Daily Returns for {symbol} (Winsorized)')
plt.xlabel('Daily Return')
plt.ylabel('Frequency')
plt.grid(True)

# Plotting the VaR values
plt.figure(figsize=(10, 6))
plt.plot(confidence_levels * 100, adjusted_var_values, marker='o')
plt.title(f'Value at Risk (VaR) for {symbol}')
plt.xlabel('Confidence Level (%)')
plt.ylabel('VaR')
plt.grid(True)

# Show all plots
plt.show()
