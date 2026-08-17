import numpy as np

# 债券参数
face_value = 100
coupon_rate = 0.046
years_to_maturity = 7
ytm = 0.053

# 由于约定“债券收益率按年复利报价”，默认为每年付息一次，现金流按年折现
annual_coupon = face_value * coupon_rate
cash_flows = np.array([annual_coupon] * (years_to_maturity - 1) + [annual_coupon + face_value])
times = np.arange(1, years_to_maturity + 1)

# 1. 计算债券价格
discount_factors = (1 + ytm) ** times
pv_cash_flows = cash_flows / discount_factors
price = np.sum(pv_cash_flows)

# 2. 计算麦考利久期
macaulay_duration_years = np.sum(times * pv_cash_flows) / price

# 3. 计算修正久期
modified_duration_years = macaulay_duration_years / (1 + ytm)

# 4. 计算凸性
# 凸性公式: Conv = (1/P) * sum[ CF_t * t * (t+1) / (1+y)^(t+2) ] 对于年付息债券
convexity = np.sum(cash_flows * times * (times + 1) / ((1 + ytm) ** (times + 2))) / price

# 按输出契约要求存入字典
result = {
    'price': price,
    'macaulay_duration_years': macaulay_duration_years,
    'modified_duration_years': modified_duration_years,
    'convexity': convexity
}
