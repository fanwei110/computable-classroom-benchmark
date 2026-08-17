import numpy as np

# ================= 债券参数与假设 =================
# 题目未指明付息频率，按金融学惯例假设每年付息1次 (Annual Coupon)
face_value = 100.0          # 面值
coupon_rate = 0.046         # 票面利率 4.6%
years_to_maturity = 7       # 期限 7年
ytm = 0.053                 # 到期收益率 5.3%
freq = 1                    # 付息频率（每年1次）

# ================= 中间变量计算 =================
periods = years_to_maturity * freq               # 总期数
coupon_per_period = face_value * coupon_rate / freq  # 每期票息
ytm_per_period = ytm / freq                      # 每期收益率

# 现金流时间轴 (以期数计，1, 2, ..., periods)
t = np.arange(1, periods + 1)

# 构建现金流数组：前 (periods-1) 期为票息，最后一期为票息+面值
cash_flows = np.full(periods, coupon_per_period)
cash_flows[-1] += face_value

# 贴现因子
discount_factors = (1 + ytm_per_period) ** t

# 现值
present_values = cash_flows / discount_factors

# ================= 步骤 1: 计算价格 =================
price = np.sum(present_values)

# ================= 步骤 2: 计算麦考利久期与修正久期 =================
# 麦考利久期 (以期为单位)
macaulay_duration_periods = np.sum(t * present_values) / price
# 转换为以年为单位 (除以付息频率)
macaulay_duration_years = macaulay_duration_periods / freq

# 修正久期 = 麦考利久期 / (1 + 每期收益率)
modified_duration_years = macaulay_duration_years / (1 + ytm_per_period)

# ================= 步骤 3: 计算凸性 =================
# 凸性 (以期数为单位) = 1/P * sum[ t*(t+1) * CF / (1+r)^(t+2) ]
# 等价于 = 1/P * 1/(1+r)^2 * sum[ t*(t+1) * PV ]
convexity_periods = np.sum(t * (t + 1) * present_values) / (price * (1 + ytm_per_period) ** 2)
# 转换为以年为单位的凸性 (除以付息频率的平方)
convexity = convexity_periods / (freq ** 2)

# ================= 步骤 4: 填充 result =================
result = {
    'price': round(price, 4),
    'macaulay_duration_years': round(macaulay_duration_years, 4),
    'modified_duration_years': round(modified_duration_years, 4),
    'convexity': round(convexity, 4)
}

# ================= 课堂投屏展示 =================
print("="*50)
print("《证券投资学》课堂实时计算演示")
print("="*50)
print(f"假设条件: 面值{int(face_value)}, 票面利率{coupon_rate*100}%, 期限{years_to_maturity}年, YTM{ytm*100}% (每年付息{freq}次)")
print("-"*50)
print(f"债券价格 (Price)            : {result['price']:.4f}")
print(f"麦考利久期 (Macaulay Duration): {result['macaulay_duration_years']:.4f} 年")
print(f"修正久期 (Modified Duration) : {result['modified_duration_years']:.4f} 年")
print(f"凸性 (Convexity)            : {result['convexity']:.4f}")
print("="*50)
