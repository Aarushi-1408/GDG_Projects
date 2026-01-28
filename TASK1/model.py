from pyexpat import model
import yfinance as yf
import pandas as pd
import numpy as np
import streamlit as st
import matplotlib.pyplot as plt

from sklearn.preprocessing import MinMaxScaler
from sklearn.metrics import mean_absolute_error, mean_squared_error
from keras.models import Sequential
from keras.layers import LSTM, Dense, Dropout


st.set_page_config(page_title="Stock LSTM Forecasting", layout="wide")
st.title("LSTM Stock Price Forecasting Dashboard")



ticker = st.text_input("Enter Stock Ticker", "AAPL")
start_date = st.date_input("Start Date", pd.to_datetime("2015-01-01"))
end_date = st.date_input("End Date", pd.to_datetime("2023-12-31"))

look_back = st.slider("Look-back window (days)", min_value=10, max_value=120, value=60)
forecast_days = st.slider("Forecast horizon (days)", min_value=1, max_value=30, value=7)




df = yf.download(ticker, start=start_date, end=end_date, progress=False)
df = df[['Close']].dropna()




st.subheader("Historical Data")
st.write(df.tail())


scaler = MinMaxScaler()
scaled_data = scaler.fit_transform(df[['Close']])

X, y = [], []
for i in range(look_back, len(scaled_data)):
    X.append(scaled_data[i-look_back:i, 0])
    y.append(scaled_data[i, 0])
X, y = np.array(X), np.array(y)
X = X.reshape((X.shape[0], X.shape[1], 1))


split = int(0.7 * len(X))
X_train, X_test = X[:split], X[split:]
y_train, y_test = y[:split], y[split:]

# ----------------------------
model = Sequential()
model.add(LSTM(50, return_sequences=True, input_shape=(X_train.shape[1], 1)))
model.add(Dropout(0.2))
model.add(LSTM(50))
model.add(Dropout(0.2))
model.add(Dense(1))




model.compile(optimizer='adam', loss='mean_squared_error')
st.write("Training LSTM model... this may take a minute.")
model.fit(X_train, y_train, epochs=20, batch_size=32, validation_split=0.1, verbose=0)


pred_scaled = model.predict(X_test)
pred = scaler.inverse_transform(pred_scaled)
y_test_inv = scaler.inverse_transform(y_test.reshape(-1, 1))





forecast_input = scaled_data[-look_back:].reshape(1, look_back, 1)
future_preds = []

for _ in range(forecast_days):
    next_pred_scaled = model.predict(forecast_input)
    future_preds.append(next_pred_scaled[0,0])
    
    # Reshape next_pred_scaled to 3D (samples, timesteps=1, features)
    next_pred_scaled_reshaped = next_pred_scaled.reshape(1, 1, 1)
    
    # Append along the time axis
    forecast_input = np.append(forecast_input[:,1:,:], next_pred_scaled_reshaped, axis=1)


future_preds = scaler.inverse_transform(np.array(future_preds).reshape(-1,1))
future_index = pd.date_range(df.index[-1], periods=forecast_days+1, freq='B')[1:]



mae = mean_absolute_error(y_test_inv, pred)
rmse = np.sqrt(mean_squared_error(y_test_inv, pred))



fig, ax = plt.subplots(figsize=(12,6))

# Historical
ax.plot(df.index, df['Close'], label="Historical", linewidth=2)

# Past predictions
test_index = df.index[look_back+split:]
ax.plot(test_index, pred, linestyle="--", label="Past Predictions")

# Simple confidence interval: ± std deviation of test residuals
residuals = y_test_inv - pred
std_res = np.std(residuals)
ax.fill_between(test_index, (pred - std_res).flatten(), (pred + std_res).flatten(), color='orange', alpha=0.2)

# Future forecast
ax.plot(future_index, future_preds, color="black", label=f"{forecast_days}-Day Forecast")
ax.fill_between(future_index, (future_preds - std_res).flatten(), (future_preds + std_res).flatten(), color='gray', alpha=0.2)

ax.set_title(f"{ticker} LSTM Price Forecast")
ax.set_xlabel("Date")
ax.set_ylabel("Price")
ax.legend()
ax.grid(True)

st.subheader("Forecast Visualization")
st.pyplot(fig)




st.subheader("Model Accuracy (Past Data)")
col1, col2 = st.columns(2)
col1.metric("MAE", f"{mae:.2f}")
col2.metric("RMSE", f"{rmse:.2f}")
