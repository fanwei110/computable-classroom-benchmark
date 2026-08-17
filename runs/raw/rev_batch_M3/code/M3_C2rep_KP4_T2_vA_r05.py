import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import norm

# ==================== 参数设定 ====================
K = 97.5            # 行权价
r = 0.043           # 无风险利率 (每年 4.3%)
T = 0.58            # 剩余期限 (年)
q = 0.0             # 股息率 (标的不分红)

S_min = 70          # 标的价格范围下限
S_max = 140         # 标的价格范围上限
S_target = 110      # 需要报告 delta 的特定标的价格

# 波动率可调参数设定
volatilities = [0.15, 0.276, 0.40]
sigma_target = 0.276

# ==================== Black-Scholes Delta 计算 ====================
def bs_call_delta(S, K, r, T, sigma, q=0.0):
    """
    计算不分红欧式看涨期权的 Delta (闭式解)
    Delta = N(d1)
    """
    d1 = (np.log(S / K) + (r - q + 0.5 * sigma**2) * T) / (sigma * np.sqrt(T))
    delta = norm.cdf(d1)
    return delta

# 1. 计算标的 110、波动率 27.6% 时的 delta
delta_at_s110 = bs_call_delta(S_target, K, r, T, sigma_target, q)

# 2. 在标的价格网格上计算不同波动率下的 delta
S_grid = np.linspace(S_min, S_max, 500)

# 3. 绘制带标注的三条 Delta 曲线
plt.figure(figsize=(10, 6))

for sigma in volatilities:
    deltas = bs_call_delta(S_grid, K, r, T, sigma, q)
    plt.plot(S_grid, deltas, label=f'σ = {sigma*100:.1f}%')

plt.title('European Call Option Delta vs. Underlying Price\n(K=97.5, r=4.3%, T=0.58yr, q=0%)')
plt.xlabel('Underlying Price (S)')
plt.ylabel('Delta')
plt.legend(title='Volatility')
plt.grid(True, linestyle='--', alpha=0.7)

# 4. 保存图形
figure_path = 'delta_curves.png'
plt.savefig(figure_path, dpi=300, bbox_inches='tight')
plt.close()

# ==================== 输出结果 ====================
result = {
    'delta_at_s110': delta_at_s110,
    'figure_path': figure_path
}

# 打印核心结果以便课堂投屏展示
print(f"标的 110、波动率 27.6% 时的 Delta 为: {delta_at_s110:.6f}")
print(f"图形已保存至: {figure_path}")
print(f"result 字典内容: {result}")
