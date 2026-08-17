import numpy as np
from scipy.stats import norm

# ---------- 给定参数 ----------
S = 103.7        # 标的资产价格
K = 97.5         # 执行价格
sigma = 0.276    # 年化波动率 (27.6%)
r = 0.043        # 无风险利率 (4.3%)
T = 0.58         # 剩余期限（年）

# ---------- 计算 d1, d2 ----------
d1 = (np.log(S / K) + (r + 0.5 * sigma ** 2) * T) / (sigma * np.sqrt(T))
d2 = d1 - sigma * np.sqrt(T)

# ---------- 计算期权价格与希腊字母 ----------
call_price = S * norm.cdf(d1) - K * np.exp(-r * T) * norm.cdf(d2)
call_delta = norm.cdf(d1)
call_vega = S * np.sqrt(T) * norm.pdf(d1)   # ∂C/∂σ，即波动率每变动 1 单位（例如 0.01）的期权价格变动

# ---------- 存入结果字典 ----------
result = {
    'call_price': call_price,
    'call_delta': call_delta,
    'call_vega': call_vega
}

# 直接打印字典供投屏查看
print(result)
