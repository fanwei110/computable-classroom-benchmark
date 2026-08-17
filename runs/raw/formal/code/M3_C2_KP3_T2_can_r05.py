import numpy as np
import matplotlib.pyplot as plt

# ================= 假设与基本参数设定 =================
# 假设：1. 每年付息一次；2. 面值在到期时随最后一次票息一起偿还
F = 100.0           # 面值
c = 0.046           # 票息率
C = F * c           # 每期票息支付额 (4.6)
T = 7               # 期限（年）
y0 = 0.053          # 当前收益率 (5.3%)
dy_100bp = 0.01     # 100个基点的收益率变动幅度 (1%)

# ================= 核心计算函数 =================
def bond_price(y):
    """
    计算给定收益率下的债券精确价格（支持标量和向量输入）
    P = Σ [C / (1+y)^t] + F / (1+y)^T
    """
    y = np.atleast_1d(y)
    t = np.arange(1, T + 1)
    cf = np.full(T, C)
    cf[-1] += F  # 最后一期加入本金
    pv = cf / (1 + y[:, None])**t
    return np.sum(pv, axis=1).squeeze()

def modified_duration(y):
    """
    计算修正久期 (Modified Duration)
    衡量收益率变动1单位时，价格的相对变化率
    """
    t = np.arange(1, T + 1)
    cf = np.full(T, C)
    cf[-1] += F
    pv = cf / (1 + y)**t
    P = np.sum(pv)
    mac_duration = np.sum(t * pv) / P  # 麦考利久期
    mod_duration = mac_duration / (1 + y)  # 修正久期
    return mod_duration

# ================= 步骤1 & 2：计算并绘制曲线 =================
# 1. 在 2% 到 9% 的收益率网格上为精确曲线定价
y_grid = np.linspace(0.02, 0.09, 1000)
exact_prices = bond_price(y_grid)

# 当前点的精确价格与修正久期
P0 = float(bond_price(y0))
ModD = modified_duration(y0)

# 2. 在当前收益率附近叠加基于久期的近似（可调收益率变动幅度）
# 设定近似曲线的变动幅度（此处设为±3%，即300个基点，可根据需要调整）
approx_amplitude = 0.03  
y_approx_grid = np.linspace(y0 - approx_amplitude, y0 + approx_amplitude, 500)

# 久期近似公式：P(y) ≈ P0 * [1 - ModD * (y - y0)]
approx_prices = P0 * (1 - ModD * (y_approx_grid - y0))

# 绘制图形
plt.rcParams['font.sans-serif'] = ['SimHei', 'Arial']  # 兼容中文与英文字体
plt.rcParams['axes.unicode_minus'] = False
plt.figure(figsize=(10, 6))

plt.plot(y_grid * 100, exact_prices, label='Exact Price-Yield Curve', color='blue', linewidth=2)
plt.plot(y_approx_grid * 100, approx_prices, label='Duration Approximation', color='red', linestyle='--', linewidth=2)

# 标出当前收益率的位置
plt.axvline(y0 * 100, color='grey', linestyle=':', alpha=0.7, label=f'Current Yield ({y0*100:.1f}%)')
plt.scatter([y0 * 100], [P0], color='black', s=60, zorder=5, label=f'Current Price ({P0:.2f})')

plt.title('Bond Price-Yield Curve & Duration Approximation', fontsize=14)
plt.xlabel('Yield to Maturity (%)', fontsize=12)
plt.ylabel('Bond Price', fontsize=12)
plt.legend(fontsize=11)
plt.grid(True, linestyle='--', alpha=0.6)

# 保存图形
fig_path = 'bond_price_yield_curve.png'
plt.savefig(fig_path, dpi=300, bbox_inches='tight')
plt.close()

# ================= 步骤3：报告 +100bp 的计算结果 =================
# 收益率上升100bp后的新收益率
y_up100 = y0 + dy_100bp

# 精确价格
price_at_up100bp = float(bond_price(y_up100))

# 久期法估计的相对价格变化 (ΔP/P ≈ -ModD * Δy)
dur_approx_change_up100bp = -ModD * dy_100bp

# ================= 步骤4：填充 result =================
result = {
    'price_at_up100bp': price_at_up100bp,
    'dur_approx_change_up100bp': dur_approx_change_up100bp,
    'figure_path': fig_path
}

# （可选）控制台打印输出，便于课堂投屏展示
print("="*50)
print("《证券投资学》课堂演示计算结果")
print("="*50)
print(f"当前收益率: {y0*100:.1f}% | 当前精确价格: {P0:.4f}")
print(f"修正久期: {ModD:.4f}")
print(f"收益率上升100bp后:")
print(f"  - 精确价格: {result['price_at_up100bp']:.4f}")
print(f"  - 久期法估计的相对价格变化: {result['dur_approx_change_up100bp']:.4f} ({result['dur_approx_change_up100bp']*100:.2f}%)")
print(f"图表已保存至: {result['figure_path']}")
print("="*50)
