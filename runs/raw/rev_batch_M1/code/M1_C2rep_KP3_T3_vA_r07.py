import numpy as np
from scipy.optimize import newton

# 债券参数
face_value = 100.0          # 面值
coupon_rate = 0.046         # 票息率 4.6%
ytm_current = 0.053         # 当前收益率 5.3%
years_to_maturity = 7       # 剩余期限 7 年
coupon_freq = 2             # 每年付息次数（半年付息）
yield_change_bps = 80       # 收益率变动 80 个基点

# 计算每期票息
coupon_payment = face_value * coupon_rate / coupon_freq

# 定义债券定价函数：现金流贴现求和
def bond_price(ytm, face_value, coupon_payment, years_to_maturity, coupon_freq):
    periods = years_to_maturity * coupon_freq
    cash_flows = np.full(periods, coupon_payment)
    cash_flows[-1] += face_value  # 最后一期加上面值
    discount_factors = (1 + ytm / coupon_freq) ** np.arange(1, periods + 1)
    return np.sum(cash_flows / discount_factors)

# 计算当前价格
price_current = bond_price(ytm_current, face_value, coupon_payment, years_to_maturity, coupon_freq)

# 定义久期和凸性计算函数
def macaulay_duration_convexity(ytm, face_value, coupon_payment, years_to_maturity, coupon_freq):
    periods = years_to_maturity * coupon_freq
    cash_flows = np.full(periods, coupon_payment)
    cash_flows[-1] += face_value
    discount_factors = (1 + ytm / coupon_freq) ** np.arange(1, periods + 1)
    pv_cash_flows = cash_flows / discount_factors
    weights = pv_cash_flows / np.sum(pv_cash_flows)
    time_periods = np.arange(1, periods + 1) / coupon_freq
    mac_dur = np.sum(weights * time_periods)
    convexity = np.sum(weights * time_periods * (time_periods + 1 / coupon_freq)) / (1 + ytm / coupon_freq)**2
    return mac_dur, convexity

# 计算久期和凸性
macaulay_dur, convexity = macaulay_duration_convexity(
    ytm_current, face_value, coupon_payment, years_to_maturity, coupon_freq
)
modified_dur = macaulay_dur / (1 + ytm_current / coupon_freq)

# 估算价格变动（久期 + 凸性近似）
yield_change = yield_change_bps / 10000  # 基点转换为小数
price_drop_pct_approx = -modified_dur * yield_change * 100 + 0.5 * convexity * (yield_change**2) * 100

# 精确计算新价格
ytm_new = ytm_current + yield_change
price_new = bond_price(ytm_new, face_value, coupon_payment, years_to_maturity, coupon_freq)
price_drop_pct_exact = (price_new - price_current) / price_current * 100

# 结果存储
result = {
    'price_drop_pct': price_drop_pct_exact  # 使用精确计算的跌幅
}

print(result)
