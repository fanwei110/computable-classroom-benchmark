import numpy as np
from scipy.stats import norm

# 给定参数
S = 103.7          # 标的现价
K = 97.5           # 行权价
sigma = 0.276      # 年化隐含波动率
r = 0.043          # 年化无风险利率
T = 0.58           # 剩余期限（年）

# 1. 计算 d1 和 d2
d1 = (np.log(S / K) + (r + 0.5 * sigma**2) * T) / (sigma * np.sqrt(T))
d2 = d1 - sigma * np.sqrt(T)

# 2. 计算期权价格和 delta
call_price = S * norm.cdf(d1) - K * np.exp(-r * T) * norm.cdf(d2)
call_delta = norm.cdf(d1)

# 3. 计算 vega（单位：波动率每变动 1 的期权价格变化）
call_vega = S * norm.pdf(d1) * np.sqrt(T)

# 4. 存入结果字典
result = {
    'call_price': call_price,
    'call_delta': call_delta,
    'call_vega': call_vega
}

# 输出以便课堂投屏查看
if __name__ == "__main__":
    print(f"d1  = {d1:.6f}")
    print(f"d2  = {d2:.6f}")
    print(f"看涨期权价格 = {call_price:.4f}")
    print(f"Delta        = {call_delta:.4f}")
    print(f"Vega         = {call_vega:.4f}")
    print("\nresult 字典内容：")
    for k, v in result.items():
        print(f"  {k}: {v}")
