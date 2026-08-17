import json

# 假设我们基于之前的对话上下文：一个平价(ATM)期权，标的资产价格为100，行权价为100，剩余期限为30天(约0.082年)，无风险利率为0
# 初始隐含波动率假设为20%，现在要计算隐含波动率上涨1个点（从20%到21%）导致的价格变动。
# 由于没有之前的具体参数，我需要用一个标准的模型来演示这个过程。通常使用Black-Scholes模型。

from math import exp, log, sqrt, pi
from scipy.stats import norm  # 如果允许使用外部库，通常这样计算。这里为了完整性，我会自己实现一个简化的CDF。

def norm_cdf(x):
    """标准正态分布的累积分布函数，避免依赖scipy"""
    # 使用误差函数近似
    return (1.0 + erf(x / sqrt(2.0))) / 2.0

def erf(x):
    # 近似误差函数，使用Abramowitz and Stegun approximation
    a1 =  0.254829592
    a2 = -0.284496736
    a3 =  1.421413741
    a4 = -1.453152027
    a5 =  1.061405429
    p  =  0.3275911

    sign = 1 if x >= 0 else -1
    x = abs(x)
    t = 1.0 / (1.0 + p * x)
    y = 1.0 - (((((a5 * t + a4) * t) + a3) * t + a2) * t + a1) * t * exp(-x * x)
    return sign * y

def black_scholes_call(S, K, T, r, sigma):
    if T == 0:
        return max(S - K, 0)
    d1 = (log(S/K) + (r + sigma**2 / 2) * T) / (sigma * sqrt(T))
    d2 = d1 - sigma * sqrt(T)
    return S * norm_cdf(d1) - K * exp(-r * T) * norm_cdf(d2)

# 设定参数：根据时间0.082年(30/365)，初始sigma=0.20，其他如S=100, K=100, r=0
S = 100.0
K = 100.0
r = 0.0
T = 30.0 / 365.0  # 大约0.08219178年
sigma_initial = 0.20
sigma_new = sigma_initial + 0.01  # 涨1个点，即1%

price_initial = black_scholes_call(S, K, T, r, sigma_initial)
price_new = black_scholes_call(S, K, T, r, sigma_new)
price_change = price_new - price_initial

# 将结果存入字典
result = {
    'price_change': price_change
}

# 打印结果（可选，仅用于展示）
print(json.dumps(result, indent=2))
