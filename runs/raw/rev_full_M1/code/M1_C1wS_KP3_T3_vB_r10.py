import numpy as np
from scipy.optimize import newton

# 债券参数
face_value = 100          # 面值
annual_coupon_rate = 0.046  # 年票息率 4.6%
ytm_initial = 0.053       # 初始到期收益率 5.3%
years_to_maturity = 7     # 剩余期限 7 年
coupon_frequency = 2      # 每年付息次数（半年付息）
yield_change_bp = 80      # 收益率变动 80 个基点

# 计算每期票息
coupon_per_period = (face_value * annual_coupon_rate) / coupon_frequency

# 现金流：每期票息 + 到期面值
cash_flows = np.array([coupon_per_period] * (years_to_maturity * coupon_frequency))
cash_flows[-1] += face_value  # 最后一期加上面值

# 计算初始价格（现金流贴现）
periods = np.arange(1, years_to_maturity * coupon_frequency + 1)
initial_price = np.sum(cash_flows / ((1 + ytm_initial / coupon_frequency) ** periods))

# 定义价格函数（用于久期和凸性计算）
def bond_price(yield_per_period):
    return np.sum(cash_flows / ((1 + yield_per_period) ** periods))

# 计算久期（Macaulay Duration）和修正久期
yield_per_period_initial = ytm_initial / coupon_frequency
weights = cash_flows / ((1 + yield_per_period_initial) ** periods) / initial_price
macaulay_duration = np.sum(periods * weights)
modified_duration = macaulay_duration / (1 + yield_per_period_initial)

# 计算凸性
convexity = np.sum(periods * (periods + 1) * cash_flows / ((1 + yield_per_period_initial) ** (periods + 2))) / initial_price
convexity /= (1 + yield_per_period_initial) ** 2

# 收益率变动（绝对值）
delta_yield = yield_change_bp / 10000  # 80bp = 0.008

# 使用久期-凸性近似估计价格变动
price_drop_approx = -modified_duration * delta_yield + 0.5 * convexity * (delta_yield ** 2)
price_drop_pct = price_drop_approx * 100

# 精确计算新价格（验证近似效果）
new_yield_per_period = (ytm_initial + delta_yield) / coupon_frequency
new_price = bond_price(new_yield_per_period)
exact_price_drop_pct = ((initial_price - new_price) / initial_price) * 100

# 结果存储
result = {
    'price_drop_pct': round(exact_price_drop_pct, 4)  # 使用精确计算结果，保留4位小数
}

print(result)
