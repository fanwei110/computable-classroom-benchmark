import numpy as np

# 债券参数
face_value = 100.0
coupon_rate = 0.046
years_to_maturity = 7
ytm = 0.053

# 1. 计算价格：每年票息贴现 + 到期面值贴现
cashflows = np.full(years_to_maturity, face_value * coupon_rate)  # 每年票息
cashflows[-1] += face_value  # 最后一年加上面值
discount_factors = (1 + ytm) ** np.arange(1, years_to_maturity + 1)
price = np.sum(cashflows / discount_factors)

# 2. 麦考利久期（年）
t = np.arange(1, years_to_maturity + 1)
macaulay_duration = np.sum(t * cashflows / discount_factors) / price

# 修正久期
modified_duration = macaulay_duration / (1 + ytm)

# 3. 凸性（年平方）
convexity = np.sum(t * (t + 1) * cashflows / (1 + ytm) ** (t + 2)) / price

# 4. 填充 result 字典
result = {
    'price': round(price, 6),
    'macaulay_duration_years': round(macaulay_duration, 6),
    'modified_duration_years': round(modified_duration, 6),
    'convexity': round(convexity, 6)
}

# 输出结果（教师投屏可见）
print(result)
