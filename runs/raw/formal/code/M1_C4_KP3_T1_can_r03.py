import numpy as np

# 债券参数
face_value = 100.0
coupon_rate = 0.046
years_to_maturity = 7
yield_to_maturity = 0.053

# 计算每年票息
annual_coupon = face_value * coupon_rate

# 1. 计算价格：现金流贴现之和
cash_flows = np.array([annual_coupon] * years_to_maturity + [face_value])
time_periods = np.arange(1, years_to_maturity + 2)
discount_factors = (1 + yield_to_maturity) ** time_periods
price = np.sum(cash_flows / discount_factors)

# 2. 计算麦考利久期
weighted_cash_flows = cash_flows * time_periods
present_values = weighted_cash_flows / discount_factors
macaulay_duration_years = np.sum(present_values) / price

# 修正久期
modified_duration_years = macaulay_duration_years / (1 + yield_to_maturity)

# 3. 计算凸性
convexity_numerator = cash_flows * time_periods * (time_periods + 1)
convexity_denominator = (1 + yield_to_maturity) ** (time_periods + 2)
convexity = np.sum(convexity_numerator / convexity_denominator) / price

# 4. 填充结果字典
result = {
    'price': price,
    'macaulay_duration_years': macaulay_duration_years,
    'modified_duration_years': modified_duration_years,
    'convexity': convexity
}

# 输出结果（可选，用于验证）
print(result)
