import numpy as np

# ================= 债券参数设定 =================
face_value = 100          # 面值
coupon_rate = 0.046       # 票面利率
years_to_maturity = 7     # 期限（年）
ytm = 0.053               # 到期收益率

# 假设处理：题目未指明付息频率，按市场惯例假设为每年付息1次 (freq=1)
freq = 1

# ================= 中间变量计算 =================
n_periods = int(years_to_maturity * freq)      # 总期数
t = np.arange(1, n_periods + 1)               # 现金流发生的时间序列
periodic_coupon = face_value * coupon_rate / freq  # 每期票息
periodic_ytm = ytm / freq                     # 每期收益率

# 构造现金流数组：前 n-1 期为票息，最后一期为票息+面值
cf = np.full(n_periods, periodic_coupon)
cf[-1] += face_value

# ================= 步骤1：计算债券价格 =================
discount_factors = (1 + periodic_ytm) ** t
pv = cf / discount_factors
price = np.sum(pv)

# ================= 步骤2：计算麦考利久期与修正久期 =================
# 麦考利久期 (年化) = [Σ(t * PV(CF_t)) / Price] / freq
macaulay_duration = np.sum(t * pv) / price / freq

# 修正久期 (年化) = Macaulay Duration / (1 + periodic_ytm)
modified_duration = macaulay_duration / (1 + periodic_ytm)

# ================= 步骤3：计算凸性 =================
# 凸性公式 (年化) = [1 / (P * (1+y)^2)] * Σ[t*(t+1) * CF_t / (1+y)^t] / freq^2
# 简化推导即为：Σ[t*(t+1) * PV(CF_t)] / (P * (1+y)^2) / freq^2
convexity = np.sum(t * (t + 1) * pv) / (price * (1 + periodic_ytm)**2) / (freq**2)

# ================= 步骤4：填充 result =================
result = {
    'price': round(price, 4),
    'macaulay_duration_years': round(macaulay_duration, 4),
    'modified_duration_years': round(modified_duration, 4),
    'convexity': round(convexity, 4)
}

# 课堂投屏打印输出
print(f"债券定价与久期、凸性计算结果（假设每年付息{freq}次）：")
for key, value in result.items():
    print(f"{key}: {value}")
