"""KP3 - Bond pricing, duration, convexity.

Conventions (bond_annual_comp): yields quoted with annual compounding; annual
coupons; valuation at a coupon date (no accrued interest). Durations in years.
Convexity = sum[t(t+1)CF_t/(1+y)^(t+2)] / P, in years^2.
"""


def cashflows(face, coupon_rate, n_years):
    """Annual cashflows of a bullet bond: coupon each year, face at maturity."""
    c = face * coupon_rate
    return [(t, c + (face if t == n_years else 0.0)) for t in range(1, n_years + 1)]


def price(face, coupon_rate, n_years, ytm):
    return sum(cf / (1 + ytm) ** t for t, cf in cashflows(face, coupon_rate, n_years))


def macaulay_duration(face, coupon_rate, n_years, ytm):
    p = price(face, coupon_rate, n_years, ytm)
    return sum(t * cf / (1 + ytm) ** t for t, cf in cashflows(face, coupon_rate, n_years)) / p


def modified_duration(face, coupon_rate, n_years, ytm):
    return macaulay_duration(face, coupon_rate, n_years, ytm) / (1 + ytm)


def convexity(face, coupon_rate, n_years, ytm):
    p = price(face, coupon_rate, n_years, ytm)
    return sum(t * (t + 1) * cf / (1 + ytm) ** (t + 2)
               for t, cf in cashflows(face, coupon_rate, n_years)) / p


def price_change_duration(face, coupon_rate, n_years, ytm, dy):
    """First-order approximation dP/P = -D_mod * dy (course rule of thumb)."""
    return -modified_duration(face, coupon_rate, n_years, ytm) * dy


def price_change_duration_convexity(face, coupon_rate, n_years, ytm, dy):
    """Second-order approximation dP/P = -D_mod*dy + 0.5*Cx*dy^2."""
    return (-modified_duration(face, coupon_rate, n_years, ytm) * dy
            + 0.5 * convexity(face, coupon_rate, n_years, ytm) * dy ** 2)


def price_change_exact(face, coupon_rate, n_years, ytm, dy):
    """Exact relative repricing (P(y+dy) - P(y)) / P(y)."""
    p0 = price(face, coupon_rate, n_years, ytm)
    p1 = price(face, coupon_rate, n_years, ytm + dy)
    return (p1 - p0) / p0
