import numpy as np

# 债券参数
face_value = 100.0          # 面值
coupon_rate = 0.046         # 票息率 4.6%
maturity_years = 7          # 期限 7 年
ytm = 0.053                 # 到期收益率 5.3%

# 现金流时间向量
t = np.arange(1, maturity_years + 1)   # 1,2,...,7

# 每年票息现金流
coupon = coupon_rate * face_value      # 4.6

# 现金流数组：前6年只有票息，最后一年票息+面值
cf = np.full(maturity_years, coupon)
cf[-1] += face_value                   # 最后一年加回面值

# 贴现因子 (1+y)^t
discount_factors = (1 + ytm) ** t

# 1) 价格 = 现金流贴现之和
price = np.sum(cf / discount_factors)

# 2) 麦考利久期 = Σ [ t * CF_t / (1+y)^t ] / Price
macaulay_duration = np.sum(t * cf / discount_factors) / price

# 修正久期 = 麦考利久期 / (1+y)
modified_duration = macaulay_duration / (1 + ytm)

# 3) 凸性 = Σ [ t(t+1) * CF_t / (1+y)^(t+2) ] / Price
# 注意分母指数是 t+2
convexity = np.sum(t * (t + 1) * cf / ((1 + ytm) ** (t + 2))) / price

# 4) 填充 result 字典
result = {
    'price': round(price, 6),
    'macaulay_duration_years': round(macaulay_duration, 6),
    'modified_duration_years': round(modified_duration, 6),
    'convexity': round(convexity, 6)
}

# 输出结果（课堂展示用）
print("计算结果：")
for key, value in result.items():
    print(f"{key}: {value}")
