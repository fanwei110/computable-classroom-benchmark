"""KP6 - Sharpe ratio and Brinson performance attribution.

Conventions: annualization by 252 (ann_252); sample std ddof=1 (ddof_1);
daily risk-free = annual / 252 (rf_simple_split); attribution is
Brinson-Hood-Beebower with a separate interaction term (attr_bhb).
"""

import numpy as np


def sharpe_annual(daily_returns, rf_annual=0.0, periods_per_year=252, ddof=1):
    """Annualized Sharpe ratio from a daily return series."""
    r = np.asarray(daily_returns, dtype=float)
    excess = r - rf_annual / periods_per_year
    return float(excess.mean() / excess.std(ddof=ddof) * np.sqrt(periods_per_year))


def rolling_sharpe_annual(daily_returns, window, rf_annual=0.0,
                          periods_per_year=252, ddof=1):
    """Rolling annualized Sharpe; returns an array aligned to window ends."""
    r = np.asarray(daily_returns, dtype=float)
    out = []
    for i in range(window, len(r) + 1):
        out.append(sharpe_annual(r[i - window:i], rf_annual, periods_per_year, ddof))
    return np.array(out)


def brinson_bhb(w_portfolio, w_benchmark, r_portfolio, r_benchmark):
    """Single-period BHB attribution. Returns (allocation, selection, interaction).

    allocation  = sum (w_p - w_b) * r_b
    selection   = sum w_b * (r_p - r_b)
    interaction = sum (w_p - w_b) * (r_p - r_b)
    """
    wp, wb = np.asarray(w_portfolio, float), np.asarray(w_benchmark, float)
    rp, rb = np.asarray(r_portfolio, float), np.asarray(r_benchmark, float)
    allocation = float(((wp - wb) * rb).sum())
    selection = float((wb * (rp - rb)).sum())
    interaction = float(((wp - wb) * (rp - rb)).sum())
    return allocation, selection, interaction
