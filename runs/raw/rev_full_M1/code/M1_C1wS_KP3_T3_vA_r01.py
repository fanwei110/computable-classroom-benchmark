import numpy as np
from scipy.optimize import newton

# 债券参数
face_value = 100.0
coupon_rate = 0.046
ytm_current = 0.053  # 当前收益率
maturity_years = 7
coupon_frequency = 2  # 每年付息次数（半年付息）
yield_rise_bps = 80  # 收益率上升基点数
yield_rise = yield_rise_bps / 10000  # 转换为小数

# 计算当前价格（现金流贴现）
def bond_price(ytm, face_value, coupon_rate, maturity_years, coupon_frequency):
    periods = maturity_years * coupon_frequency
    coupon_payment = face_value * coupon_rate / coupon_frequency
    discount_rates = (1 + ytm / coupon_frequency) ** np.arange(1, periods + 1)
    cash_flows = np.full(periods, coupon_payment)
    cash_flows[-1] += face_value  # 最后一期加上面值
    price = np.sum(cash_flows / discount_rates)
    return price

price_current = bond_price(ytm_current, face_value, coupon_rate, maturity_years, coupon_frequency)

# 计算久期（Macaulay Duration）和修正久期
def macaulay_duration(ytm, face_value, coupon_rate, maturity_years, coupon_frequency):
    periods = maturity_years * coupon_frequency
    coupon_payment = face_value * coupon_rate / coupon_frequency
    discount_rates = (1 + ytm / coupon_frequency) ** np.arange(1, periods + 1)
    cash_flows = np.full(periods, coupon_payment)
    cash_flows[-1] += face_value
    discounted_cash_flows = cash_flows / discount_rates
    time_periods = np.arange(1, periods + 1) / coupon_frequency
    duration = np.sum(time_periods * discounted_cash_flows) / np.sum(discounted_cash_flows)
    return duration

def modified_duration(macaulay_duration, ytm, coupon_frequency):
    return macaulay_duration / (1 + ytm / coupon_frequency)

mac_dur = macaulay_duration(ytm_current, face_value, coupon_rate, maturity_years, coupon_frequency)
mod_dur = modified_duration(mac_dur, ytm_current, coupon_frequency)

# 计算凸性
def convexity(ytm, face_value, coupon_rate, maturity_years, coupon_frequency):
    periods = maturity_years * coupon_frequency
    coupon_payment = face_value * coupon_rate / coupon_frequency
    discount_rates = (1 + ytm / coupon_frequency) ** np.arange(1, periods + 1)
    cash_flows = np.full(periods, coupon_payment)
    cash_flows[-1] += face_value
    time_periods = np.arange(1, periods + 1) / coupon_frequency
    discounted_cash_flows = cash_flows / discount_rates
    convexity = np.sum(time_periods * (time_periods + 1) * discounted_cash_flows) / (np.sum(discounted_cash_flows) * (1 + ytm / coupon_frequency)**2)
    return convexity

conv = convexity(ytm_current, face_value, coupon_rate, maturity_years, coupon_frequency)

# 估算价格变化（使用久期和凸性）
price_drop_pct = -mod_dur * yield_rise + 0.5 * conv * (yield_rise ** 2)
price_drop_pct *= 100  # 转换为百分比

# 精确计算新价格（验证）
ytm_new = ytm_current + yield_rise
price_new = bond_price(ytm_new, face_value, coupon_rate, maturity_years, coupon_frequency)
price_drop_pct_exact = (price_new - price_current) / price_current * 100

# 存储结果
result = {
    'price_drop_pct': price_drop_pct  # 使用久期和凸性的估算值
}

# 输出结果（可选，用于调试）
print(f"当前价格: {price_current:.4f}")
print(f"久期 (Macaulay): {mac_dur:.4f}")
print(f"修正久期: {mod_dur:.4f}")
print(f"凸性: {conv:.4f}")
print(f"估算跌幅: {price_drop_pct:.4f}%")
print(f"精确跌幅: {price_drop_pct_exact:.4f}%")
