import numpy as np
from scipy.stats import norm
import matplotlib.pyplot as plt

# ==================== 1. 参数设定 ====================
K = 97.5              # 行权价 (Strike price)
r = 0.043             # 无风险利率 (Risk-free rate, 连续复利)
T = 0.58              # 剩余期限 (Time to maturity, 年)
q = 0.0               # 股息率 (Dividend yield, 无分红)

# 标的资产价格网格
S_min, S_max = 70, 140
S_grid = np.linspace(S_min, S_max, 500)

# 波动率参数化 (可调参数)
volatilities = [0.15, 0.276, 0.40]

# 报告要求的特定计算点
S_target = 110.0
sigma_target = 0.276

# ==================== 2. 核心计算函数 ====================
def calc_d1(S, K, r, q, sigma, T):
    """
    计算 Black-Scholes 模型中的 d1
    公式: d1 = [ln(S/K) + (r - q + 0.5 * sigma^2) * T] / (sigma * sqrt(T))
    """
    return (np.log(S / K) + (r - q + 0.5 * sigma**2) * T) / (sigma * np.sqrt(T))

def calc_call_delta(S, K, r, q, sigma, T):
    """
    计算欧式看涨期权的 Delta
    公式: Delta = N(d1)
    """
    d1 = calc_d1(S, K, r, q, sigma, T)
    return norm.cdf(d1)

# ==================== 3. 特定点的 Delta 计算 ====================
# 计算标的110，波动率27.6%时的delta
delta_at_s110 = calc_call_delta(S_target, K, r, q, sigma_target, T)

# ==================== 4. 绘制 Delta 曲线 ====================
plt.figure(figsize=(10, 6))

# 遍历不同的波动率参数并画图
for sigma in volatilities:
    deltas = calc_call_delta(S_grid, K, r, q, sigma, T)
    plt.plot(S_grid, deltas, label=f'σ = {sigma*100:.1f}%')

# 图表格式设置
plt.title('European Call Option Delta vs. Underlying Price', fontsize=14)
plt.xlabel('Underlying Price (S)', fontsize=12)
plt.ylabel('Delta (N(d1))', fontsize=12)
plt.legend(title='Volatility', fontsize=10)
plt.grid(True, linestyle='--', alpha=0.7)

# 保存图形
fig_path = 'european_call_delta_curves.png'
plt.savefig(fig_path, dpi=150, bbox_inches='tight')
plt.close()

# ==================== 5. 填充并输出结果 ====================
result = {
    'delta_at_s110': delta_at_s110,
    'figure_path': fig_path
}

# 在控制台输出结果以便课堂展示
print(f"=== 计算结果 ===")
print(f"标的: {S_target}, 波动率: {sigma_target*100}% 时的 Delta: {delta_at_s110:.6f}")
print(f"图表已保存至: {fig_path}")
print(f"result 字典内容: {result}")
