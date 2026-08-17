import numpy as np

# 债券参数
face_value = 100.0          # 面值
annual_coupon_rate = 0.046  # 年票息率
years_to_maturity = 7       # 剩余期限（年）
yield_to_maturity = 0.053   # 收益率（年化）
coupon_frequency = 2        # 每年付息次数（半年付息）

# 计算每期票息
coupon_payment = face_value * annual_coupon_rate / coupon_frequency

# 生成现金流
cash_flows = np.full(years_to_maturity * coupon_frequency, coupon_payment)
cash_flows[-1] += face_value  # 最后一期包含面值

# 计算每期的贴现因子
periods = np.arange(1, years_to_maturity * coupon_frequency + 1)
discount_factors = (1 + yield_to_maturity / coupon_frequency) ** (-periods)

# 1. 计算债券价格（现金流贴现之和）
price = np.sum(cash_flows * discount_factors)

# 2. 计算麦考利久期和修正久期
weighted_cash_flows = cash_flows * discount_factors * periods
macaulay_duration_periods = np.sum(weighted_cash_flows) / price
macaulay_duration_years = macaulay_duration_periods / coupon_frequency

# 修正久期 = 麦考利久期 / (1 + y/f)
modified_duration_years = macaulay_duration_years / (1 + yield_to_maturity / coupon_frequency)

# 3. 计算凸性
convexity_periods = np.sum(cash_flows * discount_factors * periods * (periods + 1)) / price
convexity = convexity_periods / (coupon_frequency ** 2 * (1 + yield_to_maturity / coupon_frequency) ** 2)

# 4. 存入结果字典
result = {
    'price': price,
    'macaulay_duration_years': macaulay_duration_years,
    'modified_duration_years': modified_duration_years,
    'convexity': convexity
}

# 输出结果（可选，方便调试）
print(result)
