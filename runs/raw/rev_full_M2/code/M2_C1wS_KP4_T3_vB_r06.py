import numpy as np
from scipy.stats import norm

def black_scholes_vega(S, K, T, r, sigma):
    """
    计算欧式看涨/看跌期权的 Vega（波动率每变动1单位，即100%绝对变动，引起的期权价格变动）。
    """
    if T <= 0:
        return 0.0
    d1 = (np.log(S / K) + (r + 0.5 * sigma**2) * T) / (sigma * np.sqrt(T))
    vega = S * norm.pdf(d1) * np.sqrt(T)
    return vega

def main():
    # 给定参数
    S = 103.7          # 标的资产价格
    K = 97.5           # 执行价格
    sigma = 0.276      # 初始隐含波动率 (27.6%)
    r = 0.043          # 无风险利率 (4.3%)
    T = 0.58           # 剩余到期时间（年）

    # 计算 Vega（波动率绝对值变动1单位的价格变动）
    vega = black_scholes_vega(S, K, T, r, sigma)

    # 波动率上涨1个百分点，即 sigma 增加 0.01
    delta_sigma = 0.01
    price_change = vega * delta_sigma

    # 存放结果
    result = {
        'price_change': price_change
    }

    # 可选：输出到控制台以便课堂查看（不影响最终变量）
    print(f"Vega: {vega:.6f}")
    print(f"波动率上涨1个百分点带来的期权价格变化: {price_change:.6f}")
    print(f"Result dictionary: {result}")

    # 按要求，result 变量已经存在，可直接被教师代码读取
    return result

if __name__ == "__main__":
    main()
