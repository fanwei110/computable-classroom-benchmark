# 债券参数
face_value = 100
coupon_rate = 0.046
yield_to_maturity = 0.053
years = 7

# 现金流
coupon = face_value * coupon_rate
cash_flows = [coupon] * (years - 1) + [coupon + face_value]

# 折现因子
discount_factors = [(1 + yield_to_maturity) ** -t for t in range(1, years + 1)]

# 现金流现值
present_values = [cf * df for cf, df in zip(cash_flows, discount_factors)]

# 价格
price = sum(present_values)

# 麦考利久期（年）
macaulay_duration_years = sum(t * pv for t, pv in enumerate(present_values, 1)) / price

# 修正久期（年）
modified_duration_years = macaulay_duration_years / (1 + yield_to_maturity)

# 凸性
convexity = sum(t * (t + 1) * pv for t, pv in enumerate(present_values, 1)) / (price * (1 + yield_to_maturity) ** 2)

# 结果字典
result = {
    'price': price,
    'macaulay_duration_years': macaulay_duration_years,
    'modified_duration_years': modified_duration_years,
    'convexity': convexity
}

result
