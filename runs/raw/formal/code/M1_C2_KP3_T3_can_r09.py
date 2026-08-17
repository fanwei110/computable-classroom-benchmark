import numpy as np
from scipy.optimize import newton

# 债券参数
face_value = 100
coupon_rate = 0.046
ytm_current = 0.053  # 当前收益率
maturity_years = 7
yield_change_bps = 80  # 收益率变化（基点）
yield_change = yield_change_bps / 10000  # 转换为小数

# 计算当前价格
def bond_price(ytm, face_value, coupon_rate, maturity_years):
    coupon = face_value * coupon_rate
    periods = maturity_years
    cash_flows = np.array([coupon] * periods + [face_value + coupon])
    discount_factors = np.array([(1 + ytm) ** (i + 1) for i in range(periods)])
    price = np.sum(cash_flows / discount_factors)
    return price

current_price = bond_price(ytm_current, face_value, coupon_rate, maturity_years)

# 计算久期和凸性
def bond_duration_convexity(ytm, face_value, coupon_rate, maturity_years):
    coupon = face_value * coupon_rate
    periods = maturity_years
    cash_flows = np.array([coupon] * periods + [face_value + coupon])

    # 计算久期
    discount_factors = np.array([(1 + ytm) ** (i + 1) for i in range(periods)])
    present_values = cash_flows / discount_factors
    weights = present_values / np.sum(present_values)
    time_periods = np.arange(1, periods + 1)
    duration = np.sum(weights * time_periods)

    # 计算修正久期
    modified_duration = duration / (1 + ytm)

    # 计算凸性
    convexity_weights = weights * time_periods * (time_periods + 1) / (1 + ytm) ** 2
    convexity = np.sum(convexity_weights)

    return modified_duration, convexity

modified_duration, convexity = bond_duration_convexity(
    ytm_current, face_value, coupon_rate, maturity_years
)

# 估算价格变化
price_drop_estimate = -modified_duration * yield_change + 0.5 * convexity * (yield_change ** 2)
price_drop_pct = price_drop_estimate * 100

# 计算实际新价格（验证）
new_ytm = ytm_current + yield_change
new_price = bond_price(new_ytm, face_value, coupon_rate, maturity_years)
actual_price_drop_pct = ((current_price - new_price) / current_price) * 100

# 存储结果
result = {
    'price_drop_pct': price_drop_pct  # 使用久期和凸性的估算值
}

# 输出验证信息（可选，不影响result）
print(f"当前价格: {current_price:.4f}")
print(f"久期估算跌幅: {price_drop_pct:.4f}%")
print(f"实际跌幅: {actual_price_drop_pct:.4f}%")
