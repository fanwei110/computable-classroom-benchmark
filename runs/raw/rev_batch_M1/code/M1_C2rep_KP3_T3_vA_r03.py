import numpy as np
from scipy.optimize import newton

# 债券参数
face_value = 100
coupon_rate = 0.046
ytm_current = 0.053  # 当前收益率
years_to_maturity = 7
coupon_frequency = 2  # 半年付息一次
ytm_increase_bps = 80  # 收益率上升基点数

# 计算相关参数
periods = years_to_maturity * coupon_frequency
coupon_payment = face_value * coupon_rate / coupon_frequency
ytm_period = ytm_current / coupon_frequency
ytm_new = ytm_current + ytm_increase_bps / 10000  # 转换为小数

# 定义债券定价函数
def bond_price(ytm, periods, coupon, face_value):
    """计算债券价格"""
    ytm_period = ytm / coupon_frequency
    cash_flows = np.full(periods, coupon)
    cash_flows[-1] += face_value  # 最后一期加上面值
    price = np.sum(cash_flows / (1 + ytm_period) ** np.arange(1, periods + 1))
    return price

# 计算当前价格
price_current = bond_price(ytm_current, periods, coupon_payment, face_value)

# 计算久期和凸性
def bond_duration_convexity(ytm, periods, coupon, face_value):
    """计算麦考利久期和凸性"""
    ytm_period = ytm / coupon_frequency
    cash_flows = np.full(periods, coupon)
    cash_flows[-1] += face_value

    # 计算久期
    discounted_cash_flows = cash_flows / (1 + ytm_period) ** np.arange(1, periods + 1)
    macaulay_duration = np.sum(np.arange(1, periods + 1) * discounted_cash_flows) / price_current
    modified_duration = macaulay_duration / (1 + ytm_period)

    # 计算凸性
    convexity = np.sum((np.arange(1, periods + 1) * (np.arange(1, periods + 1) + 1)) *
                       discounted_cash_flows) / (price_current * (1 + ytm_period)**2)

    return modified_duration, convexity

modified_duration, convexity = bond_duration_convexity(ytm_current, periods, coupon_payment, face_value)

# 估算价格变化
price_drop_pct = -modified_duration * (ytm_increase_bps / 100) + 0.5 * convexity * (ytm_increase_bps / 100)**2

# 精确计算新价格（用于验证）
price_new = bond_price(ytm_new, periods, coupon_payment, face_value)
price_drop_pct_exact = (price_new - price_current) / price_current * 100

# 结果存储
result = {
    'price_drop_pct': price_drop_pct  # 使用久期和凸性估算的跌幅百分比
}

# 输出验证信息（可选，不影响结果）
print(f"当前价格: {price_current:.4f}")
print(f"久期估算跌幅: {price_drop_pct:.4f}%")
print(f"精确计算跌幅: {price_drop_pct_exact:.4f}%")
