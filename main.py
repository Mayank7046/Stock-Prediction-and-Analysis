import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.graph_objects as go

# Function to fetch stock data using Yahoo Finance API
def get_stock_data(ticker):
    stock = yf.Ticker(ticker)
    data = stock.history(period='1y')
    return data

# Function to plot candlestick chart
def plot_candlestick(data, stock_symbol):
    fig = go.Figure(data=[go.Candlestick(x=data.index,
                                         open=data['Open'],
                                         high=data['High'],
                                         low=data['Low'],
                                         close=data['Close'])])
    fig.update_layout(title_text=f'Candlestick Chart - {stock_symbol}', xaxis_title='Date', yaxis_title='Stock Price')
    return fig

# Function to calculate daily profit/loss
def calculate_daily_profit_loss(data):
    data['Daily Change'] = data['Close'].pct_change() * 100
    return data

# Function to plot profit/loss
def plot_profit_loss(data, stock_symbol):
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=data.index, y=data['Daily Change'], mode='lines', name='Daily Change'))
    fig.update_layout(title_text=f'Daily Profit/Loss - {stock_symbol}', xaxis_title='Date', yaxis_title='Percentage Change')
    return fig

# Streamlit app
st.title('Stock Analysis Project')

# Input stock symbols
stocks = ['AAPL', 'GOOGL', 'MSFT', 'AMZN', 'MRNA', 'NVAX', 'INO', 'BNTX', 'VXRT', 'AZN','TCS','LBPH','AMD','HIMS','FIZZ','CRSP','LPL','PRTA','USCA']
selected_stocks = st.multiselect('Select stock symbols:', stocks)

# Input investment amount
investment_amount = st.number_input('Enter your investment amount:', min_value=0.01, value=1000.0, step=0.01)

# Fetch stock data
stock_data_dict = {}
for stock_symbol in selected_stocks:
    st.text(f'Fetching stock data for {stock_symbol}...')
    stock_data_dict[stock_symbol] = get_stock_data(stock_symbol)
    st.text(f'Fetching stock data for {stock_symbol}... done!')

# Display stock data and analysis
for stock_symbol, stock_data in stock_data_dict.items():
    st.subheader(f'Stock Data - {stock_symbol}')
    st.write(stock_data.tail())

    # Calculate daily profit/loss
    stock_data = calculate_daily_profit_loss(stock_data)

    # Display profit/loss plot
    st.subheader(f'Daily Profit/Loss - {stock_symbol}')
    profit_loss_fig = plot_profit_loss(stock_data, stock_symbol)
    st.plotly_chart(profit_loss_fig)

    # Display candlestick chart
    st.subheader(f'Candlestick Chart - {stock_symbol}')
    candlestick_fig = plot_candlestick(stock_data, stock_symbol)
    st.plotly_chart(candlestick_fig)

    # Calculate previous value of investment
    previous_value = investment_amount * (1 + stock_data['Daily Change'] / 100).shift(1).fillna(1).prod()

    # Display previous value
    st.subheader(f'Previous Investment Status - {stock_symbol}')
    st.write(f'Initial Investment Amount: ${investment_amount:.2f}')
    st.write(f'Previous Value: ${previous_value:.2f}')

    # Display whether in profit or loss based on previous value
    if stock_data['Close'].iloc[-1] > stock_data['Close'].iloc[0]:
        st.success(f'You were in profit based on the previous data!')
    elif stock_data['Close'].iloc[-1] < stock_data['Close'].iloc[0]:
        st.error(f'You were in loss based on the previous data!')
    else:
        st.info('No profit, no loss based on the previous data. The stock price remained unchanged.')
