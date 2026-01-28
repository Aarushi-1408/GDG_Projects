def explain_price_drop(ticker, pct_change):
    return (
        f"{ticker} has dropped by approximately {abs(pct_change):.2f}% "
        f"over the past few trading days. "
        "This indicates short-term negative market momentum. "
        "News and broader market factors may have contributed."
    )

def explain_drop_with_news(ticker, drop_info, news_df):
    explanation = (
        f"{ticker} fell by approximately {abs(drop_info['pct_change']):.2f}% "
        f"between {drop_info['start_date'].date()} and "
        f"{drop_info['end_date'].date()}.\n\n"
    )

    if news_df.empty:
        explanation += "No major news was found during this period."
        return explanation

    explanation += "Relevant news during this period:\n"
    for _, row in news_df.iterrows():
        explanation += f"- {row['title']} ({row['publisher']})\n"

    explanation += "\nThese events likely contributed to negative market sentiment."

    return explanation
