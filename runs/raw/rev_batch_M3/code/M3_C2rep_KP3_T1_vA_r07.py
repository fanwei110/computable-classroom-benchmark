import numpy as np

# ==================== 参数设定 ====================
# 题目未指明付息频率，按行业惯例假设为每年付息一次
face_value = 100.0          # 面值
coupon_rate = 0.046          # 票息率 4.6%
years_to_maturity = 7        # 期限 7年
ytm = 0.053                 # 到期收益率 5.3%

# 每年票息现金流
annual_coupon = face_value * coupon_rate

# ==================== 构建时间轴与现金流 ====================
t = np.arange(1, years_to_maturity + 1)
cf = np.full(years_to_maturity, annual_coupon)
cf[-1] += face_value  # 最后一期还本付息

# ==================== 1. 计算价格 ====================
discount_factors = (1 + ytm) ** t
pv_cf = cf / discount_factors
price = np.sum(pv_cf)

# ==================== 2. 计算麦考利久期与修正久期 ====================
# 麦考利久期 = 现金流加权时间 / 价格
macaulay_duration_years = np.sum(t * pv_cf) / price

# 修正久期 = 麦考利久期 / (1 + ytm)
modified_duration_years = macaulay_duration_years / (1 + ytm)

# ==================== 3. 计算凸性 ====================
# 凸性公式：1/P * Σ [ t(t+1) * CF / (1+y)^(t+2) ]
convexity = np.sum(t * (t + 1) * cf / (1 + ytm) ** (t + 2)) / price

# ==================== 4. 填充 result ====================
result = {
    'price': price,
    'macaulay_duration_years': macaulay_duration_years,
    'modified_duration_years': modified_duration_years,
    'convexity': convexity
}

# 课堂演示打印输出
for key, value in result.items():
    print(f"{key}: {value:.6f}")
