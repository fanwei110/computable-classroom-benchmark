import numpy as np
from scipy.stats import norm

def black_scholes_call(S, K, T, r, sigma):
    """
    Black-Scholes European call option pricing and Greeks.
    S     : spot price
    K     : strike price
    T     : time to maturity (years)
    r     : risk-free rate (annualized, continuous compounding)
    sigma : volatility (annualized)
    Returns: price, delta, vega (vega = dPrice/dSigma)
    """
    # 1. d1 and d2
    d1 = (np.log(S / K) + (r + 0.5 * sigma**2) * T) / (sigma * np.sqrt(T))
    d2 = d1 - sigma * np.sqrt(T)
    
    # 2. Price and Delta
    price = S * norm.cdf(d1) - K * np.exp(-r * T) * norm.cdf(d2)
    delta = norm.cdf(d1)
    
    # 3. Vega: derivative w.r.t. sigma (not divided by 100)
    vega = S * norm.pdf(d1) * np.sqrt(T)
    
    return price, delta, vega

# Input parameters
S = 103.7
K = 97.5
T = 0.58
r = 0.043
sigma = 0.276

call_price, call_delta, call_vega = black_scholes_call(S, K, T, r, sigma)

result = {
    'call_price': call_price,
    'call_delta': call_delta,
    'call_vega': call_vega      # mathematical vega (change per unit volatility)
}

# Display results clearly
for key, value in result.items():
    print(f"{key}: {value:.6f}")

# If you prefer vega per 1% volatility change, uncomment the following:
# result['call_vega_1pct'] = call_vega / 100.0
# print(f"call_vega (per 1%): {result['call_vega_1pct']:.6f}")
