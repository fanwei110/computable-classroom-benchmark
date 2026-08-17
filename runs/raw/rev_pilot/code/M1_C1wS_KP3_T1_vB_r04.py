import numpy as np

# 债券参数
face_value = 100.0          # 面值
annual_coupon_rate = 0.046  # 年票息率
years_to_maturity = 7       # 剩余期限（年）
yield_to_maturity = 0.053   # 收益率（年化）
coupon_frequency = 2        # 每年付息次数（半年付息）

# 计算每期票息
coupon_payment = face_value * annual_coupon_rate / coupon_frequency

# 生成现金流时间点和现金流金额
cash_flow_times = np.arange(1, years_to_maturity * coupon_frequency + 1) / coupon_frequency
cash_flows = np.full(years_to_maturity * coupon_frequency, coupon_payment)
cash_flows[-1] += face_value  # 最后一期包含面值

# 1. 计算债券价格（现金流贴现之和）
discount_factors = (1 + yield_to_maturity / coupon_frequency) ** (-cash_flow_times * coupon_frequency)
price = np.sum(cash_flows * discount_factors)

# 2. 计算麦考利久期和修正久期
weighted_cash_flows = cash_flows * cash_flow_times * discount_factors
macaulay_duration_years = np.sum(weighted_cash_flows) / price
modified_duration_years = macaulay_duration_years / (1 + yield_to_maturity / coupon_frequency)

# 3. 计算凸性
convexity_weights = cash_flows * cash_flow_times * (cash_flow_times + 1 / coupon_frequency) * discount_factors
convexity = np.sum(convexity_weights) / (price * (1 + yield_to_maturity / coupon_frequency) ** 2)

# 将结果存入 result 字典
result = {
    'price': price,
    'macaulay_duration_years': macaulay_duration_years,
    'modified_duration_years': modified_duration_years,
    'convexity': convexity
}

# 输出结果（可选，便于调试）
print(result)
