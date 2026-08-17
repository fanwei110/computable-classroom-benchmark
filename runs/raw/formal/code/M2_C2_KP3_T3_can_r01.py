import numpy as np

# 债券参数
face = 100.0               # 面值
coupon_rate = 0.046        # 票息率（年化）
ytm = 0.053                # 到期收益率（年化）
maturity = 7               # 剩余年限
freq = 1                   # 每年付息次数（默认1，年度付息）

# 收益率变化：80个基点
delta_y = 0.0080

# ----- 现金流与时间点 -----
n_periods = maturity * freq
t = np.arange(1, n_periods + 1) / freq   # 付息时间点：1, 2, ..., 7 年

coupon_pmt = face * coupon_rate / freq   # 每期票息
cf = np.full(n_periods, coupon_pmt)      # 每期现金流
cf[-1] += face                           # 最后一期加入本金

# ----- 债券定价 -----
disc_factors = (1 + ytm / freq) ** (-t * freq)
pv_cf = cf * disc_factors
price = np.sum(pv_cf)

# ----- 麦考利久期 -----
weights = pv_cf / price
macaulay_duration = np.sum(weights * t)

# ----- 修正久期 -----
modified_duration = macaulay_duration / (1 + ytm / freq)

# ----- 凸性（年度复利下的凸性公式） -----
# 凸性 = 1/P * Σ [ CF_t * t * (t+1) / (1+y)^{t+2} ]
convexity = np.sum(cf * t * (t + 1) / (1 + ytm) ** (t + 2)) / price

# ----- 价格变化百分比估计 -----
# ΔP/P ≈ -MD * Δy + 0.5 * Convexity * (Δy)^2
delta_price_pct = -modified_duration * delta_y + 0.5 * convexity * (delta_y ** 2)

# 价格跌幅百分比（负值表示下跌，例如 -3.5 表示跌幅 3.5%）
price_drop_pct = delta_price_pct * 100.0

# ----- 输出结果 -----
result = {
    'price_drop_pct': price_drop_pct
}

print("债券价格跌幅估计（百分比，负值代表价格下跌）：")
print(result)
