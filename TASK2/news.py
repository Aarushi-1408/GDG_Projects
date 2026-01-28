import yfinance as yf
import pandas as pd

def get_stock_news(ticker, limit=10):
    stock = yf.Ticker(ticker)
    news = stock.news

    if not news:
        return pd.DataFrame()

    rows = []
    for item in news[:limit]:
        rows.append({
            "title": item.get("title"),
            "publisher": item.get("publisher"),
            "link": item.get("link"),
            "published": pd.to_datetime(item.get("providerPublishTime"), unit="s")
        })

    return pd.DataFrame(rows)

def filter_news_by_date(news_df, start_date, end_date):
    if news_df.empty:
        return news_df

    return news_df[
        (news_df['published'] >= start_date) &
        (news_df['published'] <= end_date)
    ]

def prepare_news_documents(news_df):
    if news_df.empty:
        return []

    documents = []
    for _, row in news_df.iterrows():
        documents.append(
            f"Date: {row['published'].date()}, "
            f"Source: {row['publisher']}, "
            f"Title: {row['title']}"
        )

    return documents




