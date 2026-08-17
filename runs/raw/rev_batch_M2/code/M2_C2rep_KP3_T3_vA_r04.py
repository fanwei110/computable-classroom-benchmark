import numpy as np

# 债券参数
FACE = 100.0          # 面值
COUPON_RATE = 0.046   # 票面利率（年化）
YTM = 0.053           # 当前到期收益率（年化）
YEARS = 7             # 剩余年限
FREQ = 2              # 每年付息次数（国际惯例：半年付息一次）
DY = 0.0080           # 收益率上升 80 个基点（0.0080）

# 派生参数
periods = int(YEARS * FREQ)                 # 总期数
coupon = FACE * COUPON_RATE / FREQ         # 每期票息
period_rate = YTM / FREQ                   # 每期贴现率

# 构造现金流与时间线
times = np.arange(1, periods + 1)          # 现金流发生期数（1,2,...,N）
cashflows = np.full(periods, coupon)       # 各期票息
cashflows[-1] += FACE                      # 最后一期加上本金

# 贴现因子与现值
discount_factors = (1 + period_rate) ** -times
pv_cashflows = cashflows * discount_factors
price = np.sum(pv_cashflows)               # 当前全价

# --- 1. 利率敏感性（久期与凸性） ---
# 麦考利久期（期数）
mac_dur_periods = np.sum(times * pv_cashflows) / price
# 麦考利久期（年化）
mac_dur_years = mac_dur_periods / FREQ

# 修正久期（年化）
mod_dur_years = mac_dur_years / (1 + period_rate)

# 凸性（期数平方单位）
conv_periods = np.sum(times * (times + 1) * pv_cashflows) / (price * (1 + period_rate)**2)
# 凸性（年化）
conv_annual = conv_periods / (FREQ ** 2)

# --- 2. 估算收益率上升 80 个基点的价格影响 ---
# 基于修正久期与凸性的价格变动百分比（小数）
delta_p_approx = -mod_dur_years * DY + 0.5 * conv_annual * (DY ** 2)
# 下跌幅度（正百分点）
price_drop_pct = -delta_p_approx * 100.0

# --- （可选验证）精确重定价 ---
new_ytm = YTM + DY
new_period_rate = new_ytm / FREQ
new_discount_factors = (1 + new_period_rate) ** -times
new_price = np.sum(cashflows * new_discount_factors)
exact_drop_pct = (price - new_price) / price * 100.0

# --- 输出物 ---
result = {
    'price_drop_pct': price_drop_pct
}

# 课堂展示用打印信息（便于投屏讲解）
print(f"面值: {FACE}, 票息: {COUPON_RATE*100}%, 收益率: {YTM*100}%, 年限: {YEARS}年")
print(f"当前全价: {price:.4f}")
print(f"麦考利久期(年): {mac_dur_years:.4f}")
print(f"修正久期(年): {mod_dur_years:.4f}")
print(f"凸性(年化): {conv_annual:.4f}")
print(f"收益率上升 {DY*100:.0f} 个基点")
print(f"近似价格变动(%): {delta_p_approx*100:.4f}%")
print(f"近似价格跌幅(%): {price_drop_pct:.4f}%")
print(f"精确新价格: {new_price:.4f}, 精确跌幅(%): {exact_drop_pct:.4f}%")
print(f"\n>>> 最终结果字典 result = {result}")
