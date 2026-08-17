import numpy as np
from scipy.optimize import newton

# 债券参数
face_value = 100.0          # 面值
coupon_rate = 0.046         # 票息率 4.6%
ytm_current = 0.053         # 当前收益率 5.3%
maturity_years = 7          # 到期年限
coupon_freq = 2             # 每年付息次数（半年付息）
yield_rise_bps = 80         # 收益率上升基点数

# 计算每期票息
coupon_per_period = face_value * coupon_rate / coupon_freq

# 计算总期数
total_periods = maturity_years * coupon_freq

# 定义债券定价函数：现金流贴现之和
def bond_price(ytm, face_value, coupon, periods, freq):
    ytm_period = ytm / freq
    cash_flows = np.full(periods, coupon)
    cash_flows[-1] += face_value  # 最后一期加上面值
    discount_factors = (1 + ytm_period) ** np.arange(1, periods + 1)
    return np.sum(cash_flows / discount_factors)

# 计算当前价格
price_current = bond_price(ytm_current, face_value, coupon_per_period, total_periods, coupon_freq)

# 定义久期计算函数（Macaulay久期）
def macaulay_duration(ytm, face_value, coupon, periods, freq):
    ytm_period = ytm / freq
    cash_flows = np.full(periods, coupon)
    cash_flows[-1] += face_value
    discount_factors = (1 + ytm_period) ** np.arange(1, periods + 1)
    pv_cash_flows = cash_flows / discount_factors
    weighted_times = np.arange(1, periods + 1) * pv_cash_flows
    return np.sum(weighted_times) / (freq * np.sum(pv_cash_flows))

# 计算修正久期（Modified Duration）
duration_macaulay = macaulay_duration(ytm_current, face_value, coupon_per_period, total_periods, coupon_freq)
duration_modified = duration_macaulay / (1 + ytm_current / coupon_freq)

# 定义凸性计算函数
def convexity(ytm, face_value, coupon, periods, freq):
    ytm_period = ytm / freq
    cash_flows = np.full(periods, coupon)
    cash_flows[-1] += face_value
    discount_factors = (1 + ytm_period) ** np.arange(1, periods + 1)
    pv_cash_flows = cash_flows / discount_factors
    weighted_times = np.arange(1, periods + 1) * (np.arange(1, periods + 1) + 1) * pv_cash_flows
    return np.sum(weighted_times) / ((1 + ytm_period)**2 * freq**2 * np.sum(pv_cash_flows))

# 计算凸性
bond_convexity = convexity(ytm_current, face_value, coupon_per_period, total_periods, coupon_freq)

# 收益率变动（绝对值）
delta_ytm = yield_rise_bps / 10000  # 基点转换为小数

# 使用久期和凸性估算价格变动百分比
price_drop_pct_approx = -duration_modified * delta_ytm * 100 + 0.5 * bond_convexity * (delta_ytm ** 2) * 100

# 精确计算新价格
ytm_new = ytm_current + delta_ytm
price_new = bond_price(ytm_new, face_value, coupon_per_period, total_periods, coupon_freq)
price_drop_pct_exact = (price_current - price_new) / price_current * 100

# 结果存储
result = {
    'price_drop_pct': price_drop_pct_exact  # 使用精确计算结果
}

print(result)
