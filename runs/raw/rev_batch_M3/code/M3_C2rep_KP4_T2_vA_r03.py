import numpy as np
from scipy.stats import norm
import matplotlib.pyplot as plt
import os

# ================= 1. 参数设置 =================
K = 97.5          # 行权价
r = 0.043         # 无风险利率 (年化)
T = 0.58          # 剩余期限 (年)
q = 0.0           # 标的资产分红率 (标的不分红)

# 波动率参数化 (可调参数)
sigma_list = [0.15, 0.276, 0.40]

# 标的资产价格网格
S_grid = np.linspace(70, 140, 500)

# ================= 2. 核心计算函数 =================
def calc_d1(S, K, r, q, sigma, T):
    """计算 Black-Scholes 模型中的 d1"""
    return (np.log(S / K) + (r - q + 0.5 * sigma**2) * T) / (sigma * np.sqrt(T))

def calc_call_delta(S, K, r, q, sigma, T):
    """计算欧式看涨期权的 Delta"""
    d1 = calc_d1(S, K, r, q, sigma, T)
    return norm.cdf(d1)

# ================= 3. 计算与绘图 =================
# 设置 matplotlib 以支持中文显示 (若系统无SimHei则回退到默认英文)
plt.rcParams['font.sans-serif'] = ['SimHei', 'DejaVu Sans']
plt.rcParams['axes.unicode_minus'] = False

plt.figure(figsize=(10, 6))

# 对每个波动率计算 delta 并绘制曲线
for sigma in sigma_list:
    # 计算整个网格上的 delta
    deltas = calc_call_delta(S_grid, K, r, q, sigma, T)
    
    # 绘制带标注曲线
    label_str = f'Vol = {sigma*100:.1f}%'
    plt.plot(S_grid, deltas, label=label_str, linewidth=2)

# 添加图例和标签
plt.title('欧式看涨期权 Delta 随标的价格变化曲线', fontsize=14)
plt.xlabel('标的价格 (S)', fontsize=12)
plt.ylabel('Delta', fontsize=12)
plt.axhline(0, color='black', linewidth=0.5)
plt.axhline(1, color='black', linewidth=0.5, linestyle='--')
plt.grid(True, linestyle=':', alpha=0.7)
plt.legend(fontsize=12)

# 保存图形
figure_path = 'bs_delta_curves.png'
plt.savefig(figure_path, dpi=300, bbox_inches='tight')
plt.close()

# ================= 4. 计算特定点的 Delta 并填充结果 =================
# 标的 110、波动率 27.6% 时的 delta
specific_S = 110.0
specific_sigma = 0.276
delta_at_s110 = calc_call_delta(specific_S, K, r, q, specific_sigma, T)

# 按照输出契约构建 result 字典
result = {
    'delta_at_s110': delta_at_s110,
    'figure_path': figure_path
}

# 打印结果供课堂展示
print(f"标的价格 110, 波动率 27.6% 时的 Delta: {delta_at_s110:.6f}")
print(f"图形已保存至: {figure_path}")
