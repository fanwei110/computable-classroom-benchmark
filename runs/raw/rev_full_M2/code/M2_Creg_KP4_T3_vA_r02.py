import numpy as np
from scipy.stats import norm

def main():
    # ---------- 给定参数 ----------
    S = 103.7          # 标的现价
    K = 97.5           # 行权价
    sigma = 0.276      # 当前隐含波动率 (27.6%)
    r = 0.043          # 无风险利率 (4.3%)
    T = 0.58           # 剩余到期时间 (年)
    delta_sigma = 0.01 # 隐含波动率上升 1 个百分点

    # ---------- 计算 d1 ----------
    d1 = (np.log(S / K) + (r + 0.5 * sigma**2) * T) / (sigma * np.sqrt(T))

    # ---------- 计算 Vega ----------
    # Vega = S * N'(d1) * sqrt(T)
    vega = S * norm.pdf(d1) * np.sqrt(T)

    # 波动率上升 delta_sigma 对应的期权价格变化
    price_change = vega * delta_sigma

    # ---------- 输出结果 ----------
    result = {'price_change': price_change}
    print(result)

if __name__ == "__main__":
    main()
