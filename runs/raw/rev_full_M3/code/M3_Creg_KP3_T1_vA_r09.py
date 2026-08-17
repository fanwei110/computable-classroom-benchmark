import numpy as np

# 债券参数
face_value = 100.0
coupon_rate = 0.046
years_to_maturity = 7
ytm = 0.053  # 到期收益率 (Yield to Maturity)

# 计算每年的现金流
# 假设按年支付票息，这是此类标准计算题的默认约定
coupon_payment = face_value * coupon_rate
t = np.arange(1, years_to_maturity + 1)
cash_flows = np.full(years_to_maturity, coupon_payment)
cash_flows[-1] += face_value  # 最后一期加上面值

# 计算各期现金流的折现因子和现值
discount_factors = (1 + ytm) ** t
present_values = cash_flows / discount_factors

# 1. 计算债券价格
price = np.sum(present_values)

# 2. 计算麦考利久期
# Macaulay Duration = Sum(t * PV_cf) / Price
macaulay_duration = np.sum(t * present_values) / price

# 3. 计算修正久期
# Modified Duration = Macaulay Duration / (1 + ytm)
modified_duration = macaulay_duration / (1 + ytm)

# 4. 计算凸性
# Convexity = Sum[t * (t+1) * PV_cf] / [Price * (1+ytm)^2]
convexity = np.sum(t * (t + 1) * present_values) / (price * (1 + ytm)**2)

# 将结果存入指定格式的字典，保留6位小数以确保可复现性
result = {
    'price': round(price, 6),
    'macaulay_duration_years': round(macaulay_duration, 6),
    'modified_duration_years': round(modified_duration, 6),
    'convexity': round(convexity, 6)
}

# 打印结果以便验证
print(result)
