import streamlit as st
import time

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
    <div class='main-title'>🕷️ Spider AI Financial Platform</div>
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
st.sidebar.title("⚡ AI Control Center")

stock = st.sidebar.selectbox(
    "Select Stock",
    ["AAPL","MSFT","GOOGL","AMZN","TSLA"]
)

signals = {
    "AAPL":"BUY",
    "MSFT":"BUY",
    "GOOGL":"HOLD",
    "AMZN":"SELL",
    "TSLA":"SELL"
}

confidence_data = {
    "AAPL":82,
    "MSFT":76,
    "GOOGL":67,
    "AMZN":58,
    "TSLA":61
}

risk_data = {
    "AAPL":"LOW",
    "MSFT":"LOW",
    "GOOGL":"MEDIUM",
    "AMZN":"HIGH",
    "TSLA":"HIGH"
}

signal = signals[stock]

confidence = confidence_data[stock]

risk = risk_data[stock]

signal_class = "hold"

if signal == "BUY":
    signal_class = "buy"

elif signal == "SELL":
    signal_class = "sell"

with st.spinner("🕸️ AI analyzing market signals..."):
    time.sleep(1.5)

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

st.subheader("⚡ AI Confidence Meter")

st.progress(confidence / 100)

st.subheader("📡 Live AI Market Feed")

st.write(f"Selected Stock: {stock}")

st.write(
    "AI scanning RSI, MACD, EMA and momentum signals..."
)

st.write(
    "Detecting institutional buying pressure..."
)

st.write(
    "Volatility engine active..."
)

st.subheader("📈 Stock Trend Visualization")

chart_data = [10,15,13,18,20,17,25,28,30]

st.line_chart(chart_data)

st.subheader("🧠 AI Analysis")

if signal == "BUY":

    st.success(
        "Bullish momentum detected with strong trend confirmation."
    )

elif signal == "SELL":

    st.error(
        "Bearish pressure and high volatility detected."
    )

else:

    st.warning(
        "Market momentum is currently neutral."
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

