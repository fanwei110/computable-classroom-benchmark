# 债券参数
face_value = 100.0
coupon_rate = 0.046
years = 7
ytm = 0.053

# 现金流：每年付息一次，到期还本
coupon = face_value * coupon_rate
cash_flows = [coupon] * (years - 1) + [coupon + face_value]

# 折现因子及现金流现值
pv_factors = [(1 + ytm) ** (-t) for t in range(1, years + 1)]
pv_cash_flows = [cf * pv for cf, pv in zip(cash_flows, pv_factors)]

price = sum(pv_cash_flows)

# 麦考利久期
weighted_time = [t * pv for t, pv in zip(range(1, years + 1), pv_cash_flows)]
macaulay_duration = sum(weighted_time) / price

# 修正久期
modified_duration = macaulay_duration / (1 + ytm)

# 凸性
convexity_numerator = [t * (t + 1) * pv for t, pv in zip(range(1, years + 1), pv_cash_flows)]
convexity = sum(convexity_numerator) / (price * (1 + ytm) ** 2)

# 输出字典
result = {
    'price': price,
    'macaulay_duration_years': macaulay_duration,
    'modified_duration_years': modified_duration,
    'convexity': convexity
}

result
