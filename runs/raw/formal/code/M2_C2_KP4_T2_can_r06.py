
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.stats import norm
import os

# ==================== 可调参数 ====================
K = 97.5                # 行权价
r = 0.043               # 无风险利率
T = 0.58                # 剩余期限（年）
S_min, S_max = 70, 140  # 标的价格范围
S_grid = np.linspace(S_min, S_max, 500)  # 标的价格网格
volatilities = [0.15, 0.276, 0.40]       # 波动率列表（可调参数）
S_target = 110.0                          # 报告 delta 的标的价格
sigma_target = 0.276                      # 报告 delta 的波动率
# =================================================

def bs_call_delta(S, K, T, r, sigma):
    """计算欧式看涨期权的 Black-Scholes Delta"""
    d1 = (np.log(S / K) + (r + 0.5 * sigma**2) * T) / (sigma * np.sqrt(T))
    return norm.cdf(d1)

# 1. 计算 delta 并绘图
plt.figure(figsize=(10, 6))
for sigma in volatilities:
    deltas = bs_call_delta(S_grid, K, T, r, sigma)
    plt.plot(S_grid, deltas, linewidth=2, label=f'σ = {sigma*100:.1f}%')

plt.xlabel('Underlying Price S')
plt.ylabel('Delta')
plt.title('Delta of European Call Option (Black-Scholes)')
plt.legend()
plt.grid(True, alpha=0.3)

# 保存图片
figure_filename = 'delta_curve.png'
plt.savefig(figure_filename, dpi=150, bbox_inches='tight')
plt.close()

# 2. 报告 S=110, σ=27.6% 时的 delta
delta_at_s110 = bs_call_delta(S_target, K, T, r, sigma_target)

# 3. 按要求存入字典
result = {
    'delta_at_s110': delta_at_s110,
    'figure_path': os.path.abspath(figure_filename)
}

# 课堂运行时可直接查看
print(result)
