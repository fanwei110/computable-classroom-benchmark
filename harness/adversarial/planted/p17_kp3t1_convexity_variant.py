# PLANTED ERROR (conventional, boundary exemplar): uses the convexity
# variant WITHOUT the (1+y)^2 divisor (sum t(t+1)CF/(1+y)^t / P). The course
# pins the standard definition. Everything else is correct.
# Expected: numeric_wrong (convexity key fails).
face, cr, n, y = 100.0, 0.046, 7, 0.053

cfs = [(t, face * cr + (face if t == n else 0.0)) for t in range(1, n + 1)]
price = sum(cf / (1 + y) ** t for t, cf in cfs)
mac = sum(t * cf / (1 + y) ** t for t, cf in cfs) / price
cx_variant = sum(t * (t + 1) * cf / (1 + y) ** t for t, cf in cfs) / price

result = {
    "price": price,
    "macaulay_duration_years": mac,
    "modified_duration_years": mac / (1 + y),
    "convexity": cx_variant,
}
