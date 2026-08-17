import numpy as np
from scipy.stats import norm
import json

def black_scholes_call(S, K, T, r, sigma, q=0.0):
    """
    Black-Scholes European call option pricing and Greeks.
    Assumes continuous compounding and no dividends (q=0).
    """
    d1 = (np.log(S / K) + (r - q + 0.5 * sigma**2) * T) / (sigma * np.sqrt(T))
    d2 = d1 - sigma * np.sqrt(T)
    
    # Price
    call_price = S * np.exp(-q * T) * norm.cdf(d1) - K * np.exp(-r * T) * norm.cdf(d2)
    
    # Delta
    call_delta = np.exp(-q * T) * norm.cdf(d1)
    
    # Vega (sensitivity to 1% change in volatility, i.e., derivative w.r.t. sigma)
    # Standard formula gives vega for a 1 unit (100%) change in sigma.
    # Often market convention expresses vega per 1 percentage point; we return the raw derivative.
    call_vega = S * np.exp(-q * T) * norm.pdf(d1) * np.sqrt(T)
    
    return call_price, call_delta, call_vega

# Given parameters
S0 = 103.7      # underlying price
K = 97.5        # strike price
sigma = 0.276   # implied volatility
r = 0.043       # risk-free rate
T = 0.58        # time to expiration in years
q = 0.0         # dividend yield

price, delta, vega = black_scholes_call(S0, K, T, r, sigma, q)

# Store results as required
result = {
    'call_price': price,
    'call_delta': delta,
    'call_vega': vega
}

# Print for classroom screen projection
print("Black-Scholes European Call Option")
print(f"Underlying price (S): {S0}")
print(f"Strike price (K)    : {K}")
print(f"Implied volatility  : {sigma}")
print(f"Risk-free rate (r)  : {r}")
print(f"Time to expiry (T)  : {T} years")
print(f"Dividend yield (q)  : {q}")
print("-" * 40)
print(f"Call Price : {price:.6f}")
print(f"Call Delta : {delta:.6f}")
print(f"Call Vega  : {vega:.6f}  (per 1 unit change in sigma)")

# Return dictionary (can be used by other code)
# In interactive session, result will be available
if __name__ == "__main__":
    # Optionally pretty print the dictionary
    print("\nResult dictionary:")
    print(json.dumps(result, indent=4, default=float))
