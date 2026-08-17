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
def calculate_price(yield_per_period, face_value, coupon_payment, total_periods):
    cash_flows = np.full(total_periods, coupon_payment)
    cash_flows[-1] += face_value  # 最后一期包含本金
    discount_factors = (1 + yield_per_period) ** np.arange(1, total_periods + 1)
    price = np.sum(cash_flows / discount_factors)
    return price

yield_per_period = ytm / periods_per_year
price = calculate_price(yield_per_period, face_value, coupon_payment, total_periods)

# 2. 计算麦考利久期和修正久期
def calculate_macaulay_duration(yield_per_period, face_value, coupon_payment, total_periods):
    cash_flows = np.full(total_periods, coupon_payment)
    cash_flows[-1] += face_value
    discount_factors = (1 + yield_per_period) ** np.arange(1, total_periods + 1)
    discounted_cash_flows = cash_flows / discount_factors
    weights = discounted_cash_flows / np.sum(discounted_cash_flows)
    macaulay_duration_periods = np.sum(weights * np.arange(1, total_periods + 1))
    macaulay_duration_years = macaulay_duration_periods / periods_per_year
    modified_duration_years = macaulay_duration_years / (1 + yield_per_period)
    return macaulay_duration_years, modified_duration_years

macaulay_duration_years, modified_duration_years = calculate_macaulay_duration(
    yield_per_period, face_value, coupon_payment, total_periods
)

# 3. 计算凸性
def calculate_convexity(yield_per_period, face_value, coupon_payment, total_periods):
    cash_flows = np.full(total_periods, coupon_payment)
    cash_flows[-1] += face_value
    discount_factors = (1 + yield_per_period) ** np.arange(1, total_periods + 1)
    discounted_cash_flows = cash_flows / discount_factors
    convexity_periods = np.sum(
        discounted_cash_flows * np.arange(1, total_periods + 1) * (np.arange(1, total_periods + 1) + 1)
    ) / ((1 + yield_per_period) ** 2 * np.sum(discounted_cash_flows))
    convexity = convexity_periods / (periods_per_year ** 2)
    return convexity

convexity = calculate_convexity(yield_per_period, face_value, coupon_payment, total_periods)

# 4. 填充结果字典
result = {
    'price': price,
    'macaulay_duration_years': macaulay_duration_years,
    'modified_duration_years': modified_duration_years,
    'convexity': convexity
}

# 输出结果（可选，便于调试）
print(result)
