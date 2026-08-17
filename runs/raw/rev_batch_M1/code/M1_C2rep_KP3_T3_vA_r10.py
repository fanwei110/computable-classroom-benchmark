import numpy as np
from scipy.optimize import newton

# 债券参数
face_value = 100
coupon_rate = 0.046
ytm_current = 0.053  # 当前收益率
maturity_years = 7
coupon_frequency = 2  # 每年付息次数（半年付息）
yield_change_bps = 80  # 收益率变化（基点）
yield_change = yield_change_bps / 10000  # 转换为小数

# 计算当前价格
def bond_price(ytm, face_value, coupon_rate, maturity_years, coupon_frequency):
    periods = maturity_years * coupon_frequency
    coupon = face_value * coupon_rate / coupon_frequency
    discount_rates = (1 + ytm / coupon_frequency) ** np.arange(1, periods + 1)
    cash_flows = np.full(periods, coupon)
    cash_flows[-1] += face_value  # 最后一期加上面值
    price = np.sum(cash_flows / discount_rates)
    return price

price_current = bond_price(ytm_current, face_value, coupon_rate, maturity_years, coupon_frequency)

# 计算久期和凸性
def bond_duration_convexity(ytm, face_value, coupon_rate, maturity_years, coupon_frequency):
    periods = maturity_years * coupon_frequency
    coupon = face_value * coupon_rate / coupon_frequency
    cash_flows = np.full(periods, coupon)
    cash_flows[-1] += face_value

    # 计算贴现因子
    t = np.arange(1, periods + 1)
    discount_rates = (1 + ytm / coupon_frequency) ** t
    discounted_cash_flows = cash_flows / discount_rates

    # 久期（Macaulay Duration）
    macaulay_duration = np.sum(t * discounted_cash_flows) / np.sum(discounted_cash_flows)
    modified_duration = macaulay_duration / (1 + ytm / coupon_frequency)

    # 凸性
    convexity = np.sum(t * (t + 1) * discounted_cash_flows) / (np.sum(discounted_cash_flows) * (1 + ytm / coupon_frequency)**2)

    return modified_duration, convexity

modified_duration, convexity = bond_duration_convexity(
    ytm_current, face_value, coupon_rate, maturity_years, coupon_frequency
)

# 估算价格变化（使用久期和凸性）
price_drop_estimate = -modified_duration * yield_change + 0.5 * convexity * (yield_change)**2
price_drop_pct = price_drop_estimate * 100

# 计算实际价格变化（验证）
ytm_new = ytm_current + yield_change
price_new = bond_price(ytm_new, face_value, coupon_rate, maturity_years, coupon_frequency)
actual_price_drop_pct = (price_new - price_current) / price_current * 100

# 结果存储
result = {
    'price_drop_pct': price_drop_pct  # 使用久期和凸性的估算值
}

# 输出结果（可选，便于调试）
print(f"当前价格: {price_current:.4f}")
print(f"久期: {modified_duration:.4f}")
print(f"凸性: {convexity:.4f}")
print(f"估算跌幅: {price_drop_pct:.4f}%")
print(f"实际跌幅: {actual_price_drop_pct:.4f}%")
