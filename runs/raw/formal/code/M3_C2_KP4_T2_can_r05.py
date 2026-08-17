import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import norm

# ==================== 参数设置 ====================
K = 97.5            # 行权价
r = 0.043           # 无风险利率 (每年 4.3%)
T = 0.58            # 剩余期限 (年)
q = 0.0             # 标的资产连续股息率 (题目指明不分红，故为0)

# 波动率参数化 (可调)
volatilities = [0.15, 0.276, 0.40]

# 标的价格网格
S_min, S_max = 70, 140
S_grid = np.linspace(S_min, S_max, 500)

# ==================== 计算函数 ====================
def bs_call_delta(S, K, T, r, sigma, q=0.0):
    """
    计算欧式看涨期权的 Black-Scholes Delta
    S: 标的价格 (可以是标量或数组)
    K: 行权价
    T: 到期期限
    r: 无风险利率
    sigma: 波动率
    q: 股息率
    """
    d1 = (np.log(S / K) + (r - q + 0.5 * sigma**2) * T) / (sigma * np.sqrt(T))
    delta = np.exp(-q * T) * norm.cdf(d1)
    return delta

# ==================== 绘图 ====================
plt.figure(figsize=(10, 6))

# 对每个波动率在标的网格上计算 delta 并画曲线
for sigma in volatilities:
    delta_grid = bs_call_delta(S_grid, K, T, r, sigma, q)
    plt.plot(S_grid, delta_grid, label=f'σ = {sigma * 100:.1f}%')

# 图形装饰与标注
plt.title('European Call Option Delta (Black-Scholes)', fontsize=14)
plt.xlabel('Spot Price (S)', fontsize=12)
plt.ylabel('Delta', fontsize=12)
plt.axhline(0, color='black', linewidth=0.8, linestyle='--')
plt.axhline(1, color='black', linewidth=0.8, linestyle='--')
plt.grid(True, linestyle=':', alpha=0.7)
plt.legend(fontsize=11)

# 保存图形
figure_path = 'bs_delta_curves.png'
plt.savefig(figure_path, dpi=150, bbox_inches='tight')
plt.close()

# ==================== 报告特定参数下的 Delta ====================
S_target = 110
sigma_target = 0.276
delta_at_s110 = float(bs_call_delta(S_target, K, T, r, sigma_target, q))

# ==================== 填充结果 ====================
result = {
    'delta_at_s110': delta_at_s110,
    'figure_path': figure_path
}

# 打印结果供验证
print(result)
