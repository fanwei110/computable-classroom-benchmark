# 计算债券价格、麦考利久期、修正久期与凸性

face_value = 100.0
coupon_rate = 0.046
ytm = 0.053
years = 7

# 各期现金流
cfs = [face_value * coupon_rate] * (years - 1)
cfs.append(face_value * coupon_rate + face_value)

# 贴现因子
discounts = [(1 + ytm) ** (-t) for t in range(1, years + 1)]

# 现金流现值
pv_cfs = [cf * d for cf, d in zip(cfs, discounts)]

price = sum(pv_cfs)

# 麦考利久期
weighted_sum = sum(t * pv for t, pv in zip(range(1, years + 1), pv_cfs))
macaulay_duration = weighted_sum / price

# 修正久期
modified_duration = macaulay_duration / (1 + ytm)

# 凸性
convexity_sum = sum(t * (t + 1) * pv for t, pv in zip(range(1, years + 1), pv_cfs))
convexity = convexity_sum / (price * (1 + ytm) ** 2)

result = {
    'price': price,
    'macaulay_duration_years': macaulay_duration,
    'modified_duration_years': modified_duration,
    'convexity': convexity
}

result
