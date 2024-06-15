import pandas as pd

def historical_var(returns, confidence_level=0.95):
    sorted_returns = returns.sort_values()
    index = int((1 - confidence_level) * len(sorted_returns))
    return abs(sorted_returns.iloc[index])

# Collect user inputs
file_path = input("Enter the path to the CSV file containing historical prices: ")
confidence_level = float(input("Enter the confidence level (e.g., 0.95 for 95%): "))
time_horizon = int(input("Enter the time horizon in days: "))

# Read historical price data from CSV
df = pd.read_csv(file_path)
df['Date'] = pd.to_datetime(df['Date'])
df.set_index('Date', inplace=True)

# Calculate daily returns
df['Return'] = df['Price'].pct_change().dropna()
returns = df['Return'].dropna()

# Calculate VaR
var = historical_var(returns, confidence_level)

# Adjust VaR for the time horizon
adjusted_var = var * (time_horizon ** 0.5)

print(f"VaR at {confidence_level * 100}% confidence level over {time_horizon} day(s): {adjusted_var:.2%}")
