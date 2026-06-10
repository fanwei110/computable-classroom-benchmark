# PLANTED ERROR (conceptual): reports the MACAULAY duration under the
# modified-duration key (forgets the 1/(1+y) adjustment). No convention
# swap makes this correct. Expected: numeric_wrong.
face, cr, n, y = 100.0, 0.046, 7, 0.053

cfs = [(t, face * cr + (face if t == n else 0.0)) for t in range(1, n + 1)]
price = sum(cf / (1 + y) ** t for t, cf in cfs)
mac = sum(t * cf / (1 + y) ** t for t, cf in cfs) / price
cx = sum(t * (t + 1) * cf / (1 + y) ** (t + 2) for t, cf in cfs) / price

result = {
    "price": price,
    "macaulay_duration_years": mac,
    "modified_duration_years": mac,     # should be mac / (1 + y)
    "convexity": cx,
}
