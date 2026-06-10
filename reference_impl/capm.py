"""KP2 - CAPM and the security market line.

Conventions: decimal units; converting an annual rate to a shorter period
uses simple division (rf_simple_split in course_conventions.md).
"""


def expected_return(rf, beta, expected_market_return):
    """CAPM: E[Ri] = rf + beta * (E[Rm] - rf)."""
    return rf + beta * (expected_market_return - rf)


def alpha(realized_return, rf, beta, expected_market_return):
    """Jensen-style alpha versus the SML prediction."""
    return realized_return - expected_return(rf, beta, expected_market_return)


def capm_period_return(rf_annual, beta, market_return_period, periods_per_year):
    """CAPM prediction over a sub-annual period: the annual risk-free rate is
    converted by simple division (course convention rf_simple_split)."""
    rf_period = rf_annual / periods_per_year
    return rf_period + beta * (market_return_period - rf_period)
