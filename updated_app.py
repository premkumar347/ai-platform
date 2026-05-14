import streamlit as st
import pandas as pd
import numpy as np
import yfinance as yf
import joblib
import time

from ta.momentum import RSIIndicator
from ta.trend import MACD, EMAIndicator
from ta.volatility import BollingerBands

# page config
st.set_page_config(
    page_title="Spider AI Financial Platform",
    layout="wide"
)

# custom css
st.markdown(
    """
    <style>

    .stApp {
        background: linear-gradient(
            135deg,
            #050816,
            #0f172a,
            #111827
        );
        color: white;
    }

    .main-title {
        font-size: 52px;
        font-weight: bold;
        text-align: center;
        color: #ff1e1e;
        text-shadow:
            0px 0px 10px #ff0000,
            0px 0px 20px #2563eb,
            0px 0px 40px #2563eb;
        margin-top: 10px;
    }

    .sub-title {
        text-align: center;
        font-size: 22px;
        color: #93c5fd;
        margin-bottom: 30px;
    }

    .card {
        background: rgba(17,24,39,0.8);
        border: 1px solid #2563eb;
        border-radius: 18px;
        padding: 25px;
        box-shadow:
            0px 0px 20px rgba(37,99,235,0.5);
        margin-bottom: 20px;
    }

    .metric-title {
        color: #93c5fd;
        font-size: 18px;
        font-weight: bold;
    }

    .metric-value {
        color: white;
        font-size: 34px;
        font-weight: bold;
    }

    .buy {
        color: #00ff99;
        text-shadow: 0px 0px 10px #00ff99;
    }

    .sell {
        color: #ff3b3b;
        text-shadow: 0px 0px 10px #ff3b3b;
    }

    .hold {
        color: #ffd700;
        text-shadow: 0px 0px 10px #ffd700;
    }

    </style>
    """,
    unsafe_allow_html=True
)

# title
st.markdown(
    """
    <div class='main-title'>
    🕷️ Spider AI Financial Platform
    </div>
    """,
    unsafe_allow_html=True
)

st.markdown(
    """
    <div class='sub-title'>
    Real Time AI Powered Stock Intelligence
    </div>
    """,
    unsafe_allow_html=True
)

# sidebar
st.sidebar.title(
    "⚡ AI Control Center"
)

stock = st.sidebar.selectbox(

    "Select Stock",

    ["AAPL","MSFT","GOOGL","AMZN","TSLA"]
)

# loading animation
with st.spinner(
    "🕸️ AI analyzing live market signals..."
):
    time.sleep(2)

# load model
model = joblib.load(
    "stock_model.pkl"
)

# download live stock data
data = yf.download(

    stock,

    period="1y"
)

# fixing multiindex issue
if isinstance(data.columns, pd.MultiIndex):

    data.columns = (
        data.columns.get_level_values(0)
    )

# RSI
data["RSI"] = RSIIndicator(
    close=data["Close"]
).rsi()

# MACD
data["MACD"] = MACD(
    close=data["Close"]
).macd()

# EMA
data["EMA"] = EMAIndicator(
    close=data["Close"]
).ema_indicator()

# Bollinger Bands
bb = BollingerBands(
    close=data["Close"]
)

data["BB_High"] = (
    bb.bollinger_hband()
)

data["BB_Low"] = (
    bb.bollinger_lband()
)

# daily return
data["Daily_Return"] = (
    data["Close"].pct_change()
)

# volatility
data["Volatility"] = (
    (data["High"] - data["Low"])
    /
    data["Close"]
)

# volume change
data["Volume_Change"] = (
    data["Volume"].pct_change()
)

# momentum
data["Momentum"] = (
    data["Close"]
    -
    data["Close"].shift(10)
)

# moving average ratio
data["MA_Ratio"] = (
    data["Close"]
    /
    data["EMA"]
)

# trend strength
data["Trend_Strength"] = (
    data["MACD"]
    *
    data["RSI"]
)

# stock encoding
stock_map = {

    "AAPL":0,
    "MSFT":1,
    "GOOGL":2,
    "AMZN":3,
    "TSLA":4
}

data["Stock_Code"] = (
    stock_map[stock]
)

# remove missing values
data.dropna(inplace=True)

# features
features = [

    "RSI",
    "MACD",
    "EMA",
    "BB_High",
    "BB_Low",
    "Volume",
    "Daily_Return",
    "Volatility",
    "Volume_Change",
    "Momentum",
    "MA_Ratio",
    "Trend_Strength",
    "Stock_Code"
]

latest = (
    data[features]
    .tail(1)
)

# prediction
pred = model.predict(latest)[0]

# probability
prob = model.predict_proba(latest)[0]

confidence = round(
    max(prob) * 100,
    2
)

# signal logic
if confidence < 60:

    signal = "HOLD"

elif pred == 1:

    signal = "BUY"

else:

    signal = "SELL"

# risk logic
avg_volatility = (

    data["Volatility"]

    .tail(30)

    .mean()
)

if avg_volatility < 0.02:

    risk = "LOW"

elif avg_volatility < 0.05:

    risk = "MEDIUM"

else:

    risk = "HIGH"

# signal color
signal_class = "hold"

if signal == "BUY":

    signal_class = "buy"

elif signal == "SELL":

    signal_class = "sell"

# top metrics
col1, col2, col3 = st.columns(3)

with col1:

    st.markdown(
        f'''
        <div class="card">

            <div class="metric-title">
            Recommendation
            </div>

            <div class="metric-value {signal_class}">
            {signal}
            </div>

        </div>
        ''',
        unsafe_allow_html=True
    )

with col2:

    st.markdown(
        f'''
        <div class="card">

            <div class="metric-title">
            Confidence
            </div>

            <div class="metric-value">
            {confidence}%
            </div>

        </div>
        ''',
        unsafe_allow_html=True
    )

with col3:

    st.markdown(
        f'''
        <div class="card">

            <div class="metric-title">
            Risk Level
            </div>

            <div class="metric-value">
            {risk}
            </div>

        </div>
        ''',
        unsafe_allow_html=True
    )

# confidence bar
st.subheader(
    "⚡ AI Confidence Meter"
)

st.progress(confidence / 100)

# live feed
st.subheader(
    "📡 Live AI Market Feed"
)

st.write(
    f"Selected Stock: {stock}"
)

st.write(
    "AI scanning RSI, MACD, EMA and momentum signals..."
)

st.write(
    "Detecting institutional buying pressure..."
)

st.write(
    "Volatility engine active..."
)

# chart
st.subheader(
    "📈 Live Stock Price Chart"
)

st.line_chart(
    data["Close"]
)

# AI explanations
latest_rsi = (
    data["RSI"]
    .iloc[-1]
)

latest_macd = (
    data["MACD"]
    .iloc[-1]
)

reasons = []

if latest_rsi > 70:

    reasons.append(
        "RSI indicates overbought market"
    )

elif latest_rsi < 30:

    reasons.append(
        "RSI indicates oversold recovery"
    )

if latest_macd > 0:

    reasons.append(
        "MACD shows bullish momentum"
    )

else:

    reasons.append(
        "MACD shows bearish momentum"
    )

if risk == "HIGH":

    reasons.append(
        "Market volatility is high"
    )

st.subheader(
    "🧠 AI Analysis"
)

for r in reasons:

    st.write("-", r)

# latest market data
st.subheader(
    "📊 Latest Market Data"
)

st.dataframe(
    data.tail(5)
)

# footer
st.markdown("---")

st.markdown(
    """
    <center>
    🕷️ Spider AI Financial Engine |
    Real Time Market Intelligence
    </center>
    """,
    unsafe_allow_html=True
)

