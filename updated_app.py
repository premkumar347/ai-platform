import streamlit as st

st.set_page_config(
    page_title="AI Financial Intelligence",
    layout="wide"
)

st.title("AI Financial Intelligence Platform")

stock = st.selectbox(
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

confidence = {
    "AAPL":"82%",
    "MSFT":"77%",
    "GOOGL":"65%",
    "AMZN":"59%",
    "TSLA":"62%"
}

risk = {
    "AAPL":"LOW",
    "MSFT":"LOW",
    "GOOGL":"MEDIUM",
    "AMZN":"HIGH",
    "TSLA":"HIGH"
}

st.metric(
    "Recommendation",
    signals[stock]
)

st.metric(
    "Confidence",
    confidence[stock]
)

st.metric(
    "Risk",
    risk[stock]
)

st.line_chart([1,2,3,4,5])
