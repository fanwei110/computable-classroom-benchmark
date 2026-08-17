import numpy as np
from scipy.stats import norm
import matplotlib.pyplot as plt

# ==================== 1. 参数设置 ====================
K = 97.5          # 行权价
r = 0.043         # 无风险利率 (年化)
T = 0.58          # 剩余期限 (年)
q = 0.0           # 标的不分红
S_grid = np.linspace(70, 140, 500)  # 标的价格网格
sigmas = [0.15, 0.276, 0.40]         # 波动率参数列表 (可调)

# ==================== 2. Black-Scholes 闭式解计算 Delta ====================
def bs_call_delta(S, K, r, T, sigma, q=0.0):
    """
    计算无分红欧式看涨期权的 Delta。
    S: 标的价格
    K: 行权价
    r: 无风险利率
    T: 剩余期限
    sigma: 波动率 (参数化)
    q: 连续股息率，默认为0
    """
    d1 = (np.log(S / K) + (r - q + 0.5 * sigma**2) * T) / (sigma * np.sqrt(T))
    return norm.cdf(d1)

# ==================== 3. 计算三条波动率曲线 ====================
delta_curves = {}
for sigma in sigmas:
    delta_curves[sigma] = bs_call_delta(S_grid, K, r, T, sigma, q)

# ==================== 4. 绘图 ====================
fig, ax = plt.subplots(figsize=(10, 6))

for sigma in sigmas:
    ax.plot(S_grid, delta_curves[sigma], linewidth=2, label=f'$\\sigma$ = {sigma:.1%}')

ax.set_title('European Call Delta vs Spot Price (K=97.5, r=4.3%, T=0.58yr)', fontsize=14)
ax.set_xlabel('Spot Price (S)', fontsize=12)
ax.set_ylabel('Delta', fontsize=12)
ax.axvline(x=K, color='grey', linestyle='--', linewidth=1, label=f'Strike K = {K}')
ax.legend(fontsize=11)
ax.grid(True, linestyle='--', alpha=0.6)

# ==================== 5. 报告指定条件下的 Delta ====================
target_S = 110
target_sigma = 0.276
delta_at_s110 = bs_call_delta(target_S, K, r, T, target_sigma, q)

# ==================== 6. 保存图形并封装输出 ====================
fig_path = 'european_call_delta_curve.png'
plt.savefig(fig_path, dpi=150, bbox_inches='tight')

# 将输出按要求严格存入 result 字典
result = {
    'delta_at_s110': delta_at_s110,
    'figure_path': fig_path
}

# 课堂展示辅助打印
print(f">>> 报告：标的 {target_S}、波动率 {target_sigma*100:.1f}% 时的 Delta 为: {delta_at_s110:.6f}")
print(f">>> 图形已保存至: {fig_path}")
