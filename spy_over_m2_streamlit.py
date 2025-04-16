import streamlit as st
import yfinance as yf
from fredapi import Fred
import pandas as pd
import matplotlib.pyplot as plt
import os

# Setup
FRED_API_KEY = os.getenv("FRED_API_KEY")
fred = Fred(api_key=FRED_API_KEY)

# Sidebar input
st.sidebar.title("Settings")
start_date = st.sidebar.date_input("Start Date", pd.to_datetime("2000-01-01"))
end_date = st.sidebar.date_input("End Date", pd.to_datetime("today"))
interval = st.sidebar.selectbox("Resolution", ["1d", "1wk", "1mo"])

# Main
st.title("S&P 500 / M2 Money Supply Ratio")

# Get data
spy = yf.download('^GSPC', start=start_date, end=end_date, interval=interval)['Close']
m2 = fred.get_series('M2SL')

# Merge and plot
df = pd.concat([spy, m2], axis=1).dropna()
df.columns = ['SP500', 'M2']
df['SP500_M2_Ratio'] = df['SP500'] / df['M2']

# Plot
st.line_chart(df['SP500_M2_Ratio'])
