import numpy as np

# ==================== 债券参数 ====================
face_value = 100.0          # 面值
coupon_rate = 0.046         # 票息率 4.6%
n_years = 7                 # 期限 7 年
ytm = 0.053                 # 到期收益率 5.3%
freq = 1                    # 付息频率（每年1次）

# ==================== 现金流构建 ====================
n_periods = n_years * freq
coupon_pmt = face_value * coupon_rate / freq

# 时间期数序列: [1, 2, 3, 4, 5, 6, 7]
periods = np.arange(1, n_periods + 1)

# 每期现金流（前6期为票息，第7期为票息+本金）
cash_flows = np.full(n_periods, coupon_pmt)
cash_flows[-1] += face_value

# ==================== 核心计算 ====================
# 折现因子
discount_factors = (1 + ytm / freq) ** periods

# 各期现金流现值
present_values = cash_flows / discount_factors

# 1. 计算价格
price = np.sum(present_values)

# 2. 计算麦考利久期（以期数为单位，再除以freq转换为年）
mac_duration_periods = np.sum(periods * present_values) / price
macaulay_duration_years = mac_duration_periods / freq

# 3. 计算修正久期
modified_duration_years = macaulay_duration_years / (1 + ytm / freq)

# 4. 计算凸性
# 标准公式：C = (1/P) * Σ [ t(t+1) * CF / (1+y)^{t+2} ]
# 等价于：C = Σ [ t(t+1) * PV ] / [ P * (1+y)^2 ]
# 此处 t 为期数，由于 freq=1，t 即为年数，无需再除以 freq^2 进行年化调整
convexity = np.sum(periods * (periods + 1) * present_values) / (price * (1 + ytm / freq)**2)

# ==================== 输出结果 ====================
result = {
    'price': price,
    'macaulay_duration_years': macaulay_duration_years,
    'modified_duration_years': modified_duration_years,
    'convexity': convexity
}

# 打印结果以供验证
for key, value in result.items():
    print(f"{key}: {value:.6f}")
