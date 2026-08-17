import numpy as np
from scipy.stats import norm

def black_scholes_call(S, K, T, r, sigma):
    """
    欧式看涨期权 Black-Scholes 定价公式
    """
    if sigma <= 0 or T <= 0:
        # 处理边界情况，避免除零
        return max(0.0, S - K * np.exp(-r * T))
    d1 = (np.log(S / K) + (r + 0.5 * sigma**2) * T) / (sigma * np.sqrt(T))
    d2 = d1 - sigma * np.sqrt(T)
    price = S * norm.cdf(d1) - K * np.exp(-r * T) * norm.cdf(d2)
    return price

def main():
    # 给定参数
    S = 103.7
    K = 97.5
    T = 0.58
    r = 0.043
    sigma0 = 0.276  # 隐含波动率 27.6%
    sigma1 = 0.286  # 上涨一个百分点 28.6%

    # 计算两个波动率下的期权价格
    price0 = black_scholes_call(S, K, T, r, sigma0)
    price1 = black_scholes_call(S, K, T, r, sigma1)

    # 价格变化（精确值，对看涨和看跌相同，因为vega相同）
    price_change = price1 - price0

    # 输出结果字典
    result = {'price_change': price_change}

    # 打印结果以便课堂投屏展示
    print(f"标的资产价格 S: {S}")
    print(f"行权价 K: {K}")
    print(f"剩余期限 T: {T} 年")
    print(f"无风险利率 r: {r*100:.2f}%")
    print(f"原隐含波动率: {sigma0*100:.2f}%")
    print(f"新隐含波动率: {sigma1*100:.2f}%")
    print(f"原期权价格: {price0:.6f}")
    print(f"新期权价格: {price1:.6f}")
    print(f"价格变化 (price_change): {price_change:.6f}")
    print(f"结果字典: {result}")

if __name__ == "__main__":
    main()
