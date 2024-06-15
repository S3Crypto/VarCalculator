import pandas as pd
import requests

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
        print("API response:", data)
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
