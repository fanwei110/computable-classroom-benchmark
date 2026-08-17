import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import norm

# ================= 参数设定 =================
K = 97.5          # 行权价
r = 0.043         # 无风险利率 (4.3%)
T = 0.58          # 到期时间 (年)
vols = [0.15, 0.276, 0.40]  # 三条曲线的波动率
S_min, S_max = 70, 140      # 标的资产价格范围
S_grid = np.linspace(S_min, S_max, 500) # 标的资产价格网格

# ================= BS 定价与希腊字母公式 =================
# 欧式看涨期权的 Delta 闭式解
def bs_call_delta(S, K, r, T, sigma):
    """
    计算欧式看涨期权的 Delta
    S: 标的资产价格 (可以是数组)
    K: 行权价
    r: 无风险利率
    T: 到期时间
    sigma: 波动率
    """
    d1 = (np.log(S / K) + (r + 0.5 * sigma**2) * T) / (sigma * np.sqrt(T))
    return norm.cdf(d1)

# ================= 1. 计算特定点及网格上的 Delta =================
# 计算标的110，波动率27.6%的Delta
delta_s110_vol276 = bs_call_delta(110, K, r, T, 0.276)

# 计算每个波动率在标的网格上的 delta
delta_curves = {}
for vol in vols:
    delta_curves[vol] = bs_call_delta(S_grid, K, r, T, vol)

# ================= 2. 绘制 Delta 曲线 =================
# 设置中文字体和负号显示
plt.rcParams['font.sans-serif'] = ['SimHei', 'Arial Unicode MS']
plt.rcParams['axes.unicode_minus'] = False

fig, ax = plt.subplots(figsize=(10, 6))

# 绘制三条不同波动率的曲线
for vol in vols:
    ax.plot(S_grid, delta_curves[vol], label=f'Vol = {vol*100:.1f}%', linewidth=2)

# 图表修饰
ax.set_title('欧式看涨期权 Delta 随标的资产价格变化曲线', fontsize=14)
ax.set_xlabel('标的资产价格 (S)', fontsize=12)
ax.set_ylabel('Delta', fontsize=12)
ax.axhline(0, color='black', linewidth=0.5)
ax.axvline(K, color='grey', linestyle='--', linewidth=0.8, label=f'行权价 K={K}')
ax.legend(fontsize=11)
ax.grid(True, linestyle='--', alpha=0.7)

# 保存图形
figure_path = 'delta_curve.png'
fig.savefig(figure_path, dpi=150, bbox_inches='tight')
plt.close(fig)

# ================= 3. 输出结果 =================
# 构建符合输出契约的 result 字典
result = {
    'delta_at_s110': float(delta_s110_vol276),
    'figure_path': figure_path
}

# 控制台打印验证
print(f"【计算结果】标的资产价格 110, 波动率 27.6% 时的看涨期权 Delta: {result['delta_at_s110']:.6f}")
print(f"【图形保存】图表已保存至: {result['figure_path']}")
print("\n最终返回的 result 字典:")
print(result)
