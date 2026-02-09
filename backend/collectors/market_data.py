import yfinance as yf
import pandas as pd
from datetime import datetime, timedelta

def collect_market_data(period="7d", interval="1h"):
    """
    Collects market data for Silver, Gold, and Bitcoin.
    """
    symbols = {
        "Silver": "SLV",
        "Gold": "GC=F",
        "Bitcoin": "BTC-USD",
        "USD_Index": "DX-Y.NYB" # Dollar Index for macro context
    }
    
    data = {}
    for name, ticker in symbols.items():
        try:
            # optimize: fetch all at once if possible, but separate is safer for error handling
            df = yf.download(ticker, period=period, interval=interval, progress=False)
            if not df.empty:
                # Store as list of dicts or JSON-serializable format
                # Reset index to make 'Date' a column
                df.reset_index(inplace=True)
                # Convert timestamp to string
                df['Datetime'] = df['Datetime'].astype(str) if 'Datetime' in df.columns else df['Date'].astype(str)
                data[name] = df.to_dict(orient='records')
            else:
                print(f"Warning: No data found for {name}")
                data[name] = []
        except Exception as e:
            print(f"Error fetching {name}: {e}")
            data[name] = []
            
    return data

if __name__ == "__main__":
    # Test execution
    result = collect_market_data()
    print(f"Fetched {len(result)} asset classes.")
    for key, val in result.items():
        print(f"{key}: {len(val)} records")
        if val:
            print(f"Latest {key}: {val[-1]}")
