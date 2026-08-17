import numpy as np
from scipy.stats import norm
import matplotlib.pyplot as plt
import os

# ------------------------------
# 1. 定义 Black-Scholes 看涨期权 Delta 函数
# ------------------------------
def bs_call_delta(S, K, T, r, sigma):
    """欧式看涨期权 Delta：N(d1)"""
    d1 = (np.log(S / K) + (r + 0.5 * sigma**2) * T) / (sigma * np.sqrt(T))
    return norm.cdf(d1)

# ------------------------------
# 2. 参数设置（波动率可调）
# ------------------------------
K = 97.5          # 行权价
r = 0.043         # 无风险利率（连续复利）
T = 0.58          # 剩余期限（年）
S_grid = np.linspace(70, 140, 300)  # 标的价格网格

# 可调波动率列表
sigmas = [0.15, 0.276, 0.40]

# ------------------------------
# 3. 计算 Delta 并画图
# ------------------------------
plt.figure(figsize=(10, 6))
for sigma in sigmas:
    delta = bs_call_delta(S_grid, K, T, r, sigma)
    plt.plot(S_grid, delta, label=f"$\sigma$ = {sigma*100:.1f}%")

# 图形标注
plt.title("Black-Scholes Call Delta vs. Underlying Price")
plt.xlabel("Underlying Price S")
plt.ylabel("Delta")
plt.legend()
plt.grid(True)
plt.tight_layout()

# 保存图形
figure_path = "delta_vs_S.png"
plt.savefig(figure_path, dpi=150)
plt.close()

# ------------------------------
# 4. 报告特定点的 Delta
# ------------------------------
S_specific = 110.0
sigma_specific = 0.276
delta_at_s110 = bs_call_delta(S_specific, K, T, r, sigma_specific)

# ------------------------------
# 5. 构造输出字典
# ------------------------------
result = {
    'delta_at_s110': delta_at_s110,
    'figure_path': os.path.abspath(figure_path)
}

# 打印结果以便检查（教师投屏时可看到）
print("=== Black-Scholes Delta 计算结果 ===")
print(f"标的 S=110, 波动率=27.6% 时的看涨期权 Delta = {delta_at_s110:.6f}")
print(f"图形已保存至: {result['figure_path']}")
