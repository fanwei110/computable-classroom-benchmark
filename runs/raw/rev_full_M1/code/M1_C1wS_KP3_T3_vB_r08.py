import numpy as np
from scipy.optimize import newton

# 债券参数
face_value = 100          # 面值
annual_coupon_rate = 0.046  # 年票息率 4.6%
ytm_current = 0.053       # 当前到期收益率 5.3%
years_to_maturity = 7     # 剩余期限 7 年
coupon_frequency = 2      # 每年付息次数（半年付息）
yield_change_bp = 80      # 收益率变动 80 个基点

# 计算每期票息
coupon_per_period = face_value * annual_coupon_rate / coupon_frequency

# 定义债券定价函数（半年复利）
def bond_price(ytm, face_value, coupon, periods):
    ytm_period = ytm / coupon_frequency
    cash_flows = np.full(periods, coupon)
    cash_flows[-1] += face_value  # 最后一期加上面值
    periods_arr = np.arange(1, periods + 1)
    price = np.sum(cash_flows / ((1 + ytm_period) ** periods_arr))
    return price

# 计算当前价格
periods_total = years_to_maturity * coupon_frequency
current_price = bond_price(ytm_current, face_value, coupon_per_period, periods_total)

# 计算久期（Macaulay Duration）和修正久期
def macaulay_duration(ytm, face_value, coupon, periods):
    ytm_period = ytm / coupon_frequency
    cash_flows = np.full(periods, coupon)
    cash_flows[-1] += face_value
    periods_arr = np.arange(1, periods + 1)
    pv_cash_flows = cash_flows / ((1 + ytm_period) ** periods_arr)
    weighted_cash_flows = pv_cash_flows * periods_arr
    duration = np.sum(weighted_cash_flows) / np.sum(pv_cash_flows)
    return duration / coupon_frequency  # 转换为年化久期

macaulay_dur = macaulay_duration(ytm_current, face_value, coupon_per_period, periods_total)
modified_dur = macaulay_dur / (1 + ytm_current / coupon_frequency)  # 修正久期

# 计算凸性
def convexity(ytm, face_value, coupon, periods):
    ytm_period = ytm / coupon_frequency
    cash_flows = np.full(periods, coupon)
    cash_flows[-1] += face_value
    periods_arr = np.arange(1, periods + 1)
    pv_cash_flows = cash_flows / ((1 + ytm_period) ** periods_arr)
    weighted_cash_flows = pv_cash_flows * periods_arr * (periods_arr + 1)
    conv = np.sum(weighted_cash_flows) / (np.sum(pv_cash_flows) * (1 + ytm_period)**2)
    return conv / (coupon_frequency ** 2)  # 转换为年化凸性

conv = convexity(ytm_current, face_value, coupon_per_period, periods_total)

# 计算收益率变动后的价格（精确计算）
ytm_new = ytm_current + yield_change_bp / 10000
new_price = bond_price(ytm_new, face_value, coupon_per_period, periods_total)

# 使用久期和凸性近似估算价格变动
delta_y = yield_change_bp / 10000
price_drop_approx = -modified_dur * delta_y + 0.5 * conv * (delta_y ** 2)
price_drop_pct_approx = price_drop_approx * 100

# 精确价格跌幅
price_drop_pct_exact = ((current_price - new_price) / current_price) * 100

# 结果存储（使用精确计算结果）
result = {
    'price_drop_pct': price_drop_pct_exact
}

# 输出结果（可选，用于调试）
print(f"当前价格: {current_price:.4f}")
print(f"新价格: {new_price:.4f}")
print(f"精确价格跌幅: {price_drop_pct_exact:.4f}%")
print(f"久期-凸性近似跌幅: {price_drop_pct_approx:.4f}%")
