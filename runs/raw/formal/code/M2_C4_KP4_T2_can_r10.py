import numpy as np
from scipy.stats import norm
import matplotlib.pyplot as plt

# ==================== 参数定义 ====================
K = 97.5               # 行权价
r = 0.043              # 连续复利无风险利率
T = 0.58               # 剩余期限（年）
S_min, S_max = 70, 140 # 标的价格范围
S_points = 500         # 价格网格点数

# 可调参数：波动率列表（小数）
sigma_list = [0.15, 0.276, 0.40]

# ==================== 函数定义 ====================
def bs_call_delta(S, K, r, sigma, T):
    """计算欧式看涨期权的Delta"""
    d1 = (np.log(S / K) + (r + 0.5 * sigma**2) * T) / (sigma * np.sqrt(T))
    return norm.cdf(d1)

# ==================== 计算与绘图 ====================
S = np.linspace(S_min, S_max, S_points)

plt.figure(figsize=(8, 5))
for sigma in sigma_list:
    delta = bs_call_delta(S, K, r, sigma, T)
    plt.plot(S, delta, linewidth=2, label=f'σ = {sigma:.1%}')

# 图像标注
plt.xlabel('Underlying Price')
plt.ylabel('Delta')
plt.title('Delta Curve of European Call Option')
plt.legend()
plt.grid(True, alpha=0.3)
plt.tight_layout()

# 保存图形
fig_path = 'delta_curve.png'
plt.savefig(fig_path, dpi=150)
plt.close()  # 避免在非交互环境弹出窗口

# ==================== 报告特定点 ====================
S_specific = 110.0
sigma_specific = 0.276
delta_at_s110 = bs_call_delta(S_specific, K, r, sigma_specific, T)

# ==================== 输出结果 ====================
result = {
    'delta_at_s110': delta_at_s110,   # 小数形式
    'figure_path': fig_path
}

print(result)
