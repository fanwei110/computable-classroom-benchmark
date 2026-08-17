import numpy as np
from scipy.optimize import root_scalar

# 债券参数
face_value = 100.0
coupon_rate = 0.046
years_to_maturity = 7
ytm = 0.053  # 到期收益率
coupon_payment = face_value * coupon_rate
periods_per_year = 1  # 假设每年付息一次
total_periods = years_to_maturity * periods_per_year

# 1. 计算债券价格（现金流贴现之和）
def calculate_price(yield_rate):
    cash_flows = np.array([coupon_payment] * (total_periods - 1) + [coupon_payment + face_value])
    discount_factors = np.array([(1 + yield_rate) ** (-t) for t in range(1, total_periods + 1)])
    price = np.sum(cash_flows * discount_factors)
    return price

price = calculate_price(ytm)

# 2. 计算麦考利久期和修正久期
def calculate_macaulay_duration(yield_rate):
    cash_flows = np.array([coupon_payment] * (total_periods - 1) + [coupon_payment + face_value])
    times = np.arange(1, total_periods + 1)
    discount_factors = np.array([(1 + yield_rate) ** (-t) for t in times])
    discounted_cash_flows = cash_flows * discount_factors
    macaulay_duration = np.sum(times * discounted_cash_flows) / np.sum(discounted_cash_flows)
    return macaulay_duration / periods_per_year  # 转换为年

macaulay_duration_years = calculate_macaulay_duration(ytm)
modified_duration_years = macaulay_duration_years / (1 + ytm / periods_per_year)

# 3. 计算凸性
def calculate_convexity(yield_rate):
    cash_flows = np.array([coupon_payment] * (total_periods - 1) + [coupon_payment + face_value])
    times = np.arange(1, total_periods + 1)
    discount_factors = np.array([(1 + yield_rate) ** (-t) for t in times])
    convexity = np.sum(times * (times + 1) * cash_flows * discount_factors) / ((1 + yield_rate) ** 2 * np.sum(cash_flows * discount_factors))
    return convexity / (periods_per_year ** 2)  # 转换为年

convexity = calculate_convexity(ytm)

# 4. 填充结果字典
result = {
    'price': round(price, 4),
    'macaulay_duration_years': round(macaulay_duration_years, 4),
    'modified_duration_years': round(modified_duration_years, 4),
    'convexity': round(convexity, 4)
}

print(result)
