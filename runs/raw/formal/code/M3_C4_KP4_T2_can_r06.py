import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import norm

# ==========================================
# 1. 参数设定 (课程计算约定：小数表示)
# ==========================================
K = 97.5          # 行权价
r = 0.043         # 无风险利率 (连续复利)
T = 0.58          # 剩余期限 (年)
q = 0.0           # 标的不分红，股息率为0

# 波动率做成可调参数
volatilities = [0.15, 0.276, 0.40]

# 标的资产价格网格
S_min = 70
S_max = 140
S_grid = np.linspace(S_min, S_max, 500)

# ==========================================
# 2. 定义 Black-Scholes 欧式看涨期权 Delta 函数
# ==========================================
def bs_call_delta(S, K, T, r, q, sigma):
    """
    计算欧式看涨期权的 Delta = N(d1)
    S: 标的价格 (可以是数组)
    K: 行权价
    T: 剩余期限
    r: 无风险利率
    q: 连续股息率
    sigma: 波动率
    """
    d1 = (np.log(S / K) + (r - q + 0.5 * sigma**2) * T) / (sigma * np.sqrt(T))
    delta = norm.cdf(d1)
    return delta

# ==========================================
# 3. 计算标的110、波动率27.6%时的 delta
# ==========================================
S_target = 110
sigma_target = 0.276
delta_at_s110 = bs_call_delta(S_target, K, T, r, q, sigma_target)

# ==========================================
# 4. 绘制不同波动率下的 Delta 曲线
# ==========================================
plt.figure(figsize=(10, 6))

for sigma in volatilities:
    deltas = bs_call_delta(S_grid, K, T, r, q, sigma)
    plt.plot(S_grid, deltas, label=f'σ = {sigma*100:.1f}%')

plt.title('European Call Option Delta vs Spot Price (K=97.5, r=4.3%, T=0.58yr)')
plt.xlabel('Spot Price (S)')
plt.ylabel('Delta (Δ)')
plt.legend()
plt.grid(True)

# 保存图形
figure_path = 'delta_curve.png'
plt.savefig(figure_path, dpi=150, bbox_inches='tight')
plt.close()

# ==========================================
# 5. 填充并输出结果字典
# ==========================================
result = {
    'delta_at_s110': delta_at_s110,
    'figure_path': figure_path
}

# 打印结果以便查看
print(f"标的110、波动率27.6%时的Delta: {result['delta_at_s110']:.6f}")
print(f"图形已保存至: {result['figure_path']}")
