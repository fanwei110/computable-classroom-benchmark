import numpy as np

# 给定参数
face_value = 100.0
coupon_rate = 0.046
years = 7
yield_rate = 0.053

# 现金流：每年付息一次，最后一年加上本金
t = np.arange(1, years + 1)
cf = np.full(years, coupon_rate * face_value)
cf[-1] += face_value

# 现值
discount = (1 + yield_rate) ** t
pv = cf / discount

# 价格
price = np.sum(pv)

# 麦考利久期（年）
macaulay_duration = np.sum(t * pv) / price

# 修正久期（年）
modified_duration = macaulay_duration / (1 + yield_rate)

# 凸性
convexity = np.sum(t * (t + 1) * pv) / (price * (1 + yield_rate) ** 2)

result = {
    'price': price,
    'macaulay_duration_years': macaulay_duration,
    'modified_duration_years': modified_duration,
    'convexity': convexity
}

result
