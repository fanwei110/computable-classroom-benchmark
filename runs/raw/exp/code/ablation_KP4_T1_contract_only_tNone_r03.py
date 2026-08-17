import numpy as np
from scipy.stats import norm
import pandas as pd
import matplotlib.pyplot as plt

# 设定参数
S = 103.7      # 当前股票价格
K = 97.5       # 行权价
r = 0.043      # 无风险利率
sigma = 0.276  # 隐含波动率
T = 0.58       # 剩余期限（年）

# Black-Scholes模型计算
def black_scholes_call(S, K, r, sigma, T):
    """
    计算欧式看涨期权的价格、delta和vega
    """
    # 计算d1和d2
    d1 = (np.log(S / K) + (r + 0.5 * sigma ** 2) * T) / (sigma * np.sqrt(T))
    d2 = d1 - sigma * np.sqrt(T)
    
    # 期权价格
    call_price = S * norm.cdf(d1) - K * np.exp(-r * T) * norm.cdf(d2)
    
    # Delta (N(d1) for call option)
    call_delta = norm.cdf(d1)
    
    # Vega (灵敏度相对于波动率)
    call_vega = S * norm.pdf(d1) * np.sqrt(T)
    
    return call_price, call_delta, call_vega

# 计算期权价格、delta和vega
call_price, call_delta, call_vega = black_scholes_call(S, K, r, sigma, T)

# 创建结果字典
result = {
    'call_price': call_price,
    'call_delta': call_delta,
    'call_vega': call_vega
}

# 打印结果（用于验证）
print(f"期权价格: {call_price:.4f}")
print(f"Delta: {call_delta:.4f}")
print(f"Vega: {call_vega:.4f}")

# 创建一个简单的可视化（可选）
fig, ax = plt.subplots(figsize=(10, 6))

# 展示在不同股票价格下的期权价格
stock_prices = np.linspace(80, 120, 100)
option_prices = []
option_deltas = []
option_vegas = []

for sp in stock_prices:
    cp, cd, cv = black_scholes_call(sp, K, r, sigma, T)
    option_prices.append(cp)
    option_deltas.append(cd)
    option_vegas.append(cv)

# 绘制期权价格曲线
ax.plot(stock_prices, option_prices, 'b-', linewidth=2, label='期权价格')
ax.axvline(x=S, color='r', linestyle='--', alpha=0.7, label=f'当前股价 (S={S})')
ax.axhline(y=call_price, color='g', linestyle='--', alpha=0.7, label=f'当前期权价格 ({call_price:.2f})')
ax.grid(True, alpha=0.3)
ax.set_xlabel('股票价格')
ax.set_ylabel('期权价格')
ax.set_title('欧式看涨期权价格与股票价格关系')
ax.legend()
plt.tight_layout()
plt.show()

# 确保result字典包含所有要求的键
print("\n结果字典:")
print(f"call_price: {result['call_price']:.4f}")
print(f"call_delta: {result['call_delta']:.4f}")
print(f"call_vega: {result['call_vega']:.4f}")
