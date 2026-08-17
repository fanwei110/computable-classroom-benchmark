import numpy as np

# ==================== 债券参数设定 ====================
face_value = 100.0          # 面值
coupon_rate = 0.046         # 票息率 4.6%
years = 7                   # 期限 7 年
ytm = 0.053                 # 到期收益率 5.3%
# 假设：按年付息，离散贴现

# ==================== 现金流构建 ====================
# 每年票息
coupon = face_value * coupon_rate
# 现金流数组：前 6 年为票息，第 7 年为票息+面值
cf = np.full(years, coupon)
cf[-1] += face_value

# 时间点数组
t = np.arange(1, years + 1)

# ==================== 1. 计算债券价格 ====================
# 贴现因子
discount_factors = (1 + ytm) ** t
# 各期现金流现值
pv_cf = cf / discount_factors
# 价格 = 现值之和
price = np.sum(pv_cf)

# ==================== 2. 计算久期 ====================
# 麦考利久期 = (时间 × 现金流现值) 之和 / 价格
macaulay_duration_years = np.sum(t * pv_cf) / price

# 修正久期 = 麦考利久期 / (1 + 到期收益率)
modified_duration_years = macaulay_duration_years / (1 + ytm)

# ==================== 3. 计算凸性 ====================
# 凸性公式：Conv = [1 / (P * (1+y)^2)] * Σ [t(t+1) * CF_t / (1+y)^t]
# 推导自价格对收益率的二阶导数：d²P/dy² = Σ [t(t+1) * CF_t / (1+y)^(t+2)]
# 用 pv_cf 替代可得：t(t+1) * pv_cf / (1+y)^2
convexity = np.sum(t * (t + 1) * pv_cf) / (price * (1 + ytm) ** 2)

# ==================== 4. 填充结果 ====================
result = {
    'price': price,
    'macaulay_duration_years': macaulay_duration_years,
    'modified_duration_years': modified_duration_years,
    'convexity': convexity
}

# 控制台输出，方便课堂投屏展示
print("="*40)
print("《证券投资学》- 债券定价与久期、凸性计算")
print("="*40)
print(f"面值: {face_value}, 票息率: {coupon_rate*100}%")
print(f"期限: {years}年, 到期收益率(YTM): {ytm*100}%")
print("-"*40)
for key, value in result.items():
    print(f"{key:.<30} {value:.6f}")
print("="*40)
