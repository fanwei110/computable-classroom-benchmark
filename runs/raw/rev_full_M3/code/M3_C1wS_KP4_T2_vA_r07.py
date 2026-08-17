import numpy as np
from scipy.stats import norm
import matplotlib.pyplot as plt

# ==========================================
# 1. Black-Scholes Delta 闭式解计算函数
# ==========================================
# 假设处理：题目未指明看涨/看跌期权，按惯例默认计算欧式看涨期权的 Delta
def bs_call_delta(S, K, T, r, sigma):
    """
    计算欧式看涨期权的 Delta
    S: 标的资产价格 (可以是 numpy 数组)
    K: 行权价
    T: 剩余期限 (年)
    r: 无风险利率
    sigma: 波动率
    """
    d1 = (np.log(S / K) + (r + 0.5 * sigma**2) * T) / (sigma * np.sqrt(T))
    delta = norm.cdf(d1)
    return delta

# ==========================================
# 2. 参数设置与网格计算
# ==========================================
K = 97.5          # 行权价
r = 0.043         # 无风险利率 4.3%
T = 0.58          # 剩余期限 0.58 年

# 标的价格网格：从 70 到 140，取 700 个点保证曲线平滑
S_grid = np.linspace(70, 140, 700)

# 波动率参数化：提取为列表，方便后续遍历画图
volatilities = [0.15, 0.276, 0.40]

# ==========================================
# 3. 计算特定点 (S=110, sigma=27.6%) 的 Delta
# ==========================================
delta_at_s110 = bs_call_delta(S=110, K=K, T=T, r=r, sigma=0.276)

# ==========================================
# 4. 绘图：三条不同波动率的 Delta 曲线
# ==========================================
# 设置字体兼容（防止中文乱码，若无黑体则自动降级为英文默认字体，保证不出错）
plt.rcParams['font.sans-serif'] = ['SimHei', 'DejaVu Sans']
plt.rcParams['axes.unicode_minus'] = False

plt.figure(figsize=(10, 6))

# 遍历波动率参数，计算每个波动率下的 delta 并画线
for sigma in volatilities:
    deltas = bs_call_delta(S=S_grid, K=K, T=T, r=r, sigma=sigma)
    plt.plot(S_grid, deltas, label=f'σ = {sigma*100:.1f}%', linewidth=2)

# 图表修饰
plt.title('Delta vs. Spot Price (K=97.5, r=4.3%, T=0.58yr)', fontsize=14)
plt.xlabel('Spot Price (S)', fontsize=12)
plt.ylabel('Delta', fontsize=12)
plt.axvline(x=K, color='grey', linestyle='--', linewidth=1, alpha=0.7, label=f'Strike K = {K}')
plt.legend(fontsize=11)
plt.grid(True, linestyle='--', alpha=0.6)

# 保存图形
fig_path = 'delta_vs_spot.png'
plt.savefig(fig_path, dpi=300, bbox_inches='tight')
plt.close()

# ==========================================
# 5. 按契约输出 result 字典
# ==========================================
result = {
    'delta_at_s110': delta_at_s110,
    'figure_path': fig_path
}

# 课堂投屏辅助打印（验证结果用，不违背契约）
if __name__ == '__main__':
    print(f"标的110、波动率27.6%时的看涨期权Delta: {result['delta_at_s110']:.6f}")
    print(f"图形已保存至: {result['figure_path']}")
