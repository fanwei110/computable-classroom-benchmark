import numpy as np

# 债券参数
face_value = 100.0        # 面值
coupon_rate = 0.046       # 票息率
years = 7                 # 期限（年）
ytm = 0.053               # 到期收益率（年化）

# 假设：每年付息一次，到期一次还本
t = np.arange(1, years + 1)               # 现金流发生时间（年）
coupon = face_value * coupon_rate          # 每期票息
cf = np.full(years, coupon)               # 各期现金流
cf[-1] += face_value                      # 最后一期加入本金

# 1. 计算价格：现金流贴现
discount_factors = (1 + ytm) ** t
pv = cf / discount_factors
price = np.sum(pv)

# 2. 计算麦考利久期与修正久期
weights = pv / price
macaulay_duration = np.sum(t * weights)                  # 麦考利久期（年）
modified_duration = macaulay_duration / (1 + ytm)        # 修正久期（年）

# 3. 计算凸性
# 惯用公式： convexity = Σ [ t(t+1) * PV(CF_t) ] / [ P * (1+y)^2 ]
convexity = np.sum(t * (t + 1) * pv) / (price * (1 + ytm) ** 2)

# 4. 输出结果
result = {
    'price': price,
    'macaulay_duration_years': macaulay_duration,
    'modified_duration_years': modified_duration,
    'convexity': convexity
}

# 当堂运行时可直接打印查看
print(result)
