import numpy as np

def calculate_bond_metrics():
    FV = 100
    coupon_rate = 0.046
    N = 7
    YTM = 0.053

    # 计算每期现金流
    coupon = FV * coupon_rate
    cash_flows = np.array([coupon] * N)
    cash_flows[-1] += FV  # 最后一期加上面值

    # 计算价格
    discount_factors = (1 + YTM) ** np.arange(1, N + 1)
    price = np.sum(cash_flows / discount_factors)

    # 计算麦考利久期
    weighted_cash_flows = cash_flows * np.arange(1, N + 1)
    macaulay_duration = np.sum(weighted_cash_flows / discount_factors) / price

    # 计算修正久期
    modified_duration = macaulay_duration / (1 + YTM)

    # 计算凸性
    convexity_numerator = cash_flows * np.arange(1, N + 1) * (np.arange(1, N + 1) + 1)
    convexity = np.sum(convexity_numerator / ((1 + YTM) ** (np.arange(1, N + 1) + 2))) / price

    result = {
        'price': round(price, 4),
        'macaulay_duration_years': round(macaulay_duration, 4),
        'modified_duration_years': round(modified_duration, 4),
        'convexity': round(convexity, 4)
    }
    return result

result = calculate_bond_metrics()
print(result)
