# Binomial-Options-Pricing-Model

I've uploaded code for both the one-step core model and the multi-step model. The one-step model was simply a starting point and helped me understand exactly what was going on within the model. The multi-step model builds upon the foundational principles of the one-step model and extends it to a more complex and realistic scenario. The multi-step model allows for a more detailed simulation of option price evolution over time, providing a closer approximation to real-world option pricing dynamics. The model uses the 13-week treasury bill ^IRX to calculate the risk-free rate. The risk-free rate change is based on the timeframe, see the "get_risk_free_rate" function and "expiration_map" dictionary for more detail on when and how it changes.

User Inputs:
- Stock Ticker Symbol
- Time till expiration
- Number of Steps
- Strike Price

Outputs:
- Calculated Call Option Price
- Calculated Put Option Price
- Stock Price Chart over the past 5 Years
- Binomial Tree Visualization (If steps < 100)

Libraries Used:
- numpy
- yfinance
- math
- streamlit
- matplotlib.pyplot

Functions:
- get_risk_free_rate(): Calculates the rate of return of an investment with zero risk
- get_data(): Returns the historical closing prices of the specified ticker symbol over the past year
- fetch_option_data(): Returns the Options data(Option chain data, calls/puts), Strike Prices, and the current price of the specified ticker symbol
- up_down_move(): Calculates the upward and downward movement factors (u and d) used in the binomial tree, based on the volatility of the stock and the time step length
- historical_data(): Calculates the logarithmic returns of the historical closing prices from Yahoo Finance
- build_binomial_tree(): Constructs a binomial tree for the asset's potential future prices, starting from the current price and applying the calculated up and down factors (u and d) repeatedly for a given number of steps.
- calculate_call_option_values(): Computes the values of call options at each node of the binomial tree by working backwards from the expiration values, and discounting expected future values based on the risk-free rate
- calculate_put_option_values(): Calculates the values of the put options similarly to the "calculate_call_option_values" function
- plot_binomial_tree(): Utilizes matplotlib to build the plot of the binomial tree with x-axis=Steps and y-axis=Price
- plot_historical_data(): Utilized matplotlib to plot the closing prices of the specified ticker symbol over the past year
  

Try the model yourself:
- Download the multi_step_model.py
- Install streamlit with " pip install streamlit " (If not already installed)
- Lastly, run with " streamlit run multi_step_model.py "

https://github.com/jasilva1/Binomial-Options-Pricing-Model/assets/134011187/794e0fc0-ffa9-4f94-9cee-864d36fddc60

https://github.com/jasilva1/Binomial-Options-Pricing-Model/assets/134011187/2fcb510e-ed61-4c16-a2c9-62ce68b3d3a5
