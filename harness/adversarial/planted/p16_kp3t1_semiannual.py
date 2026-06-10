# PLANTED ERROR (conventional): treats the stated ANNUAL coupon bond as a
# SEMIANNUAL payer with y/2 per period - a payment/compounding convention
# swap the task explicitly pins down. Expected: numeric_wrong.
face, cr, n_years, y = 100.0, 0.046, 7, 0.053

periods = n_years * 2
cps = face * cr / 2
yp = y / 2

cfs = [(t, cps + (face if t == periods else 0.0)) for t in range(1, periods + 1)]
price = sum(cf / (1 + yp) ** t for t, cf in cfs)
mac_periods = sum(t * cf / (1 + yp) ** t for t, cf in cfs) / price
mac_years = mac_periods / 2
mod_years = mac_years / (1 + yp)
cx_periods = sum(t * (t + 1) * cf / (1 + yp) ** (t + 2) for t, cf in cfs) / price
cx_years = cx_periods / 4

result = {
    "price": price,
    "macaulay_duration_years": mac_years,
    "modified_duration_years": mod_years,
    "convexity": cx_years,
}
