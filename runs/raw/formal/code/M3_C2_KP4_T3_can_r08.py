import numpy as np
from scipy.stats import norm

# ==================== 输入参数 ====================
S = 103.7        # 标的现价
K = 97.5         # 行权价
sigma = 0.276    # 波动率 27.6%
r = 0.043        # 无风险利率 4.3%
T = 0.58         # 剩余期限 (年)
d_sigma = 0.01   # 隐含波动率上升一个百分点 (1%)

# ==================== Black-Scholes 闭式解 ====================
# 计算 d1
d1 = (np.log(S / K) + (r + 0.5 * sigma**2) * T) / (sigma * np.sqrt(T))

# 计算 Vega (对波动率的敏感度，闭式解)
# Vega = S * N'(d1) * sqrt(T)
vega = S * norm.pdf(d1) * np.sqrt(T)

# ==================== 推算价格响应 ====================
# 利用 Vega 推算：波动率变化 d_sigma 引起的价格变化约为 vega * d_sigma
price_change = vega * d_sigma

# ==================== 验证对比 (供课堂展示参考) ====================
# 为验证线性近似的准确性，可使用BS定价公式计算精确的绝对价格变化
d2 = d1 - sigma * np.sqrt(T)
price_original = S * norm.cdf(d1) - K * np.exp(-r * T) * norm.cdf(d2)

d1_up = (np.log(S / K) + (r + 0.5 * (sigma + d_sigma)**2) * T) / ((sigma + d_sigma) * np.sqrt(T))
d2_up = d1_up - (sigma + d_sigma) * np.sqrt(T)
price_up = S * norm.cdf(d1_up) - K * np.exp(-r * T) * norm.cdf(d2_up)

exact_price_change = price_up - price_original

print(f"Vega 近似推算价格变化: {price_change:.4f}")
print(f"BS公式精确价格变化  : {exact_price_change:.4f}")
print(f"近似误差            : {abs(price_change - exact_price_change):.6f}")

# ==================== 输出契约 ====================
result = {
    'price_change': price_change
}
