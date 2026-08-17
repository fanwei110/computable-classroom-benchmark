import numpy as np
from scipy.stats import norm

# ==================== 参数设定 ====================
S = 103.7      # 股票现价
K = 97.5       # 行权价
sigma = 0.276  # 隐含波动率（年化）
r = 0.043      # 无风险利率（年化）
T = 0.58       # 剩余期限（年）
q = 0.0        # 股息率（题目指明不分红）

# ==================== 步骤 1：计算 d1 与 d2 ====================
d1 = (np.log(S / K) + (r - q + 0.5 * sigma**2) * T) / (sigma * np.sqrt(T))
d2 = d1 - sigma * np.sqrt(T)

# ==================== 步骤 2：计算期权价格与 delta ====================
call_price = S * np.exp(-q * T) * norm.cdf(d1) - K * np.exp(-r * T) * norm.cdf(d2)
call_delta = np.exp(-q * T) * norm.cdf(d1)

# ==================== 步骤 3：计算 vega ====================
# 标准数学定义：vega 是期权价格对波动率的一阶导数，此处为变动 1 单位 sigma 的绝对敏感度
call_vega = S * np.exp(-q * T) * np.sqrt(T) * norm.pdf(d1)

# ==================== 步骤 4：填充 result ====================
result = {
    'call_price': call_price,
    'call_delta': call_delta,
    'call_vega': call_vega
}

# ==================== 课堂投屏输出 ====================
print("=" * 40)
print("Black-Scholes 欧式看涨期权计算结果")
print("=" * 40)
print(f"d1         = {d1:.6f}")
print(f"d2         = {d2:.6f}")
print(f"call_price = {call_price:.4f}")
print(f"call_delta = {call_delta:.4f}")
print(f"call_vega  = {call_vega:.4f}")
print("=" * 40)
print("Result Dictionary:")
print(result)
