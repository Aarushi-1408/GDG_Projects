# GDG_Projects


This repository contains two components:

- Task 1: A machine learning model for stock price prediction.
- Task 2: An AI-powered chatbot that explains stock price movements using news and LLM reasoning.


### Task 1 – Stock Prediction

This module trains a machine learning model using historical stock data to predict future trends.

Features:
- Time series preprocessing(LSTM)
- Feature engineering
- Model training and evaluation
- Performance metrics (MAE, RMSE)

To run Task 1:

cd TASK1
streamlit run model.py




### Task 2 – AI Chatbot

This module detects stock price drops and explains them using financial news and LLM-based reasoning.

Features:
- Drop detection
- News retrieval
- Vector search (FAISS)
- LLM-based explanation
- Streamlit UI

To run Task 2:

cd TASK2
streamlit run app.py
