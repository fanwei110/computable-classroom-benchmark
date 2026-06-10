"""KP1 - Mean-variance portfolio theory (Markowitz).

Conventions: decimal units; fully-invested portfolios (weights sum to 1);
short sales allowed unless a task states otherwise; volatilities annualized.
"""

import numpy as np


def cov_from_vols_corr(vols, corr):
    """Covariance matrix from a vector of volatilities and a correlation matrix."""
    vols = np.asarray(vols, dtype=float)
    corr = np.asarray(corr, dtype=float)
    return np.outer(vols, vols) * corr


def two_asset_cov(sigma1, sigma2, rho):
    """2x2 covariance matrix for two assets."""
    return cov_from_vols_corr([sigma1, sigma2], [[1.0, rho], [rho, 1.0]])


def min_variance_weights(cov):
    """Global minimum-variance portfolio, closed form: w = Sigma^-1 1 / (1' Sigma^-1 1)."""
    cov = np.asarray(cov, dtype=float)
    ones = np.ones(cov.shape[0])
    x = np.linalg.solve(cov, ones)
    return x / x.sum()


def portfolio_vol(weights, cov):
    """Portfolio volatility w' Sigma w, square-rooted."""
    w = np.asarray(weights, dtype=float)
    cov = np.asarray(cov, dtype=float)
    return float(np.sqrt(w @ cov @ w))


def portfolio_variance(weights, cov):
    w = np.asarray(weights, dtype=float)
    cov = np.asarray(cov, dtype=float)
    return float(w @ cov @ w)


def frontier_vol_at_target(mus, cov, target_return):
    """Minimum volatility achievable at a given target expected return
    (equality-constrained Markowitz, shorting allowed). Closed form via
    the standard A,B,C,D scalars."""
    mus = np.asarray(mus, dtype=float)
    cov = np.asarray(cov, dtype=float)
    ones = np.ones(len(mus))
    inv = np.linalg.inv(cov)
    A = ones @ inv @ ones
    B = ones @ inv @ mus
    C = mus @ inv @ mus
    D = A * C - B * B
    var = (A * target_return ** 2 - 2 * B * target_return + C) / D
    return float(np.sqrt(var))
