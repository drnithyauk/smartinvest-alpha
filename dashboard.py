
import streamlit as st
import pandas as pd
from alpha_vantage.timeseries import TimeSeries
from alpha_vantage.fundamentaldata import FundamentalData
import requests

API_KEY = "B6C62FMANII3GMQZ"
ts = TimeSeries(key=API_KEY, output_format='pandas')

def search_symbol(query):
    url = f"https://www.alphavantage.co/query?function=SYMBOL_SEARCH&keywords={query}&apikey={API_KEY}"
    response = requests.get(url)
    if response.status_code == 200:
        matches = response.json().get("bestMatches", [])
        return [(m['2. name'], m['1. symbol']) for m in matches]
    return []

def fetch_stock_data(symbol):
    data, _ = ts.get_daily_adjusted(symbol=symbol, outputsize='compact')
    data = data.rename(columns=lambda x: x.lower().replace(" ", "_"))
    return data

st.set_page_config(page_title="Smart Stock Investor", layout="wide")
st.markdown("<h1 style='text-align: center; color: #1a73e8;'>📊 Smart Stock Investor</h1>", unsafe_allow_html=True)

query = st.text_input("🔍 Search for a company by name or ticker symbol:")

if query:
    matches = search_symbol(query)
    if matches:
        company_names = [f"{name} ({symbol})" for name, symbol in matches]
        selected = st.selectbox("Select a match:", company_names)
        selected_symbol = selected.split("(")[-1].strip(")")
        df = fetch_stock_data(selected_symbol)

        st.subheader(f"📈 {selected}")
        st.line_chart(df['adjusted_close'])

        st.subheader("📋 Latest Data")
        st.dataframe(df.tail())

    else:
        st.warning("No matches found.")
else:
    st.info("Enter a company name or ticker symbol to begin.")
