import numpy as np
from scipy.stats import norm

# 给定参数
S0 = 103.7          # 现价
K = 97.5            # 行权价
sigma = 0.276       # 隐含波动率 (27.6%)
r = 0.043           # 无风险利率 (4.3%)
T = 0.58            # 剩余期限 (年)

# 计算 d1 和 d2
d1 = (np.log(S0/K) + (r + sigma**2/2)*T) / (sigma*np.sqrt(T))
d2 = d1 - sigma*np.sqrt(T)

# 计算期权价格
call_price = S0*norm.cdf(d1) - K*np.exp(-r*T)*norm.cdf(d2)

# 计算 delta
call_delta = norm.cdf(d1)

# 计算 vega (dC/dσ，以小数表示)
call_vega = S0*norm.pdf(d1)*np.sqrt(T)

# 输出字典
result = {
    'call_price': call_price,
    'call_delta': call_delta,
    'call_vega': call_vega
}

# 打印结果
print("Black-Scholes 欧式看涨期权定价结果：")
print(f"期权价格 (call_price): {call_price:.6f}")
print(f"Delta (call_delta):     {call_delta:.6f}")
print(f"Vega (call_vega):       {call_vega:.6f}")

# 返回 result 供外部调用
result
