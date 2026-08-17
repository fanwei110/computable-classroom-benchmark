import numpy as np
from scipy.stats import norm
import matplotlib.pyplot as plt

# ==================== 参数定义 ====================
K = 97.5                # 行权价
r = 0.043               # 无风险利率
T = 0.58                # 剩余期限（年）
# 可调参数：波动率列表（三条曲线）
volatilities = [0.15, 0.276, 0.40]

# ==================== 函数定义 ====================
def bs_call_delta(S, K, r, sigma, T):
    """
    计算欧式看涨期权的 Delta（无分红）
    """
    d1 = (np.log(S / K) + (r + 0.5 * sigma**2) * T) / (sigma * np.sqrt(T))
    return norm.cdf(d1)

# ==================== 绘图 ====================
S = np.linspace(70, 140, 500)  # 标的网格

plt.figure(figsize=(10, 6))
for sigma in volatilities:
    delta = bs_call_delta(S, K, r, sigma, T)
    plt.plot(S, delta, linewidth=2, label=f'σ = {sigma*100:.1f}%')

plt.xlabel('Spot Price')
plt.ylabel('Delta')
plt.title('Call Option Delta vs Spot Price (Black-Scholes)')
plt.legend()
plt.grid(True, alpha=0.3)

# 保存图形
figure_path = 'delta_curve.png'
plt.savefig(figure_path, dpi=150, bbox_inches='tight')
plt.show()

# ==================== 特定点计算 ====================
S_target = 110.0
sigma_target = 0.276
delta_at_s110 = bs_call_delta(S_target, K, r, sigma_target, T)

# ==================== 输出契约 ====================
result = {
    'delta_at_s110': delta_at_s110,
    'figure_path': figure_path
}

print(result)
