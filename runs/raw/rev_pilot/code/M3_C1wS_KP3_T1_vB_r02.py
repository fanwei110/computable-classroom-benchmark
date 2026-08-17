import numpy as np

# ==========================================
# 债券参数设定
# ==========================================
face_value = 100          # 面值
coupon_rate = 0.046       # 票息率 4.6%
years = 7                 # 期限 7年
yield_rate = 0.053        # 收益率 5.3%
freq = 1                  # 假设：每年付息一次 (Annual Coupon Payments)

# ==========================================
# 基础现金流构建
# ==========================================
periods = years * freq
t = np.arange(1, periods + 1)  # 现金流时间点序列 [1, 2, ..., 7]

# 每期票息
coupon = face_value * coupon_rate / freq
# 现金流数组：前 6 期为票息，最后一期为票息 + 面值
cf = np.full(periods, coupon)
cf[-1] += face_value

# 贴现因子
discount_factors = (1 + yield_rate / freq) ** t

# ==========================================
# 1. 计算债券价格
# ==========================================
pv_cf = cf / discount_factors
price = np.sum(pv_cf)

# ==========================================
# 2. 计算麦考利久期与修正久期
# ==========================================
# 麦考利久期 (以期为单位) = 加权平均期数
mac_dur_periods = np.sum(t * pv_cf) / price

# 转换为年化麦考利久期
macaulay_duration_years = mac_dur_periods / freq

# 修正久期 = 麦考利久期 / (1 + 收益率/付息频率)
modified_duration_years = macaulay_duration_years / (1 + yield_rate / freq)

# ==========================================
# 3. 计算凸性
# ==========================================
# 凸性公式：Convexity = (1/P) * (d^2P/dy^2) = [1 / (P * f^2)] * Σ [ t(t+1) * CF_t / (1+y/f)^(t+2) ]
convexity_numerator = np.sum(t * (t + 1) * cf / ((1 + yield_rate / freq) ** (t + 2)))
convexity = convexity_numerator / (price * freq**2)

# ==========================================
# 4. 填充结果字典
# ==========================================
result = {
    'price': price,
    'macaulay_duration_years': macaulay_duration_years,
    'modified_duration_years': modified_duration_years,
    'convexity': convexity
}

# 课堂展示打印（保留4位小数，方便教师向学生核对）
print("债券定价与久期、凸性计算结果：")
for key, value in result.items():
    print(f"{key}: {value:.4f}")
