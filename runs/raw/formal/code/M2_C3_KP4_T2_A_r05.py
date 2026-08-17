import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import norm
import os

# 参数设置
S_range = np.linspace(70, 140, 100)  # 标的价格范围
K = 97.5  # 行权价
r = 0.043  # 无风险利率（连续复利）
T = 0.58  # 剩余期限（年）
sigma_values = [0.15, 0.276, 0.40]  # 波动率参数

def calculate_delta(S, K, r, T, sigma):
    """计算看涨期权的Delta值（BS模型）"""
    d1 = (np.log(S / K) + (r + sigma**2 / 2) * T) / (sigma * np.sqrt(T))
    delta = norm.cdf(d1)
    return delta

# 计算各波动率下的Delta值
delta_results = {}
for sigma in sigma_values:
    delta_results[sigma] = calculate_delta(S_range, K, r, T, sigma)

# 计算特定点的Delta值（S=110, sigma=27.6%）
S_specific = 110
sigma_specific = 0.276
delta_specific = calculate_delta(S_specific, K, r, T, sigma_specific)

# 绘图
plt.figure(figsize=(12, 8))

colors = ['blue', 'red', 'green']
labels = ['σ = 15%', 'σ = 27.6%', 'σ = 40%']

for sigma, color, label in zip(sigma_values, colors, labels):
    plt.plot(S_range, delta_results[sigma], color=color, linewidth=2, label=label)
    
# 添加特定点标记
plt.scatter(S_specific, delta_specific, color='purple', s=100, zorder=5, 
           label=f'Delta at S=110, σ=27.6%: {delta_specific:.4f}')

# 图形美化
plt.xlabel('Underlying Price (S)', fontsize=12)
plt.ylabel('Delta', fontsize=12)
plt.title('Call Option Delta vs. Underlying Price\n(K=97.5, r=4.3%, T=0.58 years)', fontsize=14)
plt.grid(True, alpha=0.3)
plt.legend(fontsize=11)
plt.ylim(0, 1.05)
plt.xlim(70, 140)

# 添加参考线
plt.axhline(y=0.5, color='gray', linestyle='--', alpha=0.5, linewidth=1)
plt.axvline(x=K, color='orange', linestyle='--', alpha=0.5, linewidth=1, label=f'Strike (K={K})')

# 保存图形
figure_path = 'delta_vs_price.png'
plt.savefig(figure_path, dpi=300, bbox_inches='tight')
plt.close()

# 构建结果字典
result = {
    'delta_at_s110': float(delta_specific),
    'figure_path': os.path.abspath(figure_path)
}

print(f"Delta at S=110, σ=27.6%: {delta_specific:.6f}")
print(f"Figure saved to: {os.path.abspath(figure_path)}")

# 输出结果字典
result
