import numpy as np
from scipy.stats import norm

# ================== 1. 参数设定 ==================
S = 103.7        # 标的资产现价
K = 97.5         # 行权价
sigma = 0.276    # 波动率 (27.6%)
r = 0.043        # 无风险利率 (4.3%)
T = 0.58         # 剩余期限 (年)

# 隐含波动率上升一个百分点 (绝对量变化 0.01)
delta_sigma = 0.01

# ================== 2. 闭式解计算 ==================
# 计算 d1 和 d2
d1 = (np.log(S / K) + (r + 0.5 * sigma**2) * T) / (sigma * np.sqrt(T))
d2 = d1 - sigma * np.sqrt(T)

# 看涨期权价格 (闭式解)
call_price = S * norm.cdf(d1) - K * np.exp(-r * T) * norm.cdf(d2)

# 希腊字母 Vega (闭式解)
# Vega 表示波动率变化 1 个单位时，期权价格的绝对变化量
vega = S * norm.pdf(d1) * np.sqrt(T)

# ================== 3. 推算价格变化 ==================
# 根据希腊字母的一阶泰勒展开近似：ΔC ≈ Vega * Δσ
# 这正是"利用希腊字母推算价格响应"的标准做法
price_change = vega * delta_sigma

# (补充对照) 精确计算波动率上升1%后的价格变化
sigma_new = sigma + delta_sigma
d1_new = (np.log(S / K) + (r + 0.5 * sigma_new**2) * T) / (sigma_new * np.sqrt(T))
d2_new = d1_new - sigma_new * np.sqrt(T)
call_price_new = S * norm.cdf(d1_new) - K * np.exp(-r * T) * norm.cdf(d2_new)
price_change_exact = call_price_new - call_price

# ================== 4. 存入结果字典 ==================
result = {
    'price_change': price_change
}

# ================== 5. 课堂展示打印 ==================
print(f"--- Black-Scholes 欧式看涨期权 ---")
print(f"当前期权价格: {call_price:.4f}")
print(f"当前 Vega:    {vega:.4f}")
print(f"----------------------------------")
print(f"波动率上升1个百分点(Δσ=0.01):")
print(f"  用 Vega 推算的价格变化: {price_change:.4f}")
print(f"  精确重新定价的价格变化(对照): {price_change_exact:.4f}")
print(f"----------------------------------")
print(f"输出结果 result: {result}")
