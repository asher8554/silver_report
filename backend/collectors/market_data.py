import yfinance as yf
import pandas as pd
from datetime import datetime, timedelta

def collect_market_data(period="7d", interval="1h"):
    """
    은(Silver), 금(Gold), 비트코인(Bitcoin)의 시장 데이터를 수집합니다.
    """
    symbols = {
        "Silver": "SLV",
        "Gold": "GC=F",
        "Bitcoin": "BTC-USD",
        "USD_Index": "DX-Y.NYB" # 거시 경제지표: 달러 인덱스
    }
    
    data = {}
    for name, ticker in symbols.items():
        try:
            # 최적화: 가능하다면 한 번에 가져오는 것이 좋지만, 에러 처리를 위해 개별적으로 가져오는 것이 안전함
            df = yf.download(ticker, period=period, interval=interval, progress=False)
            if not df.empty:
                # 딕셔너리 리스트 또는 JSON 직렬화 가능한 형식으로 저장
                # 인덱스를 리셋하여 'Date'를 컬럼으로 만듦
                df.reset_index(inplace=True)
                # 타임스탬프를 문자열로 변환
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
