import numpy as np
from scipy.stats import norm

def black_scholes_greeks(S, K, T, r, sigma, option_type='call'):
    """
    计算欧式期权的BS价格、Delta、Vega (不分红)
    option_type: 'call' 或 'put'
    返回: price, delta, vega
    vega: 价格对波动率(sigma)的偏导数，即波动率每变动1单位(如从0.20到0.21)的价格变化
    """
    if T <= 0:
        # 到期时处理
        if option_type == 'call':
            price = max(S - K, 0)
            delta = 1.0 if S > K else 0.0
        else:
            price = max(K - S, 0)
            delta = -1.0 if S < K else 0.0
        vega = 0.0
        return price, delta, vega

    d1 = (np.log(S / K) + (r + 0.5 * sigma**2) * T) / (sigma * np.sqrt(T))
    d2 = d1 - sigma * np.sqrt(T)

    if option_type == 'call':
        price = S * norm.cdf(d1) - K * np.exp(-r * T) * norm.cdf(d2)
        delta = norm.cdf(d1)
    elif option_type == 'put':
        price = K * np.exp(-r * T) * norm.cdf(-d2) - S * norm.cdf(-d1)
        delta = -norm.cdf(-d1)
    else:
        raise ValueError("option_type must be 'call' or 'put'")

    # vega: S * sqrt(T) * N'(d1)   (N' 是标准正态密度函数)
    vega = S * np.sqrt(T) * norm.pdf(d1)

    return price, delta, vega


if __name__ == "__main__":
    # 给定参数
    S = 103.7        # 标的资产价格
    K = 97.5         # 行权价
    sigma = 0.276    # 波动率
    r = 0.043        # 无风险利率
    T = 0.58         # 剩余到期时间(年)

    # 计算
    call_price, call_delta, call_vega = black_scholes_greeks(S, K, T, r, sigma, option_type='call')

    # 按契约存入字典
    result = {
        'call_price': call_price,
        'call_delta': call_delta,
        'call_vega': call_vega
    }

    print("计算结果：")
    for k, v in result.items():
        print(f"{k}: {v:.6f}")
