import numpy as np
from scipy.optimize import newton

# 债券参数
face_value = 100
coupon_rate = 0.046
ytm_current = 0.053  # 当前收益率
years_to_maturity = 7
coupon_frequency = 2  # 半年付息一次
yield_change_bps = 80  # 收益率变化（基点）
yield_change = yield_change_bps / 10000  # 转换为小数

# 计算每期票息
coupon_payment = face_value * coupon_rate / coupon_frequency

# 定义债券定价函数
def bond_price(ytm, face_value, coupon_payment, periods):
    """计算债券价格"""
    cash_flows = np.array([coupon_payment] * periods)
    cash_flows[-1] += face_value  # 最后一期加上面值
    discount_factors = (1 + ytm / coupon_frequency) ** np.arange(1, periods + 1)
    return np.sum(cash_flows / discount_factors)

# 计算当前价格
periods = years_to_maturity * coupon_frequency
current_price = bond_price(ytm_current, face_value, coupon_payment, periods)

# 计算久期和凸性
def bond_duration_convexity(ytm, face_value, coupon_payment, periods):
    """计算麦考利久期和凸性"""
    cash_flows = np.array([coupon_payment] * periods)
    cash_flows[-1] += face_value
    time_periods = np.arange(1, periods + 1)
    discount_factors = (1 + ytm / coupon_frequency) ** time_periods
    pv_cash_flows = cash_flows / discount_factors

    # 麦考利久期
    macaulay_duration = np.sum(time_periods * pv_cash_flows) / np.sum(pv_cash_flows)
    modified_duration = macaulay_duration / (1 + ytm / coupon_frequency)

    # 凸性
    convexity = np.sum(time_periods * (time_periods + 1) * pv_cash_flows) / \
                (np.sum(pv_cash_flows) * (1 + ytm / coupon_frequency)**2)

    return modified_duration, convexity

modified_duration, convexity = bond_duration_convexity(
    ytm_current, face_value, coupon_payment, periods)

# 估算价格变化
price_change_pct = (-modified_duration * yield_change +
                    0.5 * convexity * yield_change**2) * 100

# 精确计算新价格
new_ytm = ytm_current + yield_change
new_price = bond_price(new_ytm, face_value, coupon_payment, periods)
exact_price_drop_pct = (current_price - new_price) / current_price * 100

# 结果存储
result = {
    'price_drop_pct': exact_price_drop_pct  # 使用精确计算的跌幅
}

# 输出验证（可选）
print(f"当前价格: {current_price:.4f}")
print(f"新价格: {new_price:.4f}")
print(f"久期估算跌幅: {price_change_pct:.4f}%")
print(f"精确跌幅: {exact_price_drop_pct:.4f}%")
print(f"结果字典: {result}")
