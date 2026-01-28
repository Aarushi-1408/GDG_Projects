import re

TICKER_MAP = {
    "apple": "AAPL",
    "google": "GOOGL",
    "microsoft": "MSFT",
    "amazon": "AMZN",
    "tesla": "TSLA",
    
}

def extract_intent_and_ticker(query: str):
    query_lower = query.lower()
    ticker = None
    for name, symbol in TICKER_MAP.items():
        if name in query_lower:
            ticker = symbol
            break

    # detect intent
    if "why" in query_lower and ("drop" in query_lower or "fall" in query_lower):
        intent = "explain_drop"
    elif "when" in query_lower and ("up" in query_lower or "increase" in query_lower):
        intent = "find_uptrend"
    else:
        intent = "general"

    return intent, ticker