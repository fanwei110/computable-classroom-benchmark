import numpy as np

# 债券参数
face_value = 100  # 面值
coupon_rate = 0.046  # 票息率
years_to_maturity = 7  # 期限（年）
ytm = 0.053  # 到期收益率（年化）
coupon_frequency = 1  # 每年付息一次（假设）

# 计算每期票息
coupon_payment = face_value * coupon_rate / coupon_frequency

# 生成现金流：每期票息 + 到期本金
cash_flows = np.array([coupon_payment] * years_to_maturity)
cash_flows[-1] += face_value  # 最后一期加上面值

# 计算价格：现金流的贴现值之和
periods = np.arange(1, years_to_maturity + 1)
discount_factors = (1 + ytm / coupon_frequency) ** (-periods)
price = np.sum(cash_flows * discount_factors)

# 计算麦考利久期：加权平均到期时间
weighted_cash_flows = cash_flows * periods * discount_factors
macaulay_duration = np.sum(weighted_cash_flows) / price / coupon_frequency

# 计算修正久期：麦考利久期 / (1 + ytm / frequency)
modified_duration = macaulay_duration / (1 + ytm / coupon_frequency)

# 计算凸性：二阶导数 / 价格
convexity_numerator = cash_flows * periods * (periods + 1) * discount_factors
convexity = np.sum(convexity_numerator) / (price * (1 + ytm / coupon_frequency) ** 2) / (coupon_frequency ** 2)

# 结果存入字典
result = {
    'price': price,
    'macaulay_duration_years': macaulay_duration,
    'modified_duration_years': modified_duration,
    'convexity': convexity
}

# 输出结果（可选，便于调试）
print(result)
