import numpy as np

# 债券参数
face_value = 100.0      # 面值
coupon_rate = 0.046     # 票息率（4.6%）
years_to_maturity = 7   # 期限（年）
ytm = 0.053             # 到期收益率（5.3%）

# 计算每年现金流（票息和到期面值）
annual_coupon = face_value * coupon_rate
cash_flows = np.array([annual_coupon] * years_to_maturity)
cash_flows[-1] += face_value  # 最后一期包含面值

# 1. 计算价格（现金流贴现之和）
discount_factors = (1 + ytm) ** np.arange(1, years_to_maturity + 1)
price = np.sum(cash_flows / discount_factors)

# 2. 计算麦考利久期和修正久期
time_periods = np.arange(1, years_to_maturity + 1)
weighted_cash_flows = time_periods * cash_flows / discount_factors
macaulay_duration = np.sum(weighted_cash_flows) / price
modified_duration = macaulay_duration / (1 + ytm)

# 3. 计算凸性
convexity_numerator = np.sum(time_periods * (time_periods + 1) * cash_flows / (discount_factors * (1 + ytm)**2))
convexity = convexity_numerator / price

# 结果存储
result = {
    'price': price,
    'macaulay_duration_years': macaulay_duration,
    'modified_duration_years': modified_duration,
    'convexity': convexity
}

# 输出结果（可选，用于验证）
print(result)
