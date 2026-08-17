import numpy as np
from scipy.optimize import newton

# 债券参数
face_value = 100
coupon_rate = 0.046
ytm_initial = 0.053  # 初始收益率
maturity_years = 7
periods_per_year = 2  # 假设半年付息一次
yield_rise_bps = 80  # 收益率上升基点数

# 计算相关参数
total_periods = maturity_years * periods_per_year
coupon_payment = face_value * coupon_rate / periods_per_year
yield_per_period_initial = ytm_initial / periods_per_year
yield_rise_per_period = yield_rise_bps / 10000 / periods_per_year  # 转换为每期收益率变化

# 1. 计算当前收益率下的债券价格
def bond_price(yield_per_period):
    """计算债券价格"""
    cash_flows = np.full(total_periods, coupon_payment)
    cash_flows[-1] += face_value  # 最后一期加上面值
    discount_factors = (1 + yield_per_period) ** np.arange(1, total_periods + 1)
    return np.sum(cash_flows / discount_factors)

price_initial = bond_price(yield_per_period_initial)

# 2. 计算久期和凸性
def bond_duration_convexity(yield_per_period):
    """计算麦考利久期和凸性"""
    cash_flows = np.full(total_periods, coupon_payment)
    cash_flows[-1] += face_value
    periods = np.arange(1, total_periods + 1)
    discount_factors = (1 + yield_per_period) ** periods
    discounted_cash_flows = cash_flows / discount_factors

    # 麦考利久期
    macaulay_duration = np.sum(periods * discounted_cash_flows) / price_initial
    # 修正久期
    modified_duration = macaulay_duration / (1 + yield_per_period)
    # 凸性
    convexity = np.sum(periods * (periods + 1) * discounted_cash_flows) / (price_initial * (1 + yield_per_period)**2)

    return modified_duration, convexity

modified_duration, convexity = bond_duration_convexity(yield_per_period_initial)

# 3. 估算价格变化
yield_new_per_period = yield_per_period_initial + yield_rise_per_period
price_new = bond_price(yield_new_per_period)

# 使用久期和凸性估算价格变化
price_drop_estimate = -modified_duration * yield_rise_per_period * 100 + 0.5 * convexity * (yield_rise_per_period * 100)**2
price_drop_pct_estimate = price_drop_estimate / price_initial * 100

# 实际价格变化
price_drop_pct_actual = (price_initial - price_new) / price_initial * 100

# 结果存储
result = {
    'price_drop_pct': price_drop_pct_actual  # 使用实际价格变化作为最终结果
}

# 输出验证信息（可选，不影响结果）
print(f"初始价格: {price_initial:.4f}")
print(f"新价格: {price_new:.4f}")
print(f"实际跌幅: {price_drop_pct_actual:.4f}%")
print(f"久期-凸性估算跌幅: {price_drop_pct_estimate:.4f}%")
print(f"修正久期: {modified_duration:.4f}")
print(f"凸性: {convexity:.4f}")
