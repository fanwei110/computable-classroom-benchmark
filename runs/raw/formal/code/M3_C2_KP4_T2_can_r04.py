import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import norm

# ================= 假设与参数设定 =================
K = 97.5          # 行权价
r = 0.043         # 无风险利率 (每年 4.3%)
T = 0.58          # 剩余期限 (年)
q = 0.0           # 标的资产无分红

# 波动率参数化设定 (15%, 27.6%, 40%)
sigma_list = [0.15, 0.276, 0.40]

# 标的资产价格网格 (70 到 140)
S_grid = np.linspace(70, 140, 500)

# ================= 核心计算函数 =================
def bs_call_delta(S, K, T, r, sigma, q=0.0):
    """
    计算欧式看涨期权的 Delta (Black-Scholes 闭式解)
    Delta = exp(-q*T) * N(d1)
    """
    d1 = (np.log(S / K) + (r - q + 0.5 * sigma**2) * T) / (sigma * np.sqrt(T))
    delta = np.exp(-q * T) * norm.cdf(d1)
    return delta

# ================= 1 & 2. 计算 Delta 并画图 =================
plt.figure(figsize=(10, 6))

# 针对每个波动率在标的网格上计算 Delta 并绘制曲线
for sigma in sigma_list:
    deltas = bs_call_delta(S_grid, K, T, r, sigma, q)
    plt.plot(S_grid, deltas, label=f'Vol = {sigma*100:.1f}%')

# 添加图例和标注
plt.title('European Call Option Delta vs Underlying Price (K=97.5, T=0.58, r=4.3%)')
plt.xlabel('Underlying Price (S)')
plt.ylabel('Delta')
plt.legend()
plt.grid(True, linestyle='--', alpha=0.7)

# 保存图形
figure_path = 'delta_curve.png'
plt.savefig(figure_path, dpi=300, bbox_inches='tight')
plt.close()

# ================= 3. 报告特定点的 Delta =================
target_S = 110
target_sigma = 0.276
delta_at_s110 = bs_call_delta(target_S, K, T, r, target_sigma, q)

# ================= 4. 填充 result 字典 =================
result = {
    'delta_at_s110': delta_at_s110,
    'figure_path': figure_path
}

# 打印结果以供验证 (课堂展示辅助)
print(f"标的110、波动率27.6%时的Delta: {result['delta_at_s110']:.6f}")
print(f"图形已保存至: {result['figure_path']}")
