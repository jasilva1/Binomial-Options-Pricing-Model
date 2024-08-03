import streamlit as st
import numpy as np
import yfinance as yf
import math
import matplotlib.pyplot as plt

class Model:
    def __init__(self, ticker, treasury_bill, expiration):
        self.ticker = ticker
        self.treasury_bill = treasury_bill
        self.expiration = expiration

    def get_risk_free_rate(self):
        risk_free_rate = (self.treasury_bill.history(period="1d")['Close'].iloc[-1])/100
        if self.expiration < 1:
            return risk_free_rate * self.expiration
    
    def fetch_option_data(self):
        current_price =self.ticker.history(period="1d")['Close'].iloc[-1]
        options_data = self.ticker.option_chain()
        strike = list(options_data.calls['strike'])
        return current_price, options_data, strike
    
    @staticmethod
    def up_down_move(vol, t_step):
        return (math.e)**(vol*math.sqrt(t_step)), (math.e)**(-vol*math.sqrt(t_step))
    
    def historical_data(self):
        historical_data = self.ticker.history(period="1y")["Close"]
        return np.log(historical_data / historical_data.shift(1))
    



def build_binomial_tree(current_price, u, d, steps):
    tree = np.zeros([steps + 1, steps + 1])
    for i in range(steps + 1):
        for j in range(i + 1):
            tree[j, i] = current_price * (u ** (i - j)) * (d ** j)
    return tree
    
def calculate_call_option_values(tree, strike, risk_free_rate, steps, t_step):
    call_option_tree = np.zeros_like(tree)
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

def plot_historical_data(ticker):
    historical_data_5y = ticker.history(period="5y")
    plt.figure(figsize=(12, 6))
    plt.plot(historical_data_5y.index, historical_data_5y['Close'], label='Closing Price')
    plt.title(f'Historical Closing Prices - Last 5 Years of {ticker}')
    plt.xlabel('Date')
    plt.ylabel('Stock Price ($)')
    plt.legend()
    plt.grid()
    return plt

def main():
    st.title("Binomial Option Pricing Model")

    # Input fields for user parameters
    ticker_input = st.text_input("Stock Ticker Symbol(e.g. AMZN):", "AMZN")
    ticker = yf.Ticker(ticker_input)
    expiration_map = {
        "2 Weeks": 2/52,
        "1 Month": 1/12,
        "3 Months": 3/12,
        "6 Months": 0.5,
        "1 Year": 1,
        "2 Years": 2,
        "3 Years": 3,
        "5 Years": 5
    }
    expiration = st.selectbox("Choose the expiration Timeframe", ["2 Weeks", "1 Month", "3 Months", "6 Months", "1 Year", "2 Years", "3 Years", "5 Years"])
    exp_mapped = expiration_map[expiration]
    steps = st.slider("Number of Steps:", min_value=1, max_value=10000, value=6)

    treasury_bill = yf.Ticker('^IRX')
    pricing_model = Model(ticker, treasury_bill, exp_mapped)
    
    if ticker:
        current_price, _ , strike_list = pricing_model.fetch_option_data()
        strike = st.selectbox("Select Strike Price:", strike_list)
        if st.button("Calculate Option Prices"):
            if steps and strike_list and expiration:
                try:
                    # Fetch data and calculate option price
                    vol = np.std(pricing_model.historical_data()) * np.sqrt(252)  # Annualize the volatility
                    r = pricing_model.get_risk_free_rate()  # Risk-free rate
                    t_step = exp_mapped / steps  # Length of each time step

                    u, d = pricing_model.up_down_move(vol, t_step)

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
                    if steps < 100:
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


