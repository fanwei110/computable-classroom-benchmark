# 参数
face_value = 100
coupon_rate = 0.046
coupon = face_value * coupon_rate  # 每年利息 4.6
ytm = 0.053
n = 7

# 计算价格（现值）
price = 0
for t in range(1, n + 1):
    price += coupon / (1 + ytm) ** t
price += face_value / (1 + ytm) ** n

# Macaulay 久期（单位：年）
macaulay = 0
for t in range(1, n + 1):
    macaulay += t * (coupon / (1 + ytm) ** t) / price
macaulay += n * (face_value / (1 + ytm) ** n) / price

# 修正久期
modified = macaulay / (1 + ytm)

# 凸性 (convexity)
convexity = 0
for t in range(1, n + 1):
    convexity += t * (t + 1) * (coupon / (1 + ytm) ** (t + 2)) / price
convexity += n * (n + 1) * (face_value / (1 + ytm) ** (n + 2)) / price

# 存入字典
result = {
    'price': round(price, 4),
    'macaulay_duration_years': round(macaulay, 4),
    'modified_duration_years': round(modified, 4),
    'convexity': round(convexity, 4)
}

result
