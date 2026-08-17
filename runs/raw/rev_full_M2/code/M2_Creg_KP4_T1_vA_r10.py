import numpy as np
from scipy.stats import norm

def black_scholes_call(S, K, T, r, sigma):
    """
    计算欧式看涨期权价格、Delta 和 Vega (不分红)。

    参数
    ----------
    S : float
        标的现价
    K : float
        行权价
    T : float
        剩余期限，年
    r : float
        无风险利率，年化
    sigma : float
        隐含波动率，年化

    返回
    ----------
    dict : 包含 'call_price', 'call_delta', 'call_vega'
    """
    # 处理极端情况：T 极小时避免除零
    if T <= 1e-10:
        # 到期日，期权价格即为内在价值
        intrinsic = max(S - K, 0.0)
        delta = 1.0 if S > K else 0.0 if S < K else 0.5
        # Vega 理论上为 0，因为到期
        vega = 0.0
        return {
            'call_price': intrinsic,
            'call_delta': delta,
            'call_vega': vega
        }

    sigma_sqrt_T = sigma * np.sqrt(T)
    d1 = (np.log(S / K) + (r + 0.5 * sigma ** 2) * T) / sigma_sqrt_T
    d2 = d1 - sigma_sqrt_T

    call_price = S * norm.cdf(d1) - K * np.exp(-r * T) * norm.cdf(d2)
    call_delta = norm.cdf(d1)
    # Vega: 对波动率的一阶偏导 (波动率变动 1 单位，即 100% 波动的价格变化)
    call_vega = S * norm.pdf(d1) * np.sqrt(T)

    return {
        'call_price': call_price,
        'call_delta': call_delta,
        'call_vega': call_vega
    }

# 输入参数
S0 = 103.7          # 现价
K = 97.5            # 行权价
sigma = 0.276       # 年化隐含波动率 (27.6%)
r = 0.043           # 年化无风险利率 (4.3%)
T = 0.58            # 剩余期限 (年)

# 计算
result = black_scholes_call(S0, K, T, r, sigma)

# 输出结果
print("计算结果：")
for key, value in result.items():
    print(f"{key}: {value:.6f}")

# 脚本可直接运行，结果存储在 result 字典中
