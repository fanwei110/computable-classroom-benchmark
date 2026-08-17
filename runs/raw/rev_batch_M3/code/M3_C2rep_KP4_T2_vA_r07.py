import numpy as np
from scipy.stats import norm
import matplotlib.pyplot as plt

# ==========================================
# 1. 参数设定 (内部一致的假设与给定条件)
# ==========================================
K = 97.5          # 行权价
r = 0.043         # 无风险利率 (每年 4.3%)
T = 0.58          # 剩余期限 (年)
q = 0.0           # 标的资产无股息 (题目未指明，假设为0)

S_min = 70        # 标的价格范围下限
S_max = 140       # 标的价格范围上限
S_grid = np.linspace(S_min, S_max, 500) # 生成标的资产价格网格

# 波动率参数化 (可调)
volatilities = [0.15, 0.276, 0.40]

# ==========================================
# 2. 定义 Black-Scholes 欧式看涨期权 Delta 函数
# ==========================================
def bs_call_delta(S, K, T, r, sigma, q=0.0):
    """
    计算欧式看涨期权的 Delta
    S: 标的价格 (可以是标量或数组)
    K: 行权价
    T: 到期时间
    r: 无风险利率
    sigma: 波动率
    q: 连续股息率
    """
    d1 = (np.log(S / K) + (r - q + 0.5 * sigma**2) * T) / (sigma * np.sqrt(T))
    delta = norm.cdf(d1)
    return delta

# ==========================================
# 3. 计算并绘制 Delta 曲线
# ==========================================
plt.figure(figsize=(10, 6))

# 遍历不同的波动率进行计算与绘图
for sigma in volatilities:
    # 计算网格上的 delta
    deltas = bs_call_delta(S_grid, K, T, r, sigma, q)
    # 绘制曲线，百分比显示波动率
    plt.plot(S_grid, deltas, label=f'Vol = {sigma*100:.1f}%', linewidth=2)

# 图形设置与标注 (采用英文标签以确保不同操作系统的字体兼容性)
plt.title('European Call Option Delta (Black-Scholes)', fontsize=14)
plt.xlabel('Underlying Price (S)', fontsize=12)
plt.ylabel('Delta', fontsize=12)
plt.axhline(0, color='grey', linestyle='--', linewidth=0.8)
plt.axhline(1, color='grey', linestyle='--', linewidth=0.8)
plt.legend(fontsize=11)
plt.grid(True, linestyle=':', alpha=0.7)

# 保存图形
figure_path = 'bs_delta_curve.png'
plt.savefig(figure_path, dpi=300, bbox_inches='tight')
plt.close()

# ==========================================
# 4. 报告特定参数下的 Delta
# ==========================================
S_target = 110
sigma_target = 0.276

# 计算标的110、波动率27.6%时的delta
delta_at_s110 = bs_call_delta(S_target, K, T, r, sigma_target, q)
delta_at_s110_rounded = round(delta_at_s110, 6)

# ==========================================
# 5. 填充输出契约字典 result
# ==========================================
result = {
    'delta_at_s110': delta_at_s110_rounded,
    'figure_path': figure_path
}

# 打印输出以供课堂投屏检验
print(f"标的110、波动率27.6%时的 Delta: {delta_at_s110_rounded}")
print(f"图形已保存至: {figure_path}")
print(f"Result字典: {result}")
