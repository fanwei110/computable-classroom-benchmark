import numpy as np
from scipy.optimize import newton

# 债券参数
face_value = 100.0
coupon_rate = 0.046
years_to_maturity = 7
ytm = 0.053  # 到期收益率
coupon_payment = face_value * coupon_rate
periods_per_year = 1  # 假设每年付息一次
total_periods = years_to_maturity * periods_per_year

# 1. 计算债券价格（现金流贴现之和）
def bond_price(yield_to_maturity):
    cash_flows = np.array([coupon_payment] * total_periods + [face_value])
    periods = np.arange(1, total_periods + 2)
    discount_factors = (1 + yield_to_maturity / periods_per_year) ** -periods
    return np.sum(cash_flows * discount_factors)

price = bond_price(ytm)

# 2. 计算麦考利久期和修正久期
def macaulay_duration(yield_to_maturity):
    cash_flows = np.array([coupon_payment] * total_periods + [face_value])
    periods = np.arange(1, total_periods + 2)
    discount_factors = (1 + yield_to_maturity / periods_per_year) ** -periods
    discounted_cash_flows = cash_flows * discount_factors
    weighted_periods = discounted_cash_flows * periods
    return np.sum(weighted_periods) / (price * periods_per_year)

macaulay_duration_years = macaulay_duration(ytm)
modified_duration_years = macaulay_duration_years / (1 + ytm / periods_per_year)

# 3. 计算凸性
def convexity(yield_to_maturity):
    cash_flows = np.array([coupon_payment] * total_periods + [face_value])
    periods = np.arange(1, total_periods + 2)
    discount_factors = (1 + yield_to_maturity / periods_per_year) ** -periods
    weighted_periods_squared = cash_flows * discount_factors * periods * (periods + 1)
    return np.sum(weighted_periods_squared) / (price * (1 + yield_to_maturity / periods_per_year)**2 * periods_per_year**2)

convexity_value = convexity(ytm)

# 4. 填充结果字典
result = {
    'price': round(price, 4),
    'macaulay_duration_years': round(macaulay_duration_years, 4),
    'modified_duration_years': round(modified_duration_years, 4),
    'convexity': round(convexity_value, 4)
}

print(result)
