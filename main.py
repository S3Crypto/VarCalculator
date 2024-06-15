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

# Summary statistics of returns
summary_stats = returns.describe()

# Detailed output
print("\n========== VaR Calculation Details ==========")
print(f"Input File: {file_path}")
print(f"Confidence Level: {confidence_level * 100}%")
print(f"Time Horizon: {time_horizon} day(s)")
print("\nSummary Statistics of Returns:")
print(summary_stats)
print("\nIntermediate Calculations:")
print(f"Sorted Returns:\n{returns.sort_values().values}")
print(f"Index for {confidence_level * 100}% confidence level: {int((1 - confidence_level) * len(returns))}")
print(f"VaR for 1 day: {var:.2%}")
print(f"VaR adjusted for {time_horizon} day(s): {adjusted_var:.2%}")

# Additional confidence levels
confidence_levels = [0.90, 0.95, 0.99]
print("\nVaR at Multiple Confidence Levels:")
for cl in confidence_levels:
    var = historical_var(returns, cl)
    adjusted_var = var * (time_horizon ** 0.5)
    print(f"VaR at {cl * 100}% confidence level: {adjusted_var:.2%}")

print("\n=============================================")
