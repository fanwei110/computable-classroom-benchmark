import numpy as np

# ------------------------------
# 债券参数
# ------------------------------
face_value = 100.0          # 面值
coupon_rate = 0.046         # 票息率（年）
years = 7                   # 剩余年限
yield_rate = 0.053          # 到期收益率（年）

# 假设每年付息一次，到期一次还本。
coupon = face_value * coupon_rate

# 现金流时间点: t = 1, 2, ..., years
t = np.arange(1, years + 1)

# 各期现金流（最后一期包含本金）
cash_flows = np.full(years, coupon)
cash_flows[-1] += face_value

# 贴现因子及现值
discount_factors = (1 + yield_rate) ** (-t)
present_value = cash_flows * discount_factors

# ------------------------------
# 1. 债券价格
# ------------------------------
price = np.sum(present_value)

# ------------------------------
# 2. 麦考利久期 & 修正久期
# ------------------------------
macaulay_duration = np.sum(t * present_value) / price
modified_duration = macaulay_duration / (1 + yield_rate)

# ------------------------------
# 3. 凸性
# 公式: Convexity = [1 / (P * (1+y)^2)] * Σ[t*(t+1) * PV_CF_t]
# ------------------------------
convexity = np.sum(t * (t + 1) * present_value) / (price * (1 + yield_rate)**2)

# ------------------------------
# 输出结果
# ------------------------------
result = {
    'price': price,
    'macaulay_duration_years': macaulay_duration,
    'modified_duration_years': modified_duration,
    'convexity': convexity
}

if __name__ == "__main__":
    for key, value in result.items():
        print(f"{key}: {value:.6f}")
