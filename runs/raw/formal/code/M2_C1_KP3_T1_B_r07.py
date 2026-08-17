# ç»å®åæ°
face_value = 100
coupon_rate = 0.046
years = 7
ytm = 0.053
coupon = face_value * coupon_rate

# è®¡ç®åæç°éæµç°å¼
pv_cf = []
for t in range(1, years + 1):
    cf = coupon + (face_value if t == years else 0)
    pv = cf / (1 + ytm) ** t
    pv_cf.append(pv)

price = sum(pv_cf)

# éº¦èå©ä¹æ
weighted_sum = sum((t + 1) * pv for t, pv in enumerate(pv_cf))
macaulay_duration = weighted_sum / price

# ä¿®æ­£ä¹æ
modified_duration = macaulay_duration / (1 + ytm)

# å¸æ§
convexity_sum = sum((t + 1) * (t + 2) * pv for t, pv in enumerate(pv_cf))
convexity = convexity_sum / (price * (1 + ytm) ** 2)

# å­å¨ç»æ
result = {
    'price': round(price, 4),
    'macaulay_duration_years': round(macaulay_duration, 4),
    'modified_duration_years': round(modified_duration, 4),
    'convexity': round(convexity, 4)
}

result
