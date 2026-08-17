import numpy as np

def bond_price_duration_convexity(face=100.0, coupon_rate=0.046, years=7, ytm=0.053, freq=1):
    """
    计算债券价格、麦考利久期、修正久期和凸性。
    假设每年付息一次，使用离散复利。
    """
    # 现金流的时间点（年）
    t = np.arange(1, years + 1, dtype=float)
    # 每次的票息
    coupon = face * coupon_rate
    # 构造现金流，最后一年加上面值
    cashflows = np.full(years, coupon, dtype=float)
    cashflows[-1] += face

    # 折现因子 (1 + ytm)^(-t)
    disc = (1 + ytm) ** (-t)
    # 每笔现金流的现值
    pv = cashflows * disc
    price = np.sum(pv)

    # 麦考利久期 = sum(t * 权重), 权重 = pv / price
    weights = pv / price
    macaulay_duration = np.sum(t * weights)

    # 修正久期 = 麦考利久期 / (1 + ytm)，每年付息一次
    modified_duration = macaulay_duration / (1 + ytm)

    # 凸性 = [ Σ t(t+1)* PV(CF) ] / [ P * (1 + ytm)^2 ]
    convexity = np.sum(t * (t + 1) * pv) / (price * (1 + ytm) ** 2)

    return price, macaulay_duration, modified_duration, convexity

# 执行计算
price, mac_dur, mod_dur, conv = bond_price_duration_convexity()

# 按要求把结果存入 result 字典
result = {
    'price': price,
    'macaulay_duration_years': mac_dur,
    'modified_duration_years': mod_dur,
    'convexity': conv
}

# 输出以便课堂投屏观察
print(result)
