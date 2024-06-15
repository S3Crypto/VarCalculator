import pandas as pd
import numpy as np

# Sample data: historical prices of an asset
data = {
    "Date": ["2023-06-01", "2023-06-02", "2023-06-05", "2023-06-06", "2023-06-07"],
    "Price": [100, 102, 101, 103, 104]
}
df = pd.DataFrame(data)
df['Date'] = pd.to_datetime(df['Date'])
df.set_index('Date', inplace=True)

# Calculate daily returns
df['Return'] = df['Price'].pct_change().dropna()
df = df.dropna()

# Compute daily returns
returns = df['Return']

confidence_level = 0.95
time_horizon = 1  # 1 day

# Sort returns
sorted_returns = returns.sort_values()

# Calculate VaR
index = int((1 - confidence_level) * len(sorted_returns))
var = abs(sorted_returns.iloc[index])

print(f"VaR at {confidence_level * 100}% confidence level over {time_horizon} day(s): {var:.2%}")
