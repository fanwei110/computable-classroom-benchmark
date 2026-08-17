import numpy as np
from scipy.optimize import newton

# 债券参数
face_value = 100  # 面值
annual_coupon_rate = 0.046  # 年票息率4.6%
ytm_initial = 0.053  # 初始到期收益率5.3%
years_to_maturity = 7  # 剩余期限7年
coupon_frequency = 2  # 每年付息次数（半年付息）
yield_change_bp = 80  # 收益率变化80个基点
yield_change = yield_change_bp / 10000  # 转换为小数

# 计算每期票息
coupon_per_period = (face_value * annual_coupon_rate) / coupon_frequency

# 定义债券定价函数（现金流贴现）
def bond_price(ytm, face_value, coupon, periods, frequency):
    ytm_per_period = ytm / frequency
    periods_total = periods * frequency
    cash_flows = np.full(periods_total, coupon)
    cash_flows[-1] += face_value  # 最后一期加上面值
    discount_factors = (1 + ytm_per_period) ** np.arange(1, periods_total + 1)
    price = np.sum(cash_flows / discount_factors)
    return price

# 计算初始价格
initial_price = bond_price(ytm_initial, face_value, coupon_per_period, years_to_maturity, coupon_frequency)

# 计算久期（Macaulay Duration）和修正久期
def macaulay_duration(ytm, face_value, coupon, periods, frequency):
    ytm_per_period = ytm / frequency
    periods_total = periods * frequency
    cash_flows = np.full(periods_total, coupon)
    cash_flows[-1] += face_value
    discount_factors = (1 + ytm_per_period) ** np.arange(1, periods_total + 1)
    discounted_cash_flows = cash_flows / discount_factors
    weights = discounted_cash_flows / np.sum(discounted_cash_flows)
    time_periods = np.arange(1, periods_total + 1) / frequency
    duration = np.sum(weights * time_periods)
    return duration

def modified_duration(macaulay_duration, ytm, frequency):
    return macaulay_duration / (1 + ytm / frequency)

macaulay_dur = macaulay_duration(ytm_initial, face_value, coupon_per_period, years_to_maturity, coupon_frequency)
mod_dur = modified_duration(macaulay_dur, ytm_initial, coupon_frequency)

# 计算凸性
def convexity(ytm, face_value, coupon, periods, frequency):
    ytm_per_period = ytm / frequency
    periods_total = periods * frequency
    cash_flows = np.full(periods_total, coupon)
    cash_flows[-1] += face_value
    discount_factors = (1 + ytm_per_period) ** np.arange(1, periods_total + 1)
    discounted_cash_flows = cash_flows / discount_factors
    time_periods = np.arange(1, periods_total + 1) / frequency
    convexity = np.sum(discounted_cash_flows * time_periods * (time_periods + 1 / frequency)) / (initial_price * (1 + ytm_per_period)**2)
    return convexity

conv = convexity(ytm_initial, face_value, coupon_per_period, years_to_maturity, coupon_frequency)

# 估算价格变化（使用久期和凸性）
price_change_pct = -mod_dur * yield_change + 0.5 * conv * (yield_change ** 2)
price_drop_pct = price_change_pct * 100  # 转换为百分比

# 存储结果
result = {
    'price_drop_pct': price_drop_pct
}

# 输出结果（可选，便于调试）
print(f"初始价格: {initial_price:.4f}")
print(f"修正久期: {mod_dur:.4f}")
print(f"凸性: {conv:.4f}")
print(f"预计价格跌幅: {price_drop_pct:.4f}%")
