import numpy as np
from scipy.optimize import newton

# 债券参数
face_value = 100
coupon_rate = 0.046
yield_to_maturity_initial = 0.053
years_to_maturity = 7
coupon_frequency = 2  # 半年付息一次

# 计算当前价格
def bond_price(yield_rate, face_value, coupon_rate, years_to_maturity, coupon_frequency):
    periods = years_to_maturity * coupon_frequency
    coupon_payment = face_value * coupon_rate / coupon_frequency
    discount_rate = yield_rate / coupon_frequency

    # 现金流贴现
    price = sum([coupon_payment / ((1 + discount_rate) ** t) for t in range(1, int(periods) + 1)])
    price += face_value / ((1 + discount_rate) ** periods)
    return price

# 计算久期 (Macaulay Duration)
def macaulay_duration(yield_rate, face_value, coupon_rate, years_to_maturity, coupon_frequency):
    periods = years_to_maturity * coupon_frequency
    coupon_payment = face_value * coupon_rate / coupon_frequency
    discount_rate = yield_rate / coupon_frequency

    # 计算每期现金流的贴现值
    cash_flows = [coupon_payment] * int(periods)
    cash_flows[-1] += face_value  # 最后一期加上面值

    discounted_cash_flows = [cf / ((1 + discount_rate) ** t) for t, cf in enumerate(cash_flows, 1)]
    price = sum(discounted_cash_flows)

    # 计算久期
    duration = sum([t * dcf for t, dcf in enumerate(discounted_cash_flows, 1)]) / price
    return duration / coupon_frequency  # 转换为年化久期

# 计算修正久期
def modified_duration(macaulay_duration, yield_rate, coupon_frequency):
    return macaulay_duration / (1 + yield_rate / coupon_frequency)

# 计算凸性
def convexity(yield_rate, face_value, coupon_rate, years_to_maturity, coupon_frequency):
    periods = years_to_maturity * coupon_frequency
    coupon_payment = face_value * coupon_rate / coupon_frequency
    discount_rate = yield_rate / coupon_frequency

    cash_flows = [coupon_payment] * int(periods)
    cash_flows[-1] += face_value

    discounted_cash_flows = [cf / ((1 + discount_rate) ** t) for t, cf in enumerate(cash_flows, 1)]
    price = sum(discounted_cash_flows)

    convexity_sum = sum([t * (t + 1) * dcf for t, dcf in enumerate(discounted_cash_flows, 1)])
    convexity_value = convexity_sum / (price * (1 + discount_rate) ** 2)
    return convexity_value / (coupon_frequency ** 2)  # 转换为年化凸性

# 计算当前价格
current_price = bond_price(yield_to_maturity_initial, face_value, coupon_rate, years_to_maturity, coupon_frequency)

# 计算久期和凸性
mac_dur = macaulay_duration(yield_to_maturity_initial, face_value, coupon_rate, years_to_maturity, coupon_frequency)
mod_dur = modified_duration(mac_dur, yield_to_maturity_initial, coupon_frequency)
conv = convexity(yield_to_maturity_initial, face_value, coupon_rate, years_to_maturity, coupon_frequency)

# 收益率变化 (80个基点 = 0.008)
delta_yield = 0.008

# 使用久期和凸性估算价格变化
price_drop_estimate = -mod_dur * delta_yield + 0.5 * conv * (delta_yield ** 2)
price_drop_pct = price_drop_estimate * 100

# 精确计算新价格
new_yield = yield_to_maturity_initial + delta_yield
new_price = bond_price(new_yield, face_value, coupon_rate, years_to_maturity, coupon_frequency)
exact_price_drop_pct = ((current_price - new_price) / current_price) * 100

# 结果存储
result = {
    'price_drop_pct': exact_price_drop_pct  # 使用精确计算的跌幅
}

print(result)
