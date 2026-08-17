import numpy as np
from scipy.stats import norm

# ============================================================
# Black-Scholes 欧式看涨期权定价公式（连续复利）
# ============================================================
def black_scholes_call(S, K, T, r, sigma):
    """
    S : 标的现价
    K : 行权价
    T : 剩余期限（年）
    r : 连续复利无风险利率（小数）
    sigma : 波动率（小数）
    返回: 期权价格
    """
    if T <= 0 or sigma <= 0:
        # 边界情况处理
        return max(S - K, 0.0)
    
    d1 = (np.log(S / K) + (r + 0.5 * sigma**2) * T) / (sigma * np.sqrt(T))
    d2 = d1 - sigma * np.sqrt(T)
    
    price = S * norm.cdf(d1) - K * np.exp(-r * T) * norm.cdf(d2)
    return price

# ============================================================
# 给定参数
# ============================================================
S = 103.7        # 现价
K = 97.5         # 行权价
T = 0.58         # 剩余年限
r = 0.043        # 连续复利无风险利率
sigma0 = 0.276   # 当前隐含波动率 27.6%
sigma1 = 0.286   # 上升一个百分点后的波动率 28.6%

# ============================================================
# 分别在两个波动率下精确重定价
# ============================================================
price_at_27_6 = black_scholes_call(S, K, T, r, sigma0)
price_at_28_6 = black_scholes_call(S, K, T, r, sigma1)

# 精确价差（隐含波动率上升一个百分点带来的期权价格变动）
price_change = price_at_28_6 - price_at_27_6

# ============================================================
# 输出结果字典
# ============================================================
result = {
    'price_change': price_change
}

# 为了在课堂投屏时清晰展示，同时打印精确计算结果
if __name__ == "__main__":
    print("=" * 60)
    print("  欧式看涨期权 Black-Scholes 定价 — 隐含波动率敏感度")
    print("=" * 60)
    print(f"  标的现价 S        = {S}")
    print(f"  行权价 K          = {K}")
    print(f"  剩余期限 T (年)   = {T}")
    print(f"  连续复利利率 r    = {r:.4f} ({r*100:.2f}%)")
    print("-" * 60)
    print(f"  波动率 σ = {sigma0:.4f} ({sigma0*100:.2f}%) → 期权价格 = {price_at_27_6:.6f}")
    print(f"  波动率 σ = {sigma1:.4f} ({sigma1*100:.2f}%) → 期权价格 = {price_at_28_6:.6f}")
    print("-" * 60)
    print(f"  >>> 隐含波动率上升 1 个百分点，期权价格变动 = {price_change:.6f}")
    print("=" * 60)
    print(f"\n输出字典 result: {result}")
