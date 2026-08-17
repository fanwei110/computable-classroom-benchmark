import numpy as np
from scipy.stats import norm
import matplotlib.pyplot as plt
import os

# ==================== 参数设置 ====================
K = 97.5           # 行权价
r = 0.043          # 无风险利率（年化）
T = 0.58           # 剩余期限（年）
S_min, S_max = 70, 140   # 标的价格范围
S_points = 500     # 价格点数

# 可调参数：波动率列表（以小数形式）
volatilities = [0.15, 0.276, 0.40]

# 特定计算点
S_specific = 110
sigma_specific = 0.276

# ==================== 函数定义 ====================
def black_scholes_delta(S, K, r, T, sigma):
    """
    计算欧式看涨期权的 delta
    S: 标的价格（标量或数组）
    K: 行权价
    r: 无风险利率
    T: 剩余期限（年）
    sigma: 波动率
    """
    d1 = (np.log(S / K) + (r + 0.5 * sigma**2) * T) / (sigma * np.sqrt(T))
    delta = norm.cdf(d1)
    return delta

# ==================== 计算特定点 delta ====================
delta_at_s110 = black_scholes_delta(S_specific, K, r, T, sigma_specific)

# ==================== 生成绘图数据并保存图片 ====================
S_range = np.linspace(S_min, S_max, S_points)

plt.figure(figsize=(10, 6))
for sigma in volatilities:
    delta_values = black_scholes_delta(S_range, K, r, T, sigma)
    plt.plot(S_range, delta_values, label=f'σ = {sigma*100:.1f}%')

plt.xlabel('Spot Price (S)')
plt.ylabel('Delta')
plt.title('Delta of European Call Option (K=97.5, r=4.3%, T=0.58)')
plt.legend()
plt.grid(True)

# 保存图片，使用绝对路径以保证路径可追溯
figure_path = os.path.abspath('delta_curve.png')
plt.savefig(figure_path, dpi=150, bbox_inches='tight')
plt.close()

# ==================== 构建输出字典 ====================
result = {
    'delta_at_s110': delta_at_s110,
    'figure_path': figure_path
}

print(result)
