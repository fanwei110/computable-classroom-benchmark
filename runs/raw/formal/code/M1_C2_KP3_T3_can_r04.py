import numpy as np
from scipy.optimize import newton

# 债券参数
face_value = 100
coupon_rate = 0.046
yield_initial = 0.053  # 初始收益率
maturity_years = 7
coupon_frequency = 2  # 每年付息次数（半年付息）

# 计算参数
periods = maturity_years * coupon_frequency
coupon_payment = face_value * coupon_rate / coupon_frequency
yield_period = yield_initial / coupon_frequency

# 1. 计算当前价格（现金流贴现之和）
def bond_price(yield_per_period):
    cash_flows = np.full(periods, coupon_payment)
    cash_flows[-1] += face_value  # 最后一期包含本金
    discount_factors = (1 + yield_per_period) ** np.arange(1, periods + 1)
    return np.sum(cash_flows / discount_factors)

price_initial = bond_price(yield_period)

# 2. 计算久期和凸性
def bond_price_derivatives(yield_per_period):
    cash_flows = np.full(periods, coupon_payment)
    cash_flows[-1] += face_value
    t = np.arange(1, periods + 1)
    discount_factors = (1 + yield_per_period) ** t

    # 久期 (Macaulay Duration)
    weighted_cash_flows = cash_flows * t / discount_factors
    macaulay_duration = np.sum(weighted_cash_flows) / price_initial
    modified_duration = macaulay_duration / (1 + yield_per_period)

    # 凸性
    convexity = np.sum(cash_flows * t * (t + 1) / (discount_factors * (1 + yield_per_period)**2)) / price_initial

    return modified_duration, convexity

modified_duration, convexity = bond_price_derivatives(yield_period)

# 3. 估算收益率变化对价格的影响
yield_change_bps = 80  # 80个基点
yield_change = yield_change_bps / 10000  # 转换为小数

# 使用久期和凸性近似价格变化
price_drop_pct = -modified_duration * yield_change + 0.5 * convexity * (yield_change ** 2)
price_drop_pct *= 100  # 转换为百分比

# 精确计算新价格（验证近似效果）
new_yield_period = (yield_initial + yield_change) / coupon_frequency
price_new = bond_price(new_yield_period)
price_drop_pct_exact = (price_initial - price_new) / price_initial * 100

# 结果存储
result = {
    'price_drop_pct': price_drop_pct  # 使用久期-凸性近似结果
}

# 输出验证（可选，不影响result）
print(f"初始价格: {price_initial:.4f}")
print(f"久期: {modified_duration:.4f}")
print(f"凸性: {convexity:.4f}")
print(f"近似跌幅: {price_drop_pct:.4f}%")
print(f"精确跌幅: {price_drop_pct_exact:.4f}%")
