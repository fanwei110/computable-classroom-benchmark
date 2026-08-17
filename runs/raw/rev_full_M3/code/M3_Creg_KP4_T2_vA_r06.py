import numpy as np
import scipy.stats as norm
import matplotlib.pyplot as plt

# ---------------- 基本参数 ----------------
K = 97.5          # 行权价
r = 0.043         # 无风险利率 (年化)
T = 0.58          # 剩余期限 (年)
q = 0.0           # 股息率 (无分红)

# 标的价格范围
S_min = 70
S_max = 140
S_array = np.linspace(S_min, S_max, 700)

# 波动率可调参数及所需绘制的三个值
volatilities = [0.15, 0.276, 0.40]

# ---------------- 计算函数 ----------------
def calculate_d1(S, K, r, q, T, sigma):
    """计算 Black-Scholes 模型中的 d1"""
    return (np.log(S / K) + (r - q + 0.5 * sigma**2) * T) / (sigma * np.sqrt(T))

def calculate_call_delta(S, K, r, q, T, sigma):
    """计算欧式看涨期权的 Delta"""
    d1 = calculate_d1(S, K, r, q, T, sigma)
    return norm.norm.cdf(d1)

# ---------------- 绘制 Delta 曲线 ----------------
plt.figure(figsize=(10, 6))

for sigma in volatilities:
    delta_vals = calculate_call_delta(S_array, K, r, q, T, sigma)
    plt.plot(S_array, delta_vals, label=f'Volatility = {sigma*100:.1f}%')

plt.title('European Call Option Delta vs. Underlying Price')
plt.xlabel('Underlying Price (S)')
plt.ylabel('Delta')
plt.legend()
plt.grid(True, linestyle='--', alpha=0.7)

# 保存图片
figure_path = 'delta_curve.png'
plt.savefig(figure_path, dpi=150, bbox_inches='tight')
plt.close()

# ---------------- 计算特定条件下的 Delta ----------------
S_target = 110
sigma_target = 0.276
delta_at_s110 = calculate_call_delta(S_target, K, r, q, T, sigma_target)

# ---------------- 输出结果 ----------------
result = {
    'delta_at_s110': delta_at_s110,
    'figure_path': figure_path
}
