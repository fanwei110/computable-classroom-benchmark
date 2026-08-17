import numpy as np

# 债券参数
face_value = 100.0          # 面值
coupon_rate = 0.046         # 票息率 4.6%
years_to_maturity = 7       # 期限 7 年
ytm = 0.053                 # 到期收益率 5.3%

# 1. 计算价格：现金流贴现之和
cash_flows = np.full(years_to_maturity, face_value * coupon_rate)  # 每年票息
cash_flows[-1] += face_value                                       # 最后一期加上面值
discount_factors = (1 + ytm) ** np.arange(1, years_to_maturity + 1)
price = np.sum(cash_flows / discount_factors)

# 2. 计算麦考利久期
time_weights = np.arange(1, years_to_maturity + 1)
weighted_cash_flows = time_weights * cash_flows
macaulay_duration = np.sum(weighted_cash_flows / discount_factors) / price

# 修正久期
modified_duration = macaulay_duration / (1 + ytm)

# 3. 计算凸性
convexity_weights = time_weights * (time_weights + 1)
convexity_numerator = np.sum(convexity_weights * cash_flows / (discount_factors * (1 + ytm)**2))
convexity = convexity_numerator / price

# 4. 填充结果字典
result = {
    'price': price,
    'macaulay_duration_years': macaulay_duration,
    'modified_duration_years': modified_duration,
    'convexity': convexity
}
