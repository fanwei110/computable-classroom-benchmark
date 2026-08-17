import numpy as np
from scipy.optimize import newton

# 债券参数
face_value = 100
coupon_rate = 0.046
ytm_initial = 0.053  # 初始收益率
years_to_maturity = 7
coupon_frequency = 2  # 半年付息一次
yield_change_bps = 80  # 收益率变化（基点）
yield_change = yield_change_bps / 10000  # 转换为小数

# 计算每期票息
coupon_payment = face_value * coupon_rate / coupon_frequency

# 定义债券定价函数（现金流贴现）
def bond_price(ytm, face_value, coupon_payment, years_to_maturity, coupon_frequency):
    periods = years_to_maturity * coupon_frequency
    cash_flows = np.full(periods, coupon_payment)
    cash_flows[-1] += face_value  # 最后一期包含本金
    discount_factors = (1 + ytm / coupon_frequency) ** np.arange(1, periods + 1)
    return np.sum(cash_flows / discount_factors)

# 计算初始价格
initial_price = bond_price(ytm_initial, face_value, coupon_payment, years_to_maturity, coupon_frequency)

# 计算久期和凸性
def bond_duration_convexity(ytm, face_value, coupon_payment, years_to_maturity, coupon_frequency):
    periods = years_to_maturity * coupon_frequency
    cash_flows = np.full(periods, coupon_payment)
    cash_flows[-1] += face_value
    discount_factors = (1 + ytm / coupon_frequency) ** np.arange(1, periods + 1)
    discounted_cash_flows = cash_flows / discount_factors

    # 麦考利久期
    macaulay_duration = np.sum(discounted_cash_flows * np.arange(1, periods + 1)) / (initial_price * coupon_frequency)
    # 修正久期
    modified_duration = macaulay_duration / (1 + ytm / coupon_frequency)

    # 凸性
    convexity = np.sum(discounted_cash_flows * np.arange(1, periods + 1) * (np.arange(1, periods + 1) + 1)) / \
                (initial_price * (1 + ytm / coupon_frequency)**2 * coupon_frequency**2)

    return modified_duration, convexity

modified_duration, convexity = bond_duration_convexity(
    ytm_initial, face_value, coupon_payment, years_to_maturity, coupon_frequency
)

# 估算价格变化（使用久期和凸性近似）
price_change_approx = -modified_duration * yield_change + 0.5 * convexity * (yield_change)**2
price_drop_pct = price_change_approx * 100

# 精确计算新价格（验证）
new_ytm = ytm_initial + yield_change
new_price = bond_price(new_ytm, face_value, coupon_payment, years_to_maturity, coupon_frequency)
exact_price_drop_pct = (initial_price - new_price) / initial_price * 100

# 结果存储
result = {
    'price_drop_pct': price_drop_pct  # 使用久期-凸性近似结果
}

# 输出验证（可选，不影响结果）
print(f"初始价格: {initial_price:.4f}")
print(f"久期: {modified_duration:.4f}")
print(f"凸性: {convexity:.4f}")
print(f"近似跌幅: {price_drop_pct:.4f}%")
print(f"精确跌幅: {exact_price_drop_pct:.4f}%")
