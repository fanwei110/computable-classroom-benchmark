import numpy as np
from scipy.optimize import newton

# 债券参数
face_value = 100.0
coupon_rate = 0.046
years_to_maturity = 7
ytm = 0.053  # 到期收益率
coupon_payment = face_value * coupon_rate
periods_per_year = 1  # 假设每年付息一次

# 1. 计算债券价格（现金流贴现之和）
def bond_price(yield_to_maturity, face_value, coupon_payment, years_to_maturity, periods_per_year=1):
    total_periods = years_to_maturity * periods_per_year
    discount_rate_period = yield_to_maturity / periods_per_year
    cash_flows = np.array([coupon_payment] * (total_periods - 1) + [coupon_payment + face_value])
    periods = np.arange(1, total_periods + 1)
    present_values = cash_flows / ((1 + discount_rate_period) ** periods)
    return np.sum(present_values)

price = bond_price(ytm, face_value, coupon_payment, years_to_maturity, periods_per_year)

# 2. 计算麦考利久期和修正久期
def macaulay_duration(yield_to_maturity, face_value, coupon_payment, years_to_maturity, periods_per_year=1):
    total_periods = years_to_maturity * periods_per_year
    discount_rate_period = yield_to_maturity / periods_per_year
    cash_flows = np.array([coupon_payment] * (total_periods - 1) + [coupon_payment + face_value])
    periods = np.arange(1, total_periods + 1)
    present_values = cash_flows / ((1 + discount_rate_period) ** periods)
    weighted_cash_flows = present_values * periods
    mac_dur = np.sum(weighted_cash_flows) / np.sum(present_values)
    return mac_dur / periods_per_year  # 转换为年久期

def modified_duration(macaulay_duration, yield_to_maturity, periods_per_year=1):
    return macaulay_duration / (1 + yield_to_maturity / periods_per_year)

macaulay_dur = macaulay_duration(ytm, face_value, coupon_payment, years_to_maturity, periods_per_year)
modified_dur = modified_duration(macaulay_dur, ytm, periods_per_year)

# 3. 计算凸性
def convexity(yield_to_maturity, face_value, coupon_payment, years_to_maturity, periods_per_year=1):
    total_periods = years_to_maturity * periods_per_year
    discount_rate_period = yield_to_maturity / periods_per_year
    cash_flows = np.array([coupon_payment] * (total_periods - 1) + [coupon_payment + face_value])
    periods = np.arange(1, total_periods + 1)
    present_values = cash_flows / ((1 + discount_rate_period) ** periods)
    weighted_cash_flows = present_values * periods * (periods + 1)
    conv = np.sum(weighted_cash_flows) / (np.sum(present_values) * (1 + discount_rate_period)**2)
    return conv / (periods_per_year ** 2)  # 转换为年凸性

conv = convexity(ytm, face_value, coupon_payment, years_to_maturity, periods_per_year)

# 4. 填充结果字典
result = {
    'price': price,
    'macaulay_duration_years': macaulay_dur,
    'modified_duration_years': modified_dur,
    'convexity': conv
}

# 输出结果以供验证
print(result)
