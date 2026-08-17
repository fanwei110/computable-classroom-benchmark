import numpy as np
from scipy.optimize import newton

# 债券参数
face_value = 100  # 面值
annual_coupon_rate = 0.046  # 年票息率 4.6%
ytm_initial = 0.053  # 初始到期收益率 5.3%
years_to_maturity = 7  # 剩余期限 7 年
coupon_frequency = 2  # 每年付息次数（半年付息）
yield_change_bp = 80  # 收益率变动 80 个基点
yield_change = yield_change_bp / 10000  # 转换为小数

# 计算每期票息
coupon_payment = (face_value * annual_coupon_rate) / coupon_frequency

# 定义债券定价函数（现金流贴现）
def bond_price(ytm, face_value, coupon_payment, periods, frequency):
    """
    计算债券价格
    ytm: 年化到期收益率
    face_value: 面值
    coupon_payment: 每期票息
    periods: 剩余期数
    frequency: 每年付息次数
    """
    periodic_ytm = ytm / frequency
    cash_flows = np.full(periods, coupon_payment)
    cash_flows[-1] += face_value  # 最后一期包含面值
    price = np.sum(cash_flows / (1 + periodic_ytm) ** np.arange(1, periods + 1))
    return price

# 计算初始价格
periods = years_to_maturity * coupon_frequency
initial_price = bond_price(ytm_initial, face_value, coupon_payment, periods, coupon_frequency)

# 计算久期（Macaulay Duration）和修正久期
def macaulay_duration(ytm, face_value, coupon_payment, periods, frequency):
    """
    计算 Macaulay 久期
    """
    periodic_ytm = ytm / frequency
    cash_flows = np.full(periods, coupon_payment)
    cash_flows[-1] += face_value
    discounted_cash_flows = cash_flows / (1 + periodic_ytm) ** np.arange(1, periods + 1)
    weights = discounted_cash_flows / bond_price(ytm, face_value, coupon_payment, periods, frequency)
    duration = np.sum(weights * np.arange(1, periods + 1)) / frequency
    return duration

def modified_duration(ytm, face_value, coupon_payment, periods, frequency):
    """
    计算修正久期
    """
    mac_dur = macaulay_duration(ytm, face_value, coupon_payment, periods, frequency)
    periodic_ytm = ytm / frequency
    mod_dur = mac_dur / (1 + periodic_ytm)
    return mod_dur

# 计算凸性
def convexity(ytm, face_value, coupon_payment, periods, frequency):
    """
    计算凸性
    """
    periodic_ytm = ytm / frequency
    cash_flows = np.full(periods, coupon_payment)
    cash_flows[-1] += face_value
    discounted_cash_flows = cash_flows / (1 + periodic_ytm) ** np.arange(1, periods + 1)
    weights = discounted_cash_flows / bond_price(ytm, face_value, coupon_payment, periods, frequency)
    conv = np.sum(weights * np.arange(1, periods + 1) * (np.arange(1, periods + 1) + 1)) / (frequency ** 2 * (1 + periodic_ytm) ** 2)
    return conv

# 计算久期和凸性
mod_dur = modified_duration(ytm_initial, face_value, coupon_payment, periods, coupon_frequency)
conv = convexity(ytm_initial, face_value, coupon_payment, periods, coupon_frequency)

# 估算价格变化（使用久期和凸性近似）
price_drop_pct = -mod_dur * yield_change + 0.5 * conv * (yield_change ** 2)
price_drop_pct *= 100  # 转换为百分比

# 精确计算新价格（验证近似效果）
new_ytm = ytm_initial + yield_change
new_price = bond_price(new_ytm, face_value, coupon_payment, periods, coupon_frequency)
exact_price_drop_pct = ((new_price - initial_price) / initial_price) * 100

# 结果存储
result = {
    'price_drop_pct': price_drop_pct  # 使用久期和凸性近似的跌幅百分比
}

# 输出结果（可选，便于调试）
print(f"初始价格: {initial_price:.4f}")
print(f"修正久期: {mod_dur:.4f}")
print(f"凸性: {conv:.4f}")
print(f"估算跌幅: {price_drop_pct:.4f}%")
print(f"精确跌幅: {exact_price_drop_pct:.4f}%")
