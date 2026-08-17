import numpy as np

# 参数
face_value = 100
coupon_rate = 0.046
ytm = 0.053
years = 7
frequency = 1  # 年付

# 计算票息和现金流
coupon = face_value * coupon_rate
cash_flows = np.array([coupon] * years + [face_value + coupon])

# 计算贴现因子
discount_factors = np.array([(1 + ytm) ** t for t in range(1, years + 2)])

# 计算价格
price = np.sum(cash_flows / discount_factors)

# 计算麦考利久期
weights = np.array([t for t in range(1, years + 1)] + [years])
macaulay_duration = np.sum(weights * cash_flows / discount_factors) / price / frequency

# 计算修正久期
modified_duration = macaulay_duration / (1 + ytm / frequency)

# 计算凸性
convexity_weights = np.array([t * (t + 1) for t in range(1, years + 1)] + [years * (years + 1)])
convexity = np.sum(convexity_weights * cash_flows / (discount_factors ** 2)) / price / (1 + ytm / frequency) ** 2 / frequency ** 2

# 存入结果字典
result = {
    'price': round(price, 4),
    'macaulay_duration_years': round(macaulay_duration, 4),
    'modified_duration_years': round(modified_duration, 4),
    'convexity': round(convexity, 4)
}

print(result)
