from langchain_community.llms import OpenAI

llm = OpenAI(
    temperature=0,
    max_tokens=300
)

def explain_with_rag(ticker, drop_info, evidence):
    context = "\n".join(evidence)

    prompt = f"""
You are a financial analyst.

Stock: {ticker}
Price movement: {abs(drop_info['pct_change']):.2f}% drop
Period: {drop_info['start_date'].date()} to {drop_info['end_date'].date()}

Relevant news:
{context}

Task:
Explain why the stock dropped.
Only use the provided news.
Do not speculate beyond the evidence.
"""

    return llm(prompt)
