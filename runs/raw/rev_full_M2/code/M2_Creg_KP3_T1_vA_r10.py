import numpy as np

def compute_bond_metrics(face=100, coupon_rate=0.046, maturity=7, ytm=0.053):
    """
    计算每年付息一次、到期一次还本的债券的价格、麦考利久期、修正久期和凸性。
    """
    # 现金流时间点 1,2,...,maturity
    t = np.arange(1, maturity + 1, dtype=float)
    # 票息
    coupon = face * coupon_rate
    # 现金流：每期票息，最后一期加上面值
    cash_flows = np.full(maturity, coupon)
    cash_flows[-1] += face

    # 折现因子
    discount_factors = (1 + ytm) ** (-t)
    pv = cash_flows * discount_factors

    # 价格
    price = np.sum(pv)

    # 麦考利久期：以时间为权重的加权平均回款期
    macaulay_duration = np.sum(t * pv) / price

    # 修正久期
    modified_duration = macaulay_duration / (1 + ytm)

    # 凸性：使用公式 convexity = (1/(P*(1+y)^2)) * sum( t*(t+1)*PV )
    convexity = np.sum(t * (t + 1) * pv) / (price * (1 + ytm) ** 2)

    return {
        'price': round(price, 10),
        'macaulay_duration_years': round(macaulay_duration, 10),
        'modified_duration_years': round(modified_duration, 10),
        'convexity': round(convexity, 10)
    }

if __name__ == "__main__":
    result = compute_bond_metrics()
    print(result)
