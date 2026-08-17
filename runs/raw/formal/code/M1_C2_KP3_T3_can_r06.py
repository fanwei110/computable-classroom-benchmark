import numpy as np
from scipy.optimize import newton

# 债券参数
face_value = 100
coupon_rate = 0.046
ytm_current = 0.053  # 当前收益率
years_to_maturity = 7
coupon_frequency = 2  # 半年付息一次
ytm_increase_bps = 80  # 收益率上升基点数

# 计算每期票息
coupon_payment = face_value * coupon_rate / coupon_frequency

# 定义债券定价函数
def bond_price(ytm, face_value, coupon_payment, years_to_maturity, coupon_frequency):
    total_periods = years_to_maturity * coupon_frequency
    periodic_ytm = ytm / coupon_frequency
    cash_flows = np.full(total_periods, coupon_payment)
    cash_flows[-1] += face_value  # 最后一期加上面值
    discount_factors = (1 + periodic_ytm) ** np.arange(1, total_periods + 1)
    price = np.sum(cash_flows / discount_factors)
    return price

# 计算当前价格
current_price = bond_price(ytm_current, face_value, coupon_payment, years_to_maturity, coupon_frequency)

# 计算久期和凸性
def bond_duration_convexity(ytm, face_value, coupon_payment, years_to_maturity, coupon_frequency):
    total_periods = years_to_maturity * coupon_frequency
    periodic_ytm = ytm / coupon_frequency
    cash_flows = np.full(total_periods, coupon_payment)
    cash_flows[-1] += face_value

    # 计算久期
    discount_factors = (1 + periodic_ytm) ** np.arange(1, total_periods + 1)
    present_values = cash_flows / discount_factors
    weights = present_values / np.sum(present_values)
    duration = np.sum(weights * np.arange(1, total_periods + 1)) / coupon_frequency

    # 计算凸性
    convexity = np.sum(weights * np.arange(1, total_periods + 1) * (np.arange(1, total_periods + 1) + 1)) / (coupon_frequency ** 2 * (1 + periodic_ytm) ** 2)

    return duration, convexity

duration, convexity = bond_duration_convexity(ytm_current, face_value, coupon_payment, years_to_maturity, coupon_frequency)

# 计算新的收益率
ytm_new = ytm_current + ytm_increase_bps / 10000

# 精确计算新价格
new_price_exact = bond_price(ytm_new, face_value, coupon_payment, years_to_maturity, coupon_frequency)

# 使用久期和凸性估算价格变化
price_drop_estimate = -duration * (ytm_new - ytm_current) + 0.5 * convexity * (ytm_new - ytm_current) ** 2
estimated_price = current_price * (1 + price_drop_estimate)

# 计算实际跌幅百分比
price_drop_pct = (current_price - new_price_exact) / current_price * 100

# 存储结果
result = {
    'price_drop_pct': price_drop_pct
}

print(result)
