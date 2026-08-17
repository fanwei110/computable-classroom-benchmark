import numpy as np

# 债券参数
face_value = 100.0          # 面值
coupon_rate = 0.046         # 票息率
maturity_years = 7          # 期限（年）
yield_to_maturity = 0.053   # 到期收益率（小数）

# 每年付息一次，共 maturity_years 次
coupon = face_value * coupon_rate  # 每年票息金额
t = np.arange(1, maturity_years + 1)  # 付息时间点 1,2,...,7

# 现金流：前6年每年票息，最后一年票息+面值
cash_flows = np.full(maturity_years, coupon)
cash_flows[-1] += face_value

# 贴现因子（按年复利）
discount_factors = (1 + yield_to_maturity) ** (-t)

# 1. 价格 = 现金流贴现之和
price = np.sum(cash_flows * discount_factors)

# 2. 麦考利久期 = Σ [ t * CF_t / (1+y)^t ] / 价格
macaulay_duration = np.sum(t * cash_flows * discount_factors) / price

# 修正久期 = 麦考利久期 / (1 + y)
modified_duration = macaulay_duration / (1 + yield_to_maturity)

# 3. 凸性 = Σ [ t(t+1) * CF_t / (1+y)^(t+2) ] / 价格
convexity = np.sum(t * (t + 1) * cash_flows / (1 + yield_to_maturity) ** (t + 2)) / price

# 4. 填充结果字典
result = {
    'price': round(price, 6),
    'macaulay_duration_years': round(macaulay_duration, 6),
    'modified_duration_years': round(modified_duration, 6),
    'convexity': round(convexity, 6)
}

# 输出结果（供课堂展示）
print("债券价格:", result['price'])
print("麦考利久期 (年):", result['macaulay_duration_years'])
print("修正久期 (年):", result['modified_duration_years'])
print("凸性 (年平方):", result['convexity'])
