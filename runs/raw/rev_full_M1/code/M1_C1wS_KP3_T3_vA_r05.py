import numpy as np
from scipy.optimize import newton

# 债券参数
face_value = 100.0          # 面值
annual_coupon_rate = 0.046  # 年票息率 4.6%
ytm_initial = 0.053         # 初始收益率 5.3%
maturity_years = 7          # 期限 7 年
coupon_freq = 2             # 每年付息次数（半年付息）
yield_rise_bps = 80         # 收益率上升 80 个基点

# 计算每期票息
coupon_per_period = face_value * annual_coupon_rate / coupon_freq

# 现金流：每期票息 + 到期面值
periods = maturity_years * coupon_freq
cash_flows = np.full(periods, coupon_per_period)
cash_flows[-1] += face_value  # 最后一期加上面值

# 1. 计算当前收益率下的债券价格
def bond_price(yield_per_period, cash_flows, periods):
    """计算债券价格：现金流贴现之和"""
    discount_factors = (1 + yield_per_period) ** (-np.arange(1, periods + 1))
    return np.sum(cash_flows * discount_factors)

yield_per_period_initial = ytm_initial / coupon_freq
price_initial = bond_price(yield_per_period_initial, cash_flows, periods)

# 2. 计算久期（Macaulay Duration）和修正久期
def macaulay_duration(yield_per_period, cash_flows, periods):
    """计算 Macaulay 久期"""
    discount_factors = (1 + yield_per_period) ** (-np.arange(1, periods + 1))
    pv_cash_flows = cash_flows * discount_factors
    weighted_times = np.arange(1, periods + 1) * pv_cash_flows
    return np.sum(weighted_times) / np.sum(pv_cash_flows)

mac_dur = macaulay_duration(yield_per_period_initial, cash_flows, periods)
mod_dur = mac_dur / (1 + yield_per_period_initial)  # 修正久期

# 3. 计算凸性
def convexity(yield_per_period, cash_flows, periods):
    """计算凸性"""
    discount_factors = (1 + yield_per_period) ** (-np.arange(1, periods + 1))
    pv_cash_flows = cash_flows * discount_factors
    weighted_times = np.arange(1, periods + 1) * (np.arange(1, periods + 1) + 1) * pv_cash_flows
    return np.sum(weighted_times) / (np.sum(pv_cash_flows) * (1 + yield_per_period) ** 2)

conv = convexity(yield_per_period_initial, cash_flows, periods)

# 4. 估算收益率上升 80 个基点后的价格变化
yield_rise_per_period = (ytm_initial + yield_rise_bps / 10000) / coupon_freq
price_new_approx = price_initial * (1 - mod_dur * (yield_rise_per_period - yield_per_period_initial)
                                   + 0.5 * conv * (yield_rise_per_period - yield_per_period_initial) ** 2)

# 精确计算新价格
price_new_exact = bond_price(yield_rise_per_period, cash_flows, periods)

# 计算实际跌幅百分比
price_drop_pct = (price_initial - price_new_exact) / price_initial * 100

# 存入结果
result = {
    'price_drop_pct': price_drop_pct
}

print(result)
