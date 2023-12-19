import streamlit as st
import numpy as np
import yfinance as yf
import math
import matplotlib.pyplot as plt

# Used for calculating Discount Factor 
# risk free rate = rate of return of an investment with zero risk
def get_risk_free_rate():
    treasury_bill_symbol = '^IRX' # 13 week treasury bill currently about 5%
    treasury_bill = yf.Ticker(treasury_bill_symbol)
    # last close price
    latest_yield = treasury_bill.history(period="1d")['Close'].iloc[-1]
    risk_free_rate = latest_yield/100 #convert to decimal
    return risk_free_rate

def get_data(ticker_symbol):
    #define ticker
    ticker = yf.Ticker(ticker_symbol)
    #historical data
    historical_data = ticker.history(period="1y")
    #Returns closing price
    return historical_data["Close"]

def fetch_option_data(ticker_symbol):
    # Define ticker
    ticker = yf.Ticker(ticker_symbol)
    # current price
    current_price = ticker.history(period="1d")['Close'].iloc[-1]
    #Options data (calls, puts: using options_data.calls, options_data.puts)
    options_data = ticker.option_chain()
    # Strike prices
    strike = list(options_data.calls['strike'])
    return current_price, options_data, strike

def up_move(vol, t_step):
    u = (math.e)**(vol*math.sqrt(t_step))
    return u

def down_move(vol, t_step):
    d = (math.e)**(-vol*math.sqrt(t_step))
    return d

def historical_data(ticker):
    historical_data = get_data(ticker)
    log_returns = np.log(historical_data / historical_data.shift(1))
    return log_returns

def build_binomial_tree(current_price, u, d, steps):
    tree = np.zeros([steps + 1, steps + 1])

    for i in range(steps + 1):
        for j in range(i + 1):
            tree[j, i] = current_price * (u ** (i - j)) * (d ** j)
    
    return tree

def calculate_call_option_values(tree, strike, risk_free_rate, steps, t_step):
    call_option_tree = np.zeros_like(tree)
    # Calculate the option value at expiration
    call_option_tree[:, steps] = np.maximum(tree[:, steps] - strike, 0)

    # Discount rate for each step
    discount_rate = np.exp(-risk_free_rate * t_step)

    # Work backward through the tree
    for i in range(steps - 1, -1, -1):
        for j in range(i + 1):
            call_option_tree[j, i] = discount_rate * 0.5 * (call_option_tree[j, i + 1] + call_option_tree[j + 1, i + 1])
    return call_option_tree

def calculate_put_option_values(tree, strike, risk_free_rate, steps, t_step):
    put_option_tree = np.zeros_like(tree)
    put_option_tree[:, steps] = np.maximum(strike - tree[:, steps], 0)

    discount_rate = np.exp(-risk_free_rate * t_step)

    for i in range(steps - 1, -1, -1):
        for j in range(i + 1):
            put_option_tree[j, i] = discount_rate * 0.5 * (put_option_tree[j, i + 1] + put_option_tree[j + 1, i + 1])
    return put_option_tree

def plot_binomial_tree(tree):
    steps = tree.shape[1]
    plt.figure(figsize=(12, 12))
    for i in range(steps):
        for j in range(i + 1):
            plt.scatter(i, tree[j, i], color='blue')
            # Connect nodes with lines
            if i < steps - 1:
                plt.plot([i, i + 1], [tree[j, i], tree[j, i + 1]], color='black')
                plt.plot([i, i + 1], [tree[j, i], tree[j + 1, i + 1]], color='black')

    plt.title('Binomial Tree for Option Pricing')
    plt.xlabel('Step')
    plt.ylabel('Stock Price ($)')
    plt.grid()
    return plt

def plot_historical_data(ticker_symbol):
    ticker = yf.Ticker(ticker_symbol)
    historical_data_5y = ticker.history(period="5y")
    
    plt.figure(figsize=(12, 6))
    plt.plot(historical_data_5y.index, historical_data_5y['Close'], label='Closing Price')
    plt.title(f'Historical Closing Prices - Last 5 Years of {ticker_symbol}')
    plt.xlabel('Date')
    plt.ylabel('Stock Price ($)')
    plt.legend()
    plt.grid()
    return plt

def main():
    st.title("Binomial Option Pricing Model")

    # Input fields for user parameters
    ticker = st.text_input("Stock Ticker Symbol(e.g. AMZN):", "AMZN")
    steps = st.slider("Number of Steps:", min_value=1, max_value=100, value=6)

    if ticker:
        current_price, _ , strike_list = fetch_option_data(ticker)
        strike = st.selectbox("Select Strike Price:", strike_list)
        if st.button("Calculate Option Prices"):
            if steps and strike_list:
                try:
                    # Fetch data and calculate option price
                    vol = np.std(historical_data(ticker)) * np.sqrt(252)  # Annualize the volatility
                    r = get_risk_free_rate()  # Risk-free rate
                    t_step = 1 / steps  # Length of each time step

                    u = up_move(vol, t_step)
                    d = down_move(vol, t_step)

                    # Building the binomial tree for stock prices
                    stock_price_tree = build_binomial_tree(current_price, u, d, steps)

                    # Calculating option values using the binomial tree
                    call_option_tree = calculate_call_option_values(stock_price_tree, strike, r, steps, t_step)
                    put_option_tree = calculate_put_option_values(stock_price_tree, strike, r, steps, t_step)
                    
                    # Display the option price
                    call_option_price = call_option_tree[0, 0]
                    put_option_price = put_option_tree[0, 0]
                    st.success(f"The calculated Call option price is: ${call_option_price:.2f}")
                    st.success(f"The calculated Put option price is: ${put_option_price:.2f}")
                    
                    #Plotting binomial tree
                    plt_tree = plot_binomial_tree(stock_price_tree)
                    st.pyplot(plt_tree)
            
                    # plotting historical data (closing prices)
                    plt_historical = plot_historical_data(ticker)
                    st.pyplot(plt_historical)
                except Exception as e:
                    st.error(f"An error occurred: {e}")

if __name__ == "__main__":
    main()


