import streamlit as st # type: ignore
import requests # type: ignore
import os
import matplotlib.pyplot as plt # type: ignore
import pandas as pd # type: ignore
import plotly.express as px # type: ignore
from dotenv import load_dotenv # type: ignore

# Load API key from .env
load_dotenv()
API_KEY = os.getenv("EXCHANGE_RATE_API_KEY")
BASE_URL = f"https://v6.exchangerate-api.com/v6/{API_KEY}/latest/"

# 🎨 Streamlit UI Design
st.set_page_config(page_title="💱 Currency Converter", layout="centered")
st.title("💸 Currency Converter with Graphs & Formulas")

# 🚀 Sidebar for extra info
st.sidebar.header("📌 How it Works?")
st.sidebar.write(
    """
    - Enter the amount and select currencies.  
    - Click **Convert** to get the result.  
    - Graph shows past exchange rate trends.  
    - **Formula Used**: `Amount × Exchange Rate = Converted Amount`
    """
)

# 🔥 Currency Selection
col1, col2, col3 = st.columns([1, 1, 1])

amount = col1.number_input("💰 Enter Amount", min_value=0.0, format="%.2f")
from_currency = col2.text_input("🔄 From Currency (e.g. USD)", "USD").upper()
to_currency = col3.text_input("🔄 To Currency (e.g. EUR)", "EUR").upper()

# 🎯 Conversion Logic
def convert_currency(amount, from_currency, to_currency):
    url = BASE_URL + from_currency
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        exchange_rate = data["conversion_rates"].get(to_currency)
        if exchange_rate:
            return amount * exchange_rate, exchange_rate
    return None, None

# 🔘 Convert Button
if st.button("🔄 Convert"):
    converted_amount, exchange_rate = convert_currency(amount, from_currency, to_currency)
    if converted_amount:
        st.success(f"💵 {amount} {from_currency} = 💶 {converted_amount:.2f} {to_currency}")
        st.write(f"**Formula Used:** `{amount} × {exchange_rate:.4f} = {converted_amount:.2f}`")
    else:
        st.error("⚠️ Invalid currency code or API issue.")

# 📈 Graph: Exchange Rate Trend
st.subheader("📊 Exchange Rate Trend (Last 7 Days)")
historical_rates = {
    "USD": [1.0, 0.95, 0.97, 0.96, 0.94, 0.93, 0.92],  # Dummy data (Replace with real API data)
    "EUR": [0.89, 0.88, 0.87, 0.86, 0.85, 0.84, 0.83],
}
days = ["Day 1", "Day 2", "Day 3", "Day 4", "Day 5", "Day 6", "Day 7"]

df = pd.DataFrame({"Days": days, "Exchange Rate": historical_rates.get(to_currency, historical_rates["USD"])})
fig = px.line(df, x="Days", y="Exchange Rate", title=f"Exchange Rate Trend for {to_currency}", markers=True)
st.plotly_chart(fig)

# 🔚 Footer
st.markdown(
    """
    💡 **Tip:** Exchange rates change daily!  
    📌 Use the graph to track trends and convert at the right time.
    """
)
