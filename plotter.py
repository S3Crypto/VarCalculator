import matplotlib.pyplot as plt
import seaborn as sns

def plot_distribution(winsorized_returns, symbol):
    plt.figure(figsize=(10, 6))
    sns.histplot(winsorized_returns, bins=50, kde=True)
    plt.title(f'Distribution of Daily Returns for {symbol} (Winsorized)')
    plt.xlabel('Daily Return')
    plt.ylabel('Frequency')
    plt.grid(True)

def plot_var(confidence_levels, adjusted_var_values, symbol):
    plt.figure(figsize=(10, 6))
    plt.plot(confidence_levels * 100, adjusted_var_values, marker='o')
    plt.title(f'Value at Risk (VaR) for {symbol}')
    plt.xlabel('Confidence Level (%)')
    plt.ylabel('VaR')
    plt.grid(True)

def show_plots():
    plt.show()
