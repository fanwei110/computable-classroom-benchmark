import numpy as np
from scipy.stats import norm
import matplotlib.pyplot as plt

# -------------------- 基本参数 --------------------
K = 97.5          # 行权价
r = 0.043         # 无风险利率
T = 0.58          # 剩余期限（年）
q = 0.0           # 标的无分红

# -------------------- 可调参数：波动率列表 --------------------
# 学生或教师可在此处直接修改波动率取值
sigmas = [0.15, 0.276, 0.40]

# -------------------- 函数定义 --------------------
def delta_call(S, K, T, r, sigma, q=0.0):
    """计算欧式看涨期权的 Delta（Black-Scholes 公式）"""
    d1 = (np.log(S / K) + (r - q + 0.5 * sigma**2) * T) / (sigma * np.sqrt(T))
    return np.exp(-q * T) * norm.cdf(d1)

# -------------------- 绘制 Delta 曲线 --------------------
S_grid = np.linspace(70, 140, 500)   # 标的价格网格

plt.figure(figsize=(10, 6))
for sigma in sigmas:
    delta_vals = delta_call(S_grid, K, T, r, sigma, q)
    plt.plot(S_grid, delta_vals, label=f"σ = {sigma*100:.1f}%")

plt.xlabel("Spot Price")
plt.ylabel("Delta")
plt.title("Call Option Delta vs. Spot Price (Black-Scholes)")
plt.legend()
plt.grid(True)

# 保存图形
figure_path = "delta_curve.png"
plt.savefig(figure_path, dpi=150, bbox_inches="tight")
plt.close()

# -------------------- 报告特定点的 Delta --------------------
S_target = 110.0
sigma_target = 0.276
delta_at_target = delta_call(S_target, K, T, r, sigma_target, q)

# -------------------- 输出结果 --------------------
result = {
    'delta_at_s110': delta_at_target,
    'figure_path': figure_path
}

print(result)
