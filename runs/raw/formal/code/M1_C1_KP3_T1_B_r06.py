import numpy as np

# 参数
face_value = 100
coupon_rate = 0.046
ytm = 0.053
maturity = 7
coupon = face_value * coupon_rate

# 计算价格
price = sum([coupon / (1 + ytm)**t for t in range(1, maturity + 1)]) + face_value / (1 + ytm)**maturity

# 计算麦考利久期
macaulay_duration = sum([t * coupon / (1 + ytm)**t for t in range(1, maturity + 1)]) + maturity * face_value / (1 + ytm)**maturity
macaulay_duration /= price
macaulay_duration_years = macaulay_duration

# 计算修正久期
modified_duration_years = macaulay_duration / (1 + ytm)

# 计算凸性
convexity = sum([t * (t + 1) * coupon / (1 + ytm)**(t + 2) for t in range(1, maturity + 1)]) + maturity * (maturity + 1) * face_value / (1 + ytm)**(maturity + 2)
convexity /= price

# 存入字典
result = {
    'price': round(price, 4),
    'macaulay_duration_years': round(macaulay_duration_years, 4),
    'modified_duration_years': round(modified_duration_years, 4),
    'convexity': round(convexity, 4)
}

print(result)
