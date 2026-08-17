import numpy as np

# 债券参数
face_value = 100.0          # 面值
coupon_rate = 0.046         # 票息率 4.6%
years_to_maturity = 7       # 期限 7 年
ytm = 0.053                 # 到期收益率 5.3%
frequency = 1               # 每年付息次数（假设为每年付息一次）

# 计算现金流
coupon_payment = face_value * coupon_rate
periods = np.arange(1, years_to_maturity * frequency + 1)
cash_flows = np.full_like(periods, coupon_payment, dtype=float)
cash_flows[-1] += face_value  # 最后一期加上面值

# 每期折现率
discount_rate = ytm / frequency

# 现值计算
discount_factors = (1 + discount_rate) ** periods
pv_cash_flows = cash_flows / discount_factors

# 1. 计算债券价格
price = np.sum(pv_cash_flows)

# 2. 计算麦考利久期 (Macaulay Duration)
# MacD = (1/P) * Σ [ t * PV(CF_t) ]
weighted_pv_time = periods * pv_cash_flows
macaulay_duration_periods = np.sum(weighted_pv_time) / price
macaulay_duration_years = macaulay_duration_periods / frequency

# 3. 计算修正久期 (Modified Duration)
# ModD = MacD / (1 + y)
modified_duration_years = macaulay_duration_years / (1 + discount_rate)

# 4. 计算凸性 (Convexity)
# Convexity = (1 / [P * (1+y)^2]) * Σ [ t*(t+1) * PV(CF_t) ]
weighted_pv_convexity = periods * (periods + 1) * pv_cash_flows
convexity_periods = np.sum(weighted_pv_convexity) / (price * (1 + discount_rate)**2)
# 年化凸性（对于每年付息一次的债券，直接就是计算出的值；若每年付息m次，通常年化凸性需除以 m^2）
convexity = convexity_periods / (frequency**2)

# 按照输出契约存入字典
result = {
    'price': price,
    'macaulay_duration_years': macaulay_duration_years,
    'modified_duration_years': modified_duration_years,
    'convexity': convexity
}

# 打印结果以供验证
print("Bond Calculation Results:")
for key, value in result.items():
    print(f"{key}: {value:.6f}")
