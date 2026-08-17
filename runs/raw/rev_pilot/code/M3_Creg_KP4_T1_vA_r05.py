import numpy as np
from scipy.stats import norm

# --- 输入参数 ---
S = 103.7        # 现价 (Spot Price)
K = 97.5         # 行权价 (Strike Price)
sigma = 0.276    # 隐含波动率 (Implied Volatility, 27.6% 年化)
r = 0.043        # 无风险利率 (Risk-free Rate, 4.3% 年化)
T = 0.58         # 剩余期限 (Time to Maturity, 以年为单位)

# --- Black-Scholes 模型计算 ---
# 计算 d1 和 d2
d1 = (np.log(S / K) + (r + 0.5 * sigma**2) * T) / (sigma * np.sqrt(T))
d2 = d1 - sigma * np.sqrt(T)

# 计算欧式看涨期权价格 (Call Price)
call_price = S * norm.cdf(d1) - K * np.exp(-r * T) * norm.cdf(d2)

# 计算看涨期权 Delta
call_delta = norm.cdf(d1)

# 计算看涨期权 Vega (对波动率的敏感度，通常定义为绝对变化量，即波动率变化1个单位对应的期权价格变化)
# 若需表示为波动率变化1%时的价格变化，可除以100。此处按数学定义输出绝对敏感度。
call_vega = S * np.sqrt(T) * norm.pdf(d1)

# --- 输出契约存入字典 ---
result = {
    'call_price': call_price,
    'call_delta': call_delta,
    'call_vega': call_vega
}

# 打印结果以供验证
print(result)
