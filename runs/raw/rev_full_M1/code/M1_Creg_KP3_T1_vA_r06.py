import numpy as np
from scipy.optimize import newton

def calculate_bond_metrics(face_value, coupon_rate, years_to_maturity, ytm):
    """
    计算债券的价格、麦考利久期、修正久期和凸性。

    参数:
    - face_value: 债券面值
    - coupon_rate: 年票息率 (小数形式)
    - years_to_maturity: 剩余期限 (年)
    - ytm: 到期收益率 (小数形式)

    返回:
    - result: 包含价格、麦考利久期、修正久期和凸性的字典
    """
    # 计算每期票息 (假设每年付息一次)
    coupon_payment = face_value * coupon_rate
    periods = int(years_to_maturity)  # 期数
    ytm_period = ytm  # 年化收益率

    # 计算债券价格
    price = 0.0
    for t in range(1, periods + 1):
        price += coupon_payment / ((1 + ytm_period) ** t)
    price += face_value / ((1 + ytm_period) ** periods)

    # 计算麦考利久期
    macaulay_duration = 0.0
    for t in range(1, periods + 1):
        cash_flow = coupon_payment
        if t == periods:
            cash_flow += face_value  # 最后一期包含本金
        discounted_cash_flow = cash_flow / ((1 + ytm_period) ** t)
        macaulay_duration += t * discounted_cash_flow
    macaulay_duration /= price
    macaulay_duration_years = macaulay_duration  # 因为每年付息一次，久期单位为年

    # 计算修正久期
    modified_duration_years = macaulay_duration_years / (1 + ytm_period)

    # 计算凸性
    convexity = 0.0
    for t in range(1, periods + 1):
        cash_flow = coupon_payment
        if t == periods:
            cash_flow += face_value
        discounted_cash_flow = cash_flow / ((1 + ytm_period) ** t)
        convexity += t * (t + 1) * discounted_cash_flow
    convexity /= (price * (1 + ytm_period) ** 2)

    # 存储结果
    result = {
        'price': price,
        'macaulay_duration_years': macaulay_duration_years,
        'modified_duration_years': modified_duration_years,
        'convexity': convexity
    }

    return result

# 债券参数
face_value = 100
coupon_rate = 0.046  # 4.6%
years_to_maturity = 7
ytm = 0.053  # 5.3%

# 计算结果
result = calculate_bond_metrics(face_value, coupon_rate, years_to_maturity, ytm)

# 输出结果 (可选，用于验证)
print("债券价格:", result['price'])
print("麦考利久期 (年):", result['macaulay_duration_years'])
print("修正久期 (年):", result['modified_duration_years'])
print("凸性:", result['convexity'])
