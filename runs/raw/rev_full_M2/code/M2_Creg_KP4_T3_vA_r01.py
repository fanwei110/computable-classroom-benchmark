import numpy as np
from scipy.stats import norm

def bs_call_price(S, K, T, r, sigma):
    """
    Calculate Black-Scholes call option price.
    """
    if T <= 0:
        return max(S - K, 0)
    if sigma <= 0:
        # Forward price with deterministic present value
        return max(S - K * np.exp(-r * T), 0)
    
    d1 = (np.log(S / K) + (r + 0.5 * sigma**2) * T) / (sigma * np.sqrt(T))
    d2 = d1 - sigma * np.sqrt(T)
    price = S * norm.cdf(d1) - K * np.exp(-r * T) * norm.cdf(d2)
    return price

# ---------- market parameters ----------
S = 103.7               # underlying spot price
K = 97.5                # strike price
sigma_current = 0.276   # current implied volatility (27.6%)
r = 0.043               # risk-free interest rate (4.3%)
T = 0.58                # time to expiration in years

# ---------- compute price change ----------
price_current = bs_call_price(S, K, T, r, sigma_current)
price_new     = bs_call_price(S, K, T, r, sigma_current + 0.01)  # volatility up 1 percentage point
price_change  = price_new - price_current

# ---------- output ----------
result = {
    'price_change': price_change
}

print(result)
