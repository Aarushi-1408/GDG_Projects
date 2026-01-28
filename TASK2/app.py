import streamlit as st
from intent import extract_intent_and_ticker
from market_data import get_stock_data, detect_recent_drop, find_recent_drop_window
from reasoning import explain_price_drop, explain_drop_with_news
from news import get_stock_news, filter_news_by_date, prepare_news_documents
from vector_store import NewsVectorStore
from llm_reasoning import explain_with_rag

st.set_page_config(page_title="Market Intelligence Bot")
st.title("Market Intelligence Assistant")

query = st.text_input("Ask about a stock:")

if query:
    intent, ticker = extract_intent_and_ticker(query)

    if not ticker:
        st.warning("I couldn't identify the company. Try mentioning it clearly.")
    else:
        df = get_stock_data(ticker)

        if intent == "explain_drop":

            # --- Market drop detection ---
            pct_change = detect_recent_drop(df)
            basic_explanation = explain_price_drop(ticker, pct_change)

            st.subheader("Market Movement")
            st.success(basic_explanation)

            # --- Drop window ---
            drop_info = find_recent_drop_window(df)

            # --- News ---
            news_df = get_stock_news(ticker)
            relevant_news = filter_news_by_date(
                news_df,
                drop_info["start_date"],
                drop_info["end_date"]
            )

            # --- Vector store ---
            store = NewsVectorStore()
            docs = prepare_news_documents(relevant_news)
            store.add_documents(docs)

            search_query = f"Why did {ticker} stock drop?"
            evidence = store.search(search_query, k=3)

            # --- RAG explanation ---
            final_answer = explain_with_rag(
                ticker,
                drop_info,
                evidence
            )

            st.subheader("AI Explanation")
            st.write(final_answer)

            if not relevant_news.empty:
                st.subheader("Related News")
                st.dataframe(relevant_news[['published', 'title', 'publisher']])

            st.subheader("Evidence Used")
            for e in evidence:
                st.markdown(f"- {e}")

        else:
            st.info("Intent recognized, but explanation logic not added yet.")
