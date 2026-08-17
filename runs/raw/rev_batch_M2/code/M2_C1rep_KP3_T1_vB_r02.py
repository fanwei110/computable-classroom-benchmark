# 给定债券参数
face_value = 100
coupon_rate = 0.046
years = 7
yield_to_maturity = 0.053

# 现金流和折现计算
cash_flows = [coupon_rate * face_value] * (years - 1) + [coupon_rate * face_value + face_value]
discount_factors = [(1 + yield_to_maturity) ** -t for t in range(1, years + 1)]
present_values = [cf * df for cf, df in zip(cash_flows, discount_factors)]

# 价格
price = sum(present_values)

# 麦考利久期
macaulay_duration = sum(t * pv for t, pv in enumerate(present_values, start=1)) / price

# 修正久期
modified_duration = macaulay_duration / (1 + yield_to_maturity)

# 凸性
convexity = sum(t * (t + 1) * pv for t, pv in enumerate(present_values, start=1)) / (price * (1 + yield_to_maturity) ** 2)

# 存入字典
result = {
    'price': price,
    'macaulay_duration_years': macaulay_duration,
    'modified_duration_years': modified_duration,
    'convexity': convexity
}

# 打印结果（可选，用于验证）
for key, value in result.items():
    print(f"{key}: {value:.6f}")
