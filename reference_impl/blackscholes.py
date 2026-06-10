"""KP4 - Black-Scholes pricing and Greeks (European, no dividends).

Conventions (opt_cont_comp): risk-free rate continuously compounded; time in
years; vega quoted per unit of volatility (dC/dsigma).
"""

import math

from scipy.stats import norm


def d1(s, k, sigma, r, t):
    return (math.log(s / k) + (r + 0.5 * sigma ** 2) * t) / (sigma * math.sqrt(t))


def d2(s, k, sigma, r, t):
    return d1(s, k, sigma, r, t) - sigma * math.sqrt(t)


def call_price(s, k, sigma, r, t):
    return s * norm.cdf(d1(s, k, sigma, r, t)) - k * math.exp(-r * t) * norm.cdf(d2(s, k, sigma, r, t))


def put_price(s, k, sigma, r, t):
    return k * math.exp(-r * t) * norm.cdf(-d2(s, k, sigma, r, t)) - s * norm.cdf(-d1(s, k, sigma, r, t))


def call_delta(s, k, sigma, r, t):
    return float(norm.cdf(d1(s, k, sigma, r, t)))


def vega(s, k, sigma, r, t):
    """dC/dsigma per unit of volatility (identical for calls and puts)."""
    return float(s * norm.pdf(d1(s, k, sigma, r, t)) * math.sqrt(t))


def call_price_change_vol_bump(s, k, sigma, r, t, dsigma):
    """Exact repricing for a volatility bump (course strict answer for the
    'vol rises one percentage point' scenario)."""
    return call_price(s, k, sigma + dsigma, r, t) - call_price(s, k, sigma, r, t)
