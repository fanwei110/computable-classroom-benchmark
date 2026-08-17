import numpy as np
from scipy.optimize import newton

def calculate_bond_metrics(face_value, coupon_rate, years_to_maturity, ytm):
    """
    计算债券的价格、麦考利久期、修正久期和凸性。

    参数:
    - face_value: 债券面值
    - coupon_rate: 年票息率（小数形式）
    - years_to_maturity: 剩余期限（年）
    - ytm: 到期收益率（小数形式）

    返回:
    - result: 包含价格、麦考利久期、修正久期和凸性的字典
    """
    # 计算每期票息（假设每年付息一次）
    coupon_payment = face_value * coupon_rate
    periods = int(years_to_maturity)  # 期数（年）
    ytm_period = ytm  # 年化收益率

    # 计算债券价格
    price = sum([coupon_payment / (1 + ytm_period) ** t for t in range(1, periods + 1)]) + \
            face_value / (1 + ytm_period) ** periods

    # 计算麦考利久期
    weighted_cash_flows = [(t * coupon_payment) / (1 + ytm_period) ** t for t in range(1, periods + 1)]
    weighted_cash_flows.append((periods * face_value) / (1 + ytm_period) ** periods)
    macaulay_duration = sum(weighted_cash_flows) / price

    # 计算修正久期
    modified_duration = macaulay_duration / (1 + ytm_period)

    # 计算凸性
    convexity_numerator = sum([(t * (t + 1) * coupon_payment) / (1 + ytm_period) ** (t + 2) for t in range(1, periods + 1)]) + \
                          (periods * (periods + 1) * face_value) / (1 + ytm_period) ** (periods + 2)
    convexity = convexity_numerator / price

    # 结果存入字典
    result = {
        'price': price,
        'macaulay_duration_years': macaulay_duration,
        'modified_duration_years': modified_duration,
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

# 输出结果（可选，用于验证）
print("债券价格:", result['price'])
print("麦考利久期（年）:", result['macaulay_duration_years'])
print("修正久期（年）:", result['modified_duration_years'])
print("凸性:", result['convexity'])
