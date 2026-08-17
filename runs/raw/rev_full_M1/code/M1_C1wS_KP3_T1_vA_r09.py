import numpy as np
from typing import Dict

def calculate_bond_metrics(
    face_value: float = 100.0,
    coupon_rate: float = 0.046,
    years_to_maturity: int = 7,
    yield_to_maturity: float = 0.053,
    periods_per_year: int = 1
) -> Dict[str, float]:
    """
    计算债券的价格、Macaulay 久期、修正久期和凸性。

    参数:
        face_value: 债券面值
        coupon_rate: 票面利率（年化）
        years_to_maturity: 剩余期限（年）
        yield_to_maturity: 到期收益率（年化）
        periods_per_year: 每年付息次数（默认1，即年付息）

    返回:
        包含价格、Macaulay 久期、修正久期和凸性的字典
    """
    # 计算每期现金流
    coupon_payment = face_value * coupon_rate / periods_per_year
    total_periods = years_to_maturity * periods_per_year
    cash_flows = np.full(total_periods, coupon_payment)
    cash_flows[-1] += face_value  # 最后一期包含本金

    # 计算每期贴现率
    periodic_ytm = yield_to_maturity / periods_per_year

    # 计算价格（现金流贴现之和）
    periods = np.arange(1, total_periods + 1)
    discount_factors = (1 + periodic_ytm) ** -periods
    price = np.sum(cash_flows * discount_factors)

    # 计算 Macaulay 久期（加权平均回收期）
    weighted_cash_flows = cash_flows * periods * discount_factors
    macaulay_duration_periods = np.sum(weighted_cash_flows) / price
    macaulay_duration_years = macaulay_duration_periods / periods_per_year

    # 计算修正久期
    modified_duration_years = macaulay_duration_years / (1 + yield_to_maturity / periods_per_year)

    # 计算凸性
    convexity_periods = np.sum(cash_flows * periods * (periods + 1) * discount_factors) / (1 + periodic_ytm) ** 2
    convexity = convexity_periods / (price * periods_per_year ** 2)

    # 返回结果
    result = {
        'price': price,
        'macaulay_duration_years': macaulay_duration_years,
        'modified_duration_years': modified_duration_years,
        'convexity': convexity
    }
    return result

# 计算并输出结果
result = calculate_bond_metrics()
print(result)
