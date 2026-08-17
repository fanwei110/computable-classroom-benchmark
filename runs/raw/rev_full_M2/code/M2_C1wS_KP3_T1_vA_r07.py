import numpy as np

# ========================
# 债券参数设定
# ========================
face_value = 100.0          # 面值
coupon_rate = 0.046         # 票面利率（年化）
years_to_maturity = 7       # 剩余期限（年）
yield_to_maturity = 0.053   # 到期收益率（年化）
payment_frequency = 1       # 年付息次数（1 表示年付，内部一致的假设）

# 计算付息期数
n_periods = years_to_maturity * payment_frequency

# 每期票息
coupon = face_value * coupon_rate / payment_frequency

# 每期到期收益率
period_yield = yield_to_maturity / payment_frequency

# ========================
# 构建现金流时间线与现金流金额
# ========================
# 时间（以年为单位）
time_points = np.arange(1, n_periods + 1) / payment_frequency

# 现金流：前 n_periods-1 期为票息，最后一期为票息+面值
cash_flows = np.full(n_periods, coupon)
cash_flows[-1] += face_value

# ========================
# 贴现因子与现值
# ========================
discount_factors = (1 + period_yield) ** (-np.arange(1, n_periods + 1))
present_values = cash_flows * discount_factors

# 1. 债券价格
price = np.sum(present_values)

# ========================
# 2. 麦考利久期（Macaulay duration）
# ========================
weights = present_values / price
macaulay_duration = np.sum(time_points * weights)   # 以年为单位

# 修正久期（Modified duration），年复利下的标准关系
modified_duration = macaulay_duration / (1 + period_yield * payment_frequency)  # 实际就是除以(1+y)

# ========================
# 3. 凸性（Convexity）
# ========================
# 标准公式： convexity = (1/P) * Σ [ t*(t+1) * PV(CF) / (1+y)^2 ]
# 使用时间点（年）计算，注意复利频率一致。
# 由于我们是年付息，period_yield = y，t 以年为单位。
# 公式中分母的 (1+y)^2 已在 PV 之外再除一次，即：
# convexity = Σ [ CF_t * t*(t+1) / (1+y)^{t+2} ] / P
# 为避免混淆，直接用时间（年）和年收益率计算。
convexity_terms = cash_flows * time_points * (time_points + 1) / ((1 + yield_to_maturity) ** (time_points + 2))
convexity = np.sum(convexity_terms) / price

# ========================
# 4. 填充结果字典
# ========================
result = {
    'price': price,
    'macaulay_duration_years': macaulay_duration,
    'modified_duration_years': modified_duration,
    'convexity': convexity
}

# ========================
# 输出结果
# ========================
if __name__ == "__main__":
    for key, value in result.items():
        print(f"{key}: {value:.6f}")
