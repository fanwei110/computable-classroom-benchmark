import numpy as np
from scipy.stats import norm

def black_scholes_call(S, K, T, r, sigma):
    """
    计算欧式看涨期权的 Black-Scholes 价格和 Greeks
    
    参数:
    S: 标的资产现价
    K: 行权价
    T: 剩余到期时间（年）
    r: 无风险利率
    sigma: 波动率
    
    返回:
    price: 期权价格
    delta: Delta
    vega: Vega（波动率变化1个百分点对价格的影响）
    """
    d1 = (np.log(S / K) + (r + 0.5 * sigma**2) * T) / (sigma * np.sqrt(T))
    d2 = d1 - sigma * np.sqrt(T)
    
    # 期权价格
    price = S * norm.cdf(d1) - K * np.exp(-r * T) * norm.cdf(d2)
    
    # Delta
    delta = norm.cdf(d1)
    
    # Vega: 波动率变化1个单位（即100个百分点）对价格的影响
    # 但通常Vega表示波动率变化1个百分点（0.01）对价格的影响
    vega = S * np.sqrt(T) * norm.pdf(d1) * 0.01
    
    return price, delta, vega

# 给定参数
S = 103.7      # 标的资产现价
K = 97.5       # 行权价
T = 0.58       # 剩余到期时间（年）
r = 0.043      # 无风险利率
sigma = 0.276  # 当前波动率

# 计算当前期权价格和Vega
current_price, delta, vega = black_scholes_call(S, K, T, r, sigma)

# 隐含波动率上升1个百分点（0.01），期权价格的变化
# Vega已经定义为波动率变化0.01时的价格变化，所以直接使用vega值
price_change = vega

# 验证：用新的波动率重新计算价格
sigma_new = sigma + 0.01  # 波动率上升1个百分点
new_price, _, _ = black_scholes_call(S, K, T, r, sigma_new)
actual_change = new_price - current_price

# 输出结果
print("=" * 50)
print("Black-Scholes 欧式看涨期权定价与Vega计算")
print("=" * 50)
print(f"标的资产现价 (S): {S}")
print(f"行权价 (K): {K}")
print(f"剩余到期时间 (T): {T} 年")
print(f"无风险利率 (r): {r*100}%")
print(f"当前波动率 (σ): {sigma*100}%")
print("-" * 50)
print(f"当前期权价格: {current_price:.6f}")
print(f"Delta: {delta:.6f}")
print(f"Vega (波动率↑1个百分点): {vega:.6f}")
print("-" * 50)
print(f"波动率上升1个百分点后的期权价格: {new_price:.6f}")
print(f"期权价格变化 (Vega): {price_change:.6f}")
print(f"价格变化验证: {actual_change:.6f}")
print("=" * 50)

# 按要求存储结果
result = {
    'price_change': float(price_change)
}

print("\n结果字典:")
print(result)
