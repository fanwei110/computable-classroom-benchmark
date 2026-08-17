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
    cash_flows = np.array([coupon_payment] * (total_periods - 1) + [coupon_payment + face_value])
    discount_factors = np.power(1 + yield_to_maturity / periods_per_year, -np.arange(1, total_periods + 1))
    price = np.sum(cash_flows * discount_factors)
    return price

price = bond_price(ytm, face_value, coupon_payment, years_to_maturity, periods_per_year)

# 2. 计算麦考利久期和修正久期
def macaulay_duration(yield_to_maturity, face_value, coupon_payment, years_to_maturity, periods_per_year=1):
    total_periods = years_to_maturity * periods_per_year
    cash_flows = np.array([coupon_payment] * (total_periods - 1) + [coupon_payment + face_value])
    discount_factors = np.power(1 + yield_to_maturity / periods_per_year, -np.arange(1, total_periods + 1))
    discounted_cash_flows = cash_flows * discount_factors
    time_periods = np.arange(1, total_periods + 1) / periods_per_year
    mac_dur = np.sum(time_periods * discounted_cash_flows) / np.sum(discounted_cash_flows)
    return mac_dur

macaulay_duration_years = macaulay_duration(ytm, face_value, coupon_payment, years_to_maturity, periods_per_year)
modified_duration_years = macaulay_duration_years / (1 + ytm / periods_per_year)

# 3. 计算凸性
def convexity(yield_to_maturity, face_value, coupon_payment, years_to_maturity, periods_per_year=1):
    total_periods = years_to_maturity * periods_per_year
    cash_flows = np.array([coupon_payment] * (total_periods - 1) + [coupon_payment + face_value])
    discount_factors = np.power(1 + yield_to_maturity / periods_per_year, -np.arange(1, total_periods + 1))
    time_periods = np.arange(1, total_periods + 1) / periods_per_year
    conv = np.sum(time_periods * (time_periods + 1 / periods_per_year) * cash_flows * discount_factors) / \
           (np.sum(cash_flows * discount_factors) * (1 + yield_to_maturity / periods_per_year)**2)
    return conv

convexity_value = convexity(ytm, face_value, coupon_payment, years_to_maturity, periods_per_year)

# 4. 填充结果字典
result = {
    'price': price,
    'macaulay_duration_years': macaulay_duration_years,
    'modified_duration_years': modified_duration_years,
    'convexity': convexity_value
}

# 输出结果（可选，用于验证）
print(result)
