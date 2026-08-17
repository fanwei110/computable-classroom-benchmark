import numpy as np
from scipy.optimize import newton

# 债券参数
face_value = 100.0          # 面值
coupon_rate = 0.046         # 票面利率（年化）
years_to_maturity = 7       # 期限（年）
ytm = 0.053                 # 到期收益率（年化）
coupon_frequency = 2        # 每年付息次数（半年付息）

# 计算每期现金流
periods = years_to_maturity * coupon_frequency
coupon_payment = (face_value * coupon_rate) / coupon_frequency
cash_flows = np.full(periods, coupon_payment)
cash_flows[-1] += face_value  # 最后一期包含本金

# 1. 计算债券价格（现金流贴现之和）
periodic_ytm = ytm / coupon_frequency
discount_factors = np.array([(1 + periodic_ytm) ** (-t) for t in range(1, periods + 1)])
price = np.sum(cash_flows * discount_factors)

# 2. 计算 Macaulay 久期和修正久期
weighted_cash_flows = cash_flows * discount_factors * np.arange(1, periods + 1)
macaulay_duration_periods = np.sum(weighted_cash_flows) / price
macaulay_duration_years = macaulay_duration_periods / coupon_frequency
modified_duration_years = macaulay_duration_years / (1 + ytm / coupon_frequency)

# 3. 计算凸性
weighted_cash_flows_convexity = cash_flows * discount_factors * np.arange(1, periods + 1) * (np.arange(1, periods + 1) + 1)
convexity_periods = np.sum(weighted_cash_flows_convexity) / price
convexity = convexity_periods / (coupon_frequency ** 2 * (1 + periodic_ytm) ** 2)

# 4. 填充结果字典
result = {
    'price': price,
    'macaulay_duration_years': macaulay_duration_years,
    'modified_duration_years': modified_duration_years,
    'convexity': convexity
}

# 输出结果（可选，便于调试）
print("债券定价结果:")
print(f"价格: {price:.4f}")
print(f"Macaulay 久期（年）: {macaulay_duration_years:.4f}")
print(f"修正久期（年）: {modified_duration_years:.4f}")
print(f"凸性: {convexity:.4f}")
