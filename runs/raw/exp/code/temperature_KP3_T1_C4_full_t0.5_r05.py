import numpy as np

# 债券参数
face_value = 100.0          # 面值
coupon_rate = 0.046         # 票息率 4.6%
maturity_years = 7          # 期限 7 年
ytm = 0.053                 # 到期收益率 5.3%

# 1. 计算价格（现金流贴现）
# 现金流：第1~6年每年票息，第7年票息+面值
cash_flows = np.array([coupon_rate * face_value] * (maturity_years - 1) +
                      [coupon_rate * face_value + face_value])
# 对应时间点 t = 1, 2, ..., 7
t = np.arange(1, maturity_years + 1)
# 贴现因子
discount_factors = (1 + ytm) ** (-t)
# 价格 = 现金流贴现之和
price = np.sum(cash_flows * discount_factors)

# 2. 计算麦考利久期
# 麦考利久期 = Σ[t * CF_t / (1+y)^t] / P
macaulay_duration = np.sum(t * cash_flows * discount_factors) / price

# 修正久期 = 麦考利久期 / (1+y)
modified_duration = macaulay_duration / (1 + ytm)

# 3. 计算凸性（年平方）
# 凸性 = Σ[t(t+1) * CF_t / (1+y)^(t+2)] / P
convexity = np.sum(t * (t + 1) * cash_flows * (1 + ytm) ** (-t - 2)) / price

# 4. 填充 result 字典
result = {
    'price': price,
    'macaulay_duration_years': macaulay_duration,
    'modified_duration_years': modified_duration,
    'convexity': convexity
}

# 输出结果（保留适当精度便于课堂展示）
print("计算结果：")
for key, value in result.items():
    print(f"{key:30s} = {value:.6f}")
