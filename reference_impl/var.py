"""KP5 - Value-at-Risk (parametric and historical).

Conventions: VaR reported as a positive loss amount (var_positive); zero-mean
assumption at short horizons; one-tailed z = Phi^-1(confidence);
de-annualization by sqrt(252) (ann_252); historical VaR via linearly
interpolated empirical percentile (hist_var_linear).
"""

import numpy as np
from scipy.stats import norm


def parametric_var(position_value, sigma_annual, confidence=0.95,
                   horizon_days=1, periods_per_year=252):
    """Parametric (delta-normal) VaR, positive loss amount."""
    sigma_daily = sigma_annual / np.sqrt(periods_per_year)
    z = norm.ppf(confidence)
    return float(position_value * z * sigma_daily * np.sqrt(horizon_days))


def historical_var(daily_returns, position_value, confidence=0.95):
    """Historical one-day VaR: positive loss at the (1-confidence) percentile
    of the P&L distribution, linearly interpolated (numpy default)."""
    pnl = np.asarray(daily_returns, dtype=float) * position_value
    return float(-np.percentile(pnl, (1 - confidence) * 100))
