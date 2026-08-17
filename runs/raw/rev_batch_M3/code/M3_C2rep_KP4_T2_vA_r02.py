import numpy as np
from scipy.stats import norm
import matplotlib.pyplot as plt

def bs_call_delta(S, K, r, T, sigma):
    """
    计算不分红欧式看涨期权的 Delta
    S: 标的价格，可以是数组
    K: 行权价
    r: 无风险利率
    T: 剩余期限（年）
    sigma: 波动率
    """
    d1 = (np.log(S / K) + (r + 0.5 * sigma**2) * T) / (sigma * np.sqrt(T))
    return norm.cdf(d1)

# ==================== 参数设定 ====================
K = 97.5          # 行权价
r = 0.043         # 无风险利率 4.3%
T = 0.58          # 剩余期限 0.58 年

# 波动率作为可调参数（列表形式，方便增删改）
volatilities = [0.15, 0.276, 0.40]

# 标的资产价格网格
S_grid = np.linspace(70, 140, 500)

# ==================== 1. 计算 Delta ====================
# 为每个波动率在网格上计算 delta，存入字典
delta_curves = {}
for sigma in volatilities:
    delta_curves[sigma] = bs_call_delta(S_grid, K, r, T, sigma)

# ==================== 2. 绘制 Delta 曲线 ====================
plt.figure(figsize=(10, 6))
for sigma in volatilities:
    plt.plot(S_grid, delta_curves[sigma], label=f'Vol = {sigma*100:.1f}%')

plt.title('European Call Option Delta vs. Spot Price (K=97.5, r=4.3%, T=0.58yr)')
plt.xlabel('Spot Price (S)')
plt.ylabel('Delta')
plt.legend(title='Volatility')
plt.grid(True, linestyle='--', alpha=0.7)

# 保存图形
figure_path = 'bs_delta_curve.png'
plt.savefig(figure_path, dpi=300, bbox_inches='tight')
plt.close()

# ==================== 3. 报告特定点的 Delta ====================
S_target = 110
sigma_target = 0.276
delta_at_s110 = bs_call_delta(S_target, K, r, T, sigma_target)

# ==================== 4. 填充 result 字典 ====================
result = {
    'delta_at_s110': float(delta_at_s110),
    'figure_path': figure_path
}

# 输出结果以供验证
print(f"标的110、波动率27.6%时的Delta为: {result['delta_at_s110']:.6f}")
print(f"图形已保存至: {result['figure_path']}")
print(result)
