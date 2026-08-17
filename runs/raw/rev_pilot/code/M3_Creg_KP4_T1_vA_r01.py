import numpy as np
from scipy.stats import norm

# --- 输入参数 ---
S = 103.7       # 标的资产现价
K = 97.5        # 行权价
sigma = 0.276   # 隐含波动率 (年化，27.6%)
r = 0.043       # 无风险利率 (年化，4.3%)
T = 0.58        # 剩余期限 (年)

# --- Black-Scholes 公式计算 ---
# 计算 d1 和 d2
d1 = (np.log(S / K) + (r + 0.5 * sigma**2) * T) / (sigma * np.sqrt(T))
d2 = d1 - sigma * np.sqrt(T)

# 计算欧式看涨期权价格
call_price = S * norm.cdf(d1) - K * np.exp(-r * T) * norm.cdf(d2)

# 计算 Delta (不分红股票的看涨期权 Delta = N(d1))
call_delta = norm.cdf(d1)

# 计算 Vega (数学导数 dC/d_sigma，表示波动率变化1单位(即100%)时期权价格的变化量)
call_vega = S * np.sqrt(T) * norm.pdf(d1)

# --- 封装输出 ---
result = {
    'call_price': call_price,
    'call_delta': call_delta,
    'call_vega': call_vega
}

# 打印结果以供验证
print(result)
