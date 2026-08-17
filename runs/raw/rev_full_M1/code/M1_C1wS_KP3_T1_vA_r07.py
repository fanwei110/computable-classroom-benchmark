import numpy as np
from scipy.optimize import newton

# 债券参数
face_value = 100.0          # 面值
coupon_rate = 0.046         # 票面利率（年化）
years_to_maturity = 7       # 期限（年）
ytm = 0.053                 # 到期收益率（年化）
coupon_frequency = 2        # 每年付息次数（半年付息）

# 计算每期票息和期数
periods = years_to_maturity * coupon_frequency
coupon_payment = (face_value * coupon_rate) / coupon_frequency

# 生成现金流：每期票息 + 到期面值
cash_flows = np.full(periods, coupon_payment)
cash_flows[-1] += face_value  # 最后一期加上面值

# 1. 计算债券价格（现金流贴现之和）
discount_rates = (1 + ytm / coupon_frequency) ** np.arange(1, periods + 1)
price = np.sum(cash_flows / discount_rates)

# 2. 计算 Macaulay 久期和修正久期
# 计算每期现金流的贡献（时间加权贴现值）
time_periods = np.arange(1, periods + 1) / coupon_frequency  # 转换为年
weighted_cash_flows = (time_periods * cash_flows) / discount_rates
macaulay_duration_years = np.sum(weighted_cash_flows) / price

# 修正久期 = Macaulay久期 / (1 + ytm / coupon_frequency)
modified_duration_years = macaulay_duration_years / (1 + ytm / coupon_frequency)

# 3. 计算凸性
# 计算每期现金流的二阶贡献（时间平方加权贴现值）
convexity_weights = time_periods * (time_periods + 1 / coupon_frequency)
weighted_convexity_cash_flows = (convexity_weights * cash_flows) / discount_rates
convexity = np.sum(weighted_convexity_cash_flows) / (price * (1 + ytm / coupon_frequency) ** 2)

# 4. 填充结果字典
result = {
    'price': price,
    'macaulay_duration_years': macaulay_duration_years,
    'modified_duration_years': modified_duration_years,
    'convexity': convexity
}

# 输出结果（可选，便于调试）
print("债券定价结果:")
print(f"价格: {result['price']:.4f}")
print(f"Macaulay久期: {result['macaulay_duration_years']:.4f} 年")
print(f"修正久期: {result['modified_duration_years']:.4f} 年")
print(f"凸性: {result['convexity']:.4f}")
