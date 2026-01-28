import yfinance as yf
import pandas as pd

def get_stock_data(ticker, period="6mo"):
    df = yf.download(ticker, period=period, progress=False)
    return df[['Close']].dropna()

'''def detect_recent_drop(df, days=5):
    recent = df.tail(days)
    pct_change = (recent['Close'].iloc[-1] - recent['Close'].iloc[0]) / recent['Close'].iloc[0]
    return pct_change * 100
'''
def detect_recent_drop(df, days=5):
    recent = df.tail(days)
    start_price = recent['Close'].iloc[0]
    end_price = recent['Close'].iloc[-1]

    pct_change = (end_price - start_price) / start_price * 100
    return float(pct_change)

def find_recent_drop_window(df, days=5):
    recent = df.tail(days)
    start_price = recent['Close'].iloc[0]
    end_price = recent['Close'].iloc[-1]

    pct_change = (end_price - start_price) / start_price * 100

    return {
        "pct_change": pct_change,
        "start_date": recent.index[0],
        "end_date": recent.index[-1]
    }
