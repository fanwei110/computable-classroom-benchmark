import math

def black_scholes_call(S, K, T, r, sigma):
    """计算欧式看涨期权价格、Delta、Vega（无分红）"""
    d1 = (math.log(S / K) + (r + 0.5 * sigma**2) * T) / (sigma * math.sqrt(T))
    d2 = d1 - sigma * math.sqrt(T)
    # 标准正态累积分布函数近似
    def norm_cdf(x):
        # Abramowitz and Stegun 近似
        a1, a2, a3, a4, a5 = 0.31938153, -0.35656378, 1.78147794, -1.82125598, 1.33027443
        k = 1.0 / (1.0 + 0.2316419 * abs(x))
        n = (1.0 / math.sqrt(2.0 * math.pi)) * math.exp(-0.5 * x * x)
        cdf_approx = 1.0 - n * (a1 * k + a2 * k**2 + a3 * k**3 + a4 * k**4 + a5 * k**5)
        if x >= 0:
            return cdf_approx
        else:
            return 1.0 - cdf_approx

    Nd1 = norm_cdf(d1)
    Nd2 = norm_cdf(d2)
    call_price = S * Nd1 - K * math.exp(-r * T) * Nd2
    call_delta = Nd1
    # Vega: ∂C/∂σ
    n_d1 = (1.0 / math.sqrt(2.0 * math.pi)) * math.exp(-0.5 * d1**2)
    call_vega = S * n_d1 * math.sqrt(T)
    return call_price, call_delta, call_vega

# 参数
S = 103.7
K = 97.5
T = 0.58
r = 0.043
sigma = 0.276

price, delta, vega = black_scholes_call(S, K, T, r, sigma)

result = {
    'call_price': round(price, 4),
    'call_delta': round(delta, 4),
    'call_vega': round(vega, 4)
}

print(result)
