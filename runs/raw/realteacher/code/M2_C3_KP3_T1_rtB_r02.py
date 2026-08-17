import numpy as np

# 给定参数
face = 100
coupon_rate = 0.046
ytm = 0.053
years = 7

# 现金流：每年付息一次，到期还本
coupon = face * coupon_rate
t = np.arange(1, years + 1)
cf = np.full(years, coupon)
cf[-1] += face  # 最后一期现金流包括面值

# 折现因子（年复利）
discount = (1 + ytm) ** t
pv = cf / discount

# 1. 债券价格
price = np.sum(pv)

# 2. 麦考利久期
macaulay_duration = np.sum(t * pv) / price

# 3. 修正久期（年复利，除以 (1 + ytm)）
modified_duration = macaulay_duration / (1 + ytm)

# 4. 凸性：Σ [ t*(t+1)*CF / (1+ytm)^(t+2) ] / price
t_plus = t + 2
convexity = np.sum(t * (t + 1) * cf / (1 + ytm) ** t_plus) / price

result = {
    'price': price,
    'macaulay_duration_years': macaulay_duration,
    'modified_duration_years': modified_duration,
    'convexity': convexity
}

# 按精度要求输出（保留6位小数便于观察）
for k, v in result.items():
    print(f"{k}: {v:.6f}")
