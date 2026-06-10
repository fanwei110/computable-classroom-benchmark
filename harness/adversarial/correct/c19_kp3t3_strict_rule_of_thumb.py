# T3 solution using the course rule of thumb (first-order modified duration).
# Expected verdict: correct at the STRICT tier.
face, cr, n, y, dy = 100.0, 0.046, 7, 0.053, 0.008

cfs = [(t, face * cr + (face if t == n else 0.0)) for t in range(1, n + 1)]
price = sum(cf / (1 + y) ** t for t, cf in cfs)
mac = sum(t * cf / (1 + y) ** t for t, cf in cfs) / price
dmod = mac / (1 + y)

result = {"price_drop_pct": dmod * dy}
