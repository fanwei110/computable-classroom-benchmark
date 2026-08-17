import numpy as np

# ==========================================
# 已知参数与假设
# ==========================================
face_value = 100.0          # 面值
coupon_rate = 0.046         # 票息率 4.6%
years_to_maturity = 7       # 期限 7年
ytm = 0.053                 # 到期收益率 5.3%

# 假设处理：题目未指明付息频率，默认采用市场最常见的假设：每年付息一次
freq = 1                    # 每年付息次数
periods = int(years_to_maturity * freq)  # 总期数
coupon_per_period = face_value * coupon_rate / freq  # 每期票息

# ==========================================
# 1. 构建现金流并计算价格
# ==========================================
# 生成每期现金流：前6期仅付票息，第7期付票息+面值
cash_flows = np.full(periods, coupon_per_period)
cash_flows[-1] += face_value

# 对应的期数时间数组 (1, 2, ..., 7)
t_periods = np.arange(1, periods + 1)

# 按报价收益率贴现现金流
discount_factors = (1 + ytm / freq) ** (-t_periods)
price = np.sum(cash_flows * discount_factors)

# ==========================================
# 2. 计算麦考利久期与修正久期
# ==========================================
# 麦考利久期 = (1/P) * Σ [ t * CF_t / (1+y)^t ]
macaulay_duration_periods = np.sum(t_periods * cash_flows * discount_factors) / price

# 转换为以年为单位的麦考利久期
macaulay_duration_years = macaulay_duration_periods / freq

# 修正久期 = 麦考利久期 / (1 + y)
modified_duration_years = macaulay_duration_years / (1 + ytm / freq)

# ==========================================
# 3. 计算凸性
# ==========================================
# 凸性 = (1/P) * Σ [ t*(t+1) * CF_t / (1+y)^(t+2) ] / freq^2
# 其中 t 为期数，此公式为标准金融学教材的按期现金流凸性折现公式
convexity_periods = np.sum(t_periods * (t_periods + 1) * cash_flows / (1 + ytm / freq) ** (t_periods + 2)) / price
convexity = convexity_periods / (freq ** 2)

# ==========================================
# 4. 填充 result
# ==========================================
result = {
    'price': price,
    'macaulay_duration_years': macaulay_duration_years,
    'modified_duration_years': modified_duration_years,
    'convexity': convexity
}

# 课堂投屏展示结果
print("="*50)
print("债券定价与久期、凸性计算结果:")
print("="*50)
for key, value in result.items():
    print(f"{key:>28s} : {value:.6f}")
print("="*50)
