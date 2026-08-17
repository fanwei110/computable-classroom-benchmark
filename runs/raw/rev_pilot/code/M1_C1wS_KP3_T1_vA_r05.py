import numpy as np
from scipy.optimize import newton

# 债券参数
face_value = 100.0          # 面值
coupon_rate = 0.046         # 票面利率
years_to_maturity = 7       # 期限（年）
ytm = 0.053                 # 到期收益率（年化）
frequency = 2               # 每年付息次数（半年付息）

# 计算每期现金流
periods = years_to_maturity * frequency
coupon_payment = face_value * coupon_rate / frequency
cash_flows = np.full(periods, coupon_payment)
cash_flows[-1] += face_value  # 最后一期加上面值

# 1. 计算债券价格（现金流贴现之和）
periodic_ytm = ytm / frequency
discount_factors = np.power(1 + periodic_ytm, -np.arange(1, periods + 1))
price = np.sum(cash_flows * discount_factors)

# 2. 计算Macaulay久期和修正久期
weighted_cash_flows = cash_flows * discount_factors * np.arange(1, periods + 1)
macaulay_duration_periods = np.sum(weighted_cash_flows) / price
macaulay_duration_years = macaulay_duration_periods / frequency
modified_duration_years = macaulay_duration_years / (1 + ytm / frequency)

# 3. 计算凸性
weighted_cash_flows_convexity = cash_flows * discount_factors * np.arange(1, periods + 1) * (np.arange(1, periods + 1) + 1)
convexity_periods = np.sum(weighted_cash_flows_convexity) / price
convexity = convexity_periods / (frequency ** 2 * (1 + periodic_ytm) ** 2)

# 结果存储
result = {
    'price': round(price, 4),
    'macaulay_duration_years': round(macaulay_duration_years, 4),
    'modified_duration_years': round(modified_duration_years, 4),
    'convexity': round(convexity, 4)
}

print(result)
