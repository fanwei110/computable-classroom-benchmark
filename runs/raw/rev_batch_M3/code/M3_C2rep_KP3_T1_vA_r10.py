import numpy as np

# ==================== 假设与参数设定 ====================
# 假设：本题未指明付息频率，按金融学常规及内部一致性，假设为每年付息一次 (Annual Coupon)
face_value = 100.0          # 面值
coupon_rate = 0.046         # 票息率 4.6%
maturity_years = 7          # 期限 7 年
ytm = 0.053                # 到期收益率 5.3%

# ==================== 1. 计算债券价格 ====================
# 构建现金流时间序列与现金流数组
t = np.arange(1, maturity_years + 1)
cash_flows = np.full(maturity_years, face_value * coupon_rate)
cash_flows[-1] += face_value  # 最后一期加上本金

# 贴现因子
discount_factors = (1 + ytm) ** t

# 现值
present_values = cash_flows / discount_factors

# 价格 = 现金流贴现之和
price = np.sum(present_values)

# ==================== 2. 计算麦考利久期与修正久期 ====================
# 麦考利久期 = (时间 x 现值) 之和 / 价格
weighted_pv = t * present_values
macaulay_duration_years = np.sum(weighted_pv) / price

# 修正久期 = 麦考利久期 / (1 + 到期收益率)
modified_duration_years = macaulay_duration_years / (1 + ytm)

# ==================== 3. 计算凸性 ====================
# 凸性 = (时间 x (时间+1) x 现值) 之和 / (价格 x (1+到期收益率)^2)
# 注：对于按年付息债券，t即为年份，此公式直接得出年度化凸性
convexity_numerator = np.sum(t * (t + 1) * present_values)
convexity = convexity_numerator / (price * (1 + ytm) ** 2)

# ==================== 4. 填充 result 字典 ====================
result = {
    'price': price,
    'macaulay_duration_years': macaulay_duration_years,
    'modified_duration_years': modified_duration_years,
    'convexity': convexity
}

# (可选) 打印结果以便投屏展示
for key, value in result.items():
    print(f"{key}: {value:.6f}")
