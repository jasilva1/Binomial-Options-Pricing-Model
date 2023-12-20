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

Try the model yourself:
- Download the multi_step_model.py
- Install streamlit with " pip install streamlit " (If not already installed)
- Lastly, run with " streamlit run multi_step_model.py "

https://github.com/jasilva1/Binomial-Options-Pricing-Model/assets/134011187/794e0fc0-ffa9-4f94-9cee-864d36fddc60

https://github.com/jasilva1/Binomial-Options-Pricing-Model/assets/134011187/2fcb510e-ed61-4c16-a2c9-62ce68b3d3a5
