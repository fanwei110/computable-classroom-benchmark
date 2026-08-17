import numpy as np
from scipy.stats import norm

# ============================================================
# Black-Scholes 公式与希腊字母（欧式看涨期权）
# ============================================================
def bs_price(S, K, T, r, sigma, option_type='call'):
    """Black-Scholes 期权价格闭式解"""
    if T <= 0 or sigma <= 0:
        return max(S - K, 0) if option_type == 'call' else max(K - S, 0)
    d1 = (np.log(S / K) + (r + 0.5 * sigma**2) * T) / (sigma * np.sqrt(T))
    d2 = d1 - sigma * np.sqrt(T)
    if option_type == 'call':
        price = S * norm.cdf(d1) - K * np.exp(-r * T) * norm.cdf(d2)
    else:
        price = K * np.exp(-r * T) * norm.cdf(-d2) - S * norm.cdf(-d1)
    return price

def bs_vega(S, K, T, r, sigma):
    """Black-Scholes vega：期权价格对波动率1个百分点的敏感度（即 sigma 变化 0.01）"""
    if T <= 0 or sigma <= 0:
        return 0.0
    d1 = (np.log(S / K) + (r + 0.5 * sigma**2) * T) / (sigma * np.sqrt(T))
    # vega_raw 是价格对 sigma 的偏导数（sigma 变动 1 单位的价格变化）
    # 再乘以 0.01 得到 sigma 变动 1 个百分点（即 0.01）的价格变化
    vega_raw = S * norm.pdf(d1) * np.sqrt(T)
    vega_one_pct = vega_raw * 0.01
    return vega_one_pct

# ============================================================
# 给定参数
# ============================================================
S     = 103.7      # 标的现价
K     = 97.5       # 行权价
T     = 0.58       # 剩余到期时间（年）
r     = 0.043      # 无风险利率
sigma = 0.276      # 当前波动率

# ============================================================
# 问题：隐含波动率涨一个百分点，期权价格涨多少？
# 这正好是 vega 的定义（vega = dPrice / d(sigma_one_pct)）
# ============================================================
price_change = bs_vega(S, K, T, r, sigma)

# 存入结果字典
result = {
    'price_change': price_change
}

# 输出以便课堂展示
print("============================================")
print("  Black-Scholes 期权希腊字母：Vega 计算")
print("============================================")
print(f"  标的现价 S      = {S}")
print(f"  行权价 K        = {K}")
print(f"  剩余到期 T      = {T} 年")
print(f"  无风险利率 r    = {r*100:.1f}%")
print(f"  当前波动率 σ    = {sigma*100:.1f}%")
print("--------------------------------------------")
print(f"  Vega（波动率+1%的价格变化） = {price_change:.4f}")
print("============================================")
print(f"\n  result = {result}")
