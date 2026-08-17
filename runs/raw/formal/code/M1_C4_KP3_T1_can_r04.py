import numpy as np

# 债券参数
face_value = 100.0
coupon_rate = 0.046
years_to_maturity = 7
yield_to_maturity = 0.053

# 计算每年票息
annual_coupon = face_value * coupon_rate

# 现金流：每年票息 + 到期面值
cash_flows = np.array([annual_coupon] * years_to_maturity)
cash_flows[-1] += face_value  # 最后一期加上面值

# 1. 计算价格：现金流贴现之和
discount_factors = (1 + yield_to_maturity) ** np.arange(1, years_to_maturity + 1)
price = np.sum(cash_flows / discount_factors)

# 2. 计算麦考利久期
time_periods = np.arange(1, years_to_maturity + 1)
weighted_cash_flows = time_periods * cash_flows / discount_factors
macaulay_duration = np.sum(weighted_cash_flows) / price

# 修正久期
modified_duration = macaulay_duration / (1 + yield_to_maturity)

# 3. 计算凸性
convexity_numerator = np.sum(time_periods * (time_periods + 1) * cash_flows / (discount_factors * (1 + yield_to_maturity)**2))
convexity = convexity_numerator / price

# 结果存入字典
result = {
    'price': price,
    'macaulay_duration_years': macaulay_duration,
    'modified_duration_years': modified_duration,
    'convexity': convexity
}

# 输出结果（可选，用于验证）
print(result)
