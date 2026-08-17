import numpy as np

def bond_price_macaulay_convexity(face, coupon_rate, maturity, ytm):
    """
    计算债券价格、麦考利久期、修正久期与凸性。

    参数：
        face: 面值
        coupon_rate: 票息率（小数）
        maturity: 剩余年限（年）
        ytm: 到期收益率（年复利，小数）

    返回：价格、麦考利久期（年）、修正久期（年）、凸性（年平方）
    """
    # 现金流生成
    t = np.arange(1, maturity + 1)                # 年份 1..T
    cf = np.full(maturity, coupon_rate * face)    # 票息
    cf[-1] += face                                # 最后一年加上面值

    # 贴现因子与现值
    df = (1 + ytm) ** (-t)
    pv = cf * df
    price = np.sum(pv)

    # 权重
    w = pv / price

    # 麦考利久期
    macaulay_dur = np.sum(t * w)

    # 修正久期
    modified_dur = macaulay_dur / (1 + ytm)

    # 凸性
    # Σ[ t*(t+1)*CF_t / (1+y)^(t+2) ] / P
    convex_contrib = t * (t + 1) * cf / (1 + ytm) ** (t + 2)
    convexity = np.sum(convex_contrib) / price

    return price, macaulay_dur, modified_dur, convexity


# 债券参数
face_value = 100.0
coupon_rate = 0.046    # 4.6%
maturity = 7           # 7年
ytm = 0.053            # 5.3%

# 计算
price, mac_dur, mod_dur, conv = bond_price_macaulay_convexity(
    face=face_value,
    coupon_rate=coupon_rate,
    maturity=maturity,
    ytm=ytm
)

# 结果字典
result = {
    "price": price,
    "macaulay_duration_years": mac_dur,
    "modified_duration_years": mod_dur,
    "convexity": conv
}

# 输出结果供投屏显示
for key, value in result.items():
    print(f"{key}: {value:.6f}")
