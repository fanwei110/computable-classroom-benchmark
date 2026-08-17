import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import norm

# ========================
# 可调参数区域
# ========================
K = 97.5               # 行权价
r = 0.043              # 无风险利率
T = 0.58               # 剩余期限（年）
S_grid = np.linspace(70, 140, 500)   # 标的价格网格

# 波动率列表（可调参数）
volatilities = [0.15, 0.276, 0.40]

# ========================
# 计算函数
# ========================
def bs_call_delta(S, K, r, T, sigma):
    """计算欧式看涨期权的 Delta（不分红）"""
    d1 = (np.log(S / K) + (r + 0.5 * sigma**2) * T) / (sigma * np.sqrt(T))
    return norm.cdf(d1)

# ========================
# 绘图
# ========================
plt.figure(figsize=(10, 6))
for sigma in volatilities:
    delta = bs_call_delta(S_grid, K, r, T, sigma)
    plt.plot(S_grid, delta, label=f'$\sigma$ = {sigma*100:.1f}%')

plt.xlabel('标的资产价格')
plt.ylabel('Delta')
plt.title('不同波动率下的看涨期权 Delta')
plt.legend()
plt.grid(True)

# 保存图形
figure_path = 'delta_curve.png'
plt.savefig(figure_path, dpi=150)
plt.close()

# ========================
# 报告特定点的 Delta
# ========================
S_target = 110
sigma_target = 0.276
delta_target = bs_call_delta(S_target, K, r, T, sigma_target)

# ========================
# 输出结果
# ========================
result = {
    'delta_at_s110': delta_target,
    'figure_path': figure_path
}

print(result)
