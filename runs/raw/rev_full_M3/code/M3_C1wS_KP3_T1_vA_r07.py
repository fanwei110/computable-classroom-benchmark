import numpy as np

# ====================
# 债券参数设定
# ====================
face_value = 100.0          # 面值
coupon_rate = 0.046         # 票面利率 4.6%
years_to_maturity = 7       # 期限 7年
ytm = 0.053                # 到期收益率 5.3%

# 假设处理：题目未指明付息频率，按国内高校《证券投资学》惯例，假设每年付息一次（Annual Coupon）

# ====================
# 1. 计算现金流与债券价格
# ====================
# 每期利息
annual_coupon = face_value * coupon_rate

# 生成各期现金流：1-6年为利息，第7年为利息+本金
cash_flows = np.full(years_to_maturity, annual_coupon)
cash_flows[-1] += face_value

# 各期时间点
time_periods = np.arange(1, years_to_maturity + 1)

# 贴现因子
discount_factors = (1 + ytm) ** time_periods

# 各期现金流现值
pv_cash_flows = cash_flows / discount_factors

# 债券价格 = 现金流现值之和
price = np.sum(pv_cash_flows)

# ====================
# 2. 计算麦考利久期与修正久期
# ====================
# 麦考利久期 = (各期现金流现值 × 时间) 之和 / 债券价格
weighted_pv = pv_cash_flows * time_periods
macaulay_duration_years = np.sum(weighted_pv) / price

# 修正久期 = 麦考利久期 / (1 + 到期收益率)
modified_duration_years = macaulay_duration_years / (1 + ytm)

# ====================
# 3. 计算凸性
# ====================
# 凸性 = [1 / (P * (1+y)^2)] * Σ [CF_t * t * (t+1) / (1+y)^t]
convexity_numerator = np.sum(cash_flows * time_periods * (time_periods + 1) / discount_factors)
convexity = convexity_numerator / (price * (1 + ytm) ** 2)

# ====================
# 4. 填充结果
# ====================
result = {
    'price': round(price, 4),
    'macaulay_duration_years': round(macaulay_duration_years, 4),
    'modified_duration_years': round(modified_duration_years, 4),
    'convexity': round(convexity, 4)
}

# 打印结果以便投屏展示
print("="*50)
print("《证券投资学》债券定价与久期、凸性计算结果")
print("="*50)
print(f"假设: 面值{int(face_value)}元, 票面利率{coupon_rate*100}%, 期限{years_to_maturity}年, YTM{ytm*100}%, 每年付息一次")
print("-"*50)
for key, value in result.items():
    print(f"{key:>30s} : {value}")
print("="*50)
