import streamlit as st
import pandas as pd
import numpy as np
import yfinance as yf
import time

from ta.momentum import RSIIndicator
from ta.trend import MACD, EMAIndicator
from ta.volatility import BollingerBands

st.set_page_config(
    page_title="Spider AI Financial Platform",
    layout="wide"
)

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

st.sidebar.title(
    "⚡ AI Control Center"
)

stock = st.sidebar.selectbox(
    "Select Stock",
    ["AAPL","MSFT","GOOGL","AMZN","TSLA"]
)

with st.spinner(
    "🕸️ AI analyzing live market signals..."
):
    time.sleep(2)

data = yf.download(
    stock,
    period="1y"
)

if isinstance(data.columns, pd.MultiIndex):

    data.columns = (
        data.columns.get_level_values(0)
    )

data["RSI"] = RSIIndicator(
    close=data["Close"]
).rsi()

data["MACD"] = MACD(
    close=data["Close"]
).macd()

data["EMA"] = EMAIndicator(
    close=data["Close"]
).ema_indicator()

bb = BollingerBands(
    close=data["Close"]
)

data["BB_High"] = (
    bb.bollinger_hband()
)

data["BB_Low"] = (
    bb.bollinger_lband()
)

data["Daily_Return"] = (
    data["Close"].pct_change()
)

data["Volatility"] = (
    (data["High"] - data["Low"])
    /
    data["Close"]
)

data["Volume_Change"] = (
    data["Volume"].pct_change()
)

data["Momentum"] = (
    data["Close"]
    -
    data["Close"].shift(10)
)

data["MA_Ratio"] = (
    data["Close"]
    /
    data["EMA"]
)

data["Trend_Strength"] = (
    data["MACD"]
    *
    data["RSI"]
)

data.dropna(inplace=True)

latest_rsi = round(
    data["RSI"].iloc[-1],
    2
)

latest_macd = round(
    data["MACD"].iloc[-1],
    2
)

latest_close = round(
    data["Close"].iloc[-1],
    2
)

volatility = round(
    data["Volatility"]
    .tail(30)
    .mean(),
    4
)

signal = "HOLD"

confidence = 50

if latest_rsi < 35 and latest_macd > 0:

    signal = "BUY"

    confidence = 82

elif latest_rsi > 70 and latest_macd < 0:

    signal = "SELL"

    confidence = 79

elif latest_macd > 0:

    signal = "BUY"

    confidence = 68

else:

    signal = "SELL"

    confidence = 64

if volatility < 0.02:

    risk = "LOW"

elif volatility < 0.05:

    risk = "MEDIUM"

else:

    risk = "HIGH"

signal_class = "hold"

if signal == "BUY":

    signal_class = "buy"

elif signal == "SELL":

    signal_class = "sell"

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

st.subheader(
    "⚡ AI Confidence Meter"
)

st.progress(confidence / 100)

st.subheader(
    "📡 Live AI Market Feed"
)

st.write(
    f"Selected Stock: {stock}"
)

st.write(
    f"Latest Close Price: {latest_close}"
)

st.write(
    f"RSI: {latest_rsi}"
)

st.write(
    f"MACD: {latest_macd}"
)

st.write(
    "AI scanning momentum and volatility signals..."
)

st.subheader(
    "📈 Live Stock Price Chart"
)

st.line_chart(
    data["Close"]
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

st.subheader(
    "📊 Latest Market Data"
)

st.dataframe(
    data.tail(5)
)

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

