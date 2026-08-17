import numpy as np
from scipy.stats import norm

# ==================== 参数设定 ====================
S = 103.7       # 股票现价
K = 97.5        # 行权价
sigma = 0.276   # 隐含波动率（年化，27.6%）
r = 0.043       # 无风险利率（年化，4.3%）
T = 0.58        # 剩余期限（年）

# ==================== 1. 计算 d1 与 d2 ====================
d1 = (np.log(S / K) + (r + 0.5 * sigma**2) * T) / (sigma * np.sqrt(T))
d2 = d1 - sigma * np.sqrt(T)

# ==================== 2. 计算期权价格与 delta ====================
# 欧式看涨期权价格 (Black-Scholes 闭式解)
call_price = S * norm.cdf(d1) - K * np.exp(-r * T) * norm.cdf(d2)

# 欧式看涨期权 Delta (不支付红利股票)
call_delta = norm.cdf(d1)

# ==================== 3. 计算 vega ====================
# 假设说明：Vega 定义为期权价格对波动率的绝对敏感度 ∂C/∂σ
# （未采用某些交易平台将 vega 除以 100 表示波动率每变动 1% 价格变化的惯例）
call_vega = S * np.sqrt(T) * norm.pdf(d1)

# ==================== 4. 填充 result ====================
result = {
    'call_price': call_price,
    'call_delta': call_delta,
    'call_vega': call_vega
}

# ==================== 课堂投屏展示 ====================
print("="*40)
print("Black-Scholes 欧式看涨期权计算结果")
print("="*40)
print(f"参数检核: S={S}, K={K}, sigma={sigma}, r={r}, T={T}")
print(f"步骤1: d1 = {d1:.6f}")
print(f"步骤1: d2 = {d2:.6f}")
print(f"步骤2: 期权价格 = {call_price:.4f}")
print(f"步骤2: Delta = {call_delta:.4f}")
print(f"步骤3: Vega (∂C/∂σ) = {call_vega:.4f}")
print("="*40)
print("输出契约字典 result:")
print(result)
