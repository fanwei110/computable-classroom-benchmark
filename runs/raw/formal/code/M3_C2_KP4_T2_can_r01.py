import numpy as np
from scipy.stats import norm
import matplotlib.pyplot as plt

# ==================== 参数设置 ====================
K = 97.5          # 行权价
r = 0.043         # 无风险利率 (年化)
T = 0.58          # 剩余期限 (年)
S_min = 70        # 标的价格网格下限
S_max = 140       # 标的价格网格上限

# 波动率参数化（作为可调参数列表）
volatilities = [0.15, 0.276, 0.40]

# 需单独报告delta的特定参数
S_target = 110
vol_target = 0.276

# ==================== 核心计算函数 ====================
def bs_call_delta(S, K, T, r, sigma):
    """
    计算无分红欧式看涨期权的 Delta (闭式解)
    S: 标的价格 (可以是标量或 numpy 数组)
    K: 行权价
    T: 到期期限
    r: 无风险利率
    sigma: 波动率
    """
    d1 = (np.log(S / K) + (r + 0.5 * sigma**2) * T) / (sigma * np.sqrt(T))
    delta = norm.cdf(d1)
    return delta

# ==================== 步骤1：在标的网格上计算 delta ====================
# 生成标的价格网格
S_grid = np.linspace(S_min, S_max, 500)

# 用于存储各个波动率下的 delta 计算结果
delta_curves = {}
for sigma in volatilities:
    delta_curves[sigma] = bs_call_delta(S_grid, K, T, r, sigma)

# ==================== 步骤2：画三条带标注曲线 ====================
plt.figure(figsize=(10, 6))

# 定义颜色与线型以确保图表区分度
styles = ['-', '--', '-.']
colors = ['blue', 'orange', 'green']

for i, sigma in enumerate(volatilities):
    plt.plot(S_grid, delta_curves[sigma], 
             linestyle=styles[i], 
             color=colors[i], 
             label=f'Vol = {sigma*100:.1f}%')

plt.title('European Call Option Delta vs Underlying Price', fontsize=14)
plt.xlabel('Underlying Price (S)', fontsize=12)
plt.ylabel('Delta', fontsize=12)
plt.xlim(S_min, S_max)
plt.ylim(0, 1)
plt.grid(True, linestyle=':', alpha=0.7)
plt.legend(fontsize=11)

# 保存图形
figure_path = 'delta_curves.png'
plt.savefig(figure_path, dpi=300, bbox_inches='tight')
plt.close()

# ==================== 步骤3：报告标的110、波动率27.6%的 delta ====================
delta_at_s110 = float(bs_call_delta(S_target, K, T, r, vol_target))

# ==================== 步骤4：保存图形并填充 result ====================
result = {
    'delta_at_s110': delta_at_s110,
    'figure_path': figure_path
}

# 打印结果以便课堂投屏展示
print(f"标的 {S_target}、波动率 {vol_target*100}% 时的 Delta 为: {delta_at_s110:.6f}")
print(f"图形已保存至: {figure_path}")
