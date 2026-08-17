import numpy as np
from scipy.stats import norm
import matplotlib.pyplot as plt
import pandas as pd

# =====================
# 参数设置 (课程计算约定：小数表示)
# =====================
K = 97.5          # 行权价
r = 0.043         # 无风险利率 (4.3%)
T = 0.58          # 剩余期限 (年)
q = 0.0           # 标的不分红，股息率设为0

# 波动率参数化（可调参数）
sigmas = [0.15, 0.276, 0.40]

# 标的资产价格网格
S_grid = np.linspace(70, 140, 500)

# 需要单独报告的特定点
S_target = 110.0
sigma_target = 0.276

# =====================
# 核心计算函数
# =====================
def bs_call_delta(S, K, r, q, T, sigma):
    """
    计算欧式看涨期权的 Delta = N(d1)
    参数:
        S: 标的资产价格 (可以是数组或标量)
        K: 行权价
        r: 无风险连续复利利率
        q: 连续股息收益率
        T: 剩余到期时间(年)
        sigma: 波动率
    返回:
        Delta 值
    """
    d1 = (np.log(S / K) + (r - q + 0.5 * sigma**2) * T) / (sigma * np.sqrt(T))
    return norm.cdf(d1)

# =====================
# 1 & 2. 计算并绘制不同波动率下的 Delta 曲线
# =====================
fig, ax = plt.subplots(figsize=(10, 6))

for sigma in sigmas:
    # 计算网格上的 delta
    deltas = bs_call_delta(S_grid, K, r, q, T, sigma)
    # 绘制曲线并添加图例标注
    ax.plot(S_grid, deltas, label=f'σ = {sigma*100:.1f}%')

# 图形美化
ax.set_xlabel('Underlying Price (S)', fontsize=12)
ax.set_ylabel('Delta (Δ)', fontsize=12)
ax.set_title('European Call Option Delta vs. Underlying Price', fontsize=14)
ax.legend(fontsize=11)
ax.grid(True, linestyle='--', alpha=0.7)

# 保存图形
figure_path = 'bs_delta_curve.png'
plt.savefig(figure_path, dpi=150, bbox_inches='tight')

# =====================
# 3. 报告标的 110、波动率 27.6% 时的 delta
# =====================
delta_at_s110 = bs_call_delta(S_target, K, r, q, T, sigma_target)

# =====================
# 4. 构造输出契约结果
# =====================
result = {
    'delta_at_s110': delta_at_s110,
    'figure_path': figure_path
}

# 打印结果供课堂投屏查看
print(f"标的110、波动率27.6%时的Delta: {result['delta_at_s110']:.6f}")
print(f"图形已保存至: {result['figure_path']}")
