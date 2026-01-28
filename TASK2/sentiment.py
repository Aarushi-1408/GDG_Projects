NEGATIVE_KEYWORDS = [
    "miss", "drop", "fall", "decline", "lawsuit",
    "regulation", "weak", "slowdown", "cut", "warning"
]

def estimate_sentiment(text):
    text = text.lower()
    score = sum(1 for word in NEGATIVE_KEYWORDS if word in text)
    return score
