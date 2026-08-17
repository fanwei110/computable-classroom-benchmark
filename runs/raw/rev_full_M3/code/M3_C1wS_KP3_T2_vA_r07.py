import numpy as np
import matplotlib.pyplot as plt

# ==========================================
# 债券参数与假设
# ==========================================
# 假设：债券按年付息，面值在到期时随最后一次票息一起偿还
FACE_VALUE = 100.0
COUPON_RATE = 0.046
MATURITY = 7
Y0 = 0.053

# 可调参数：久期近似线的收益率变动幅度（相对于初始收益率y0的上下浮动范围）
# 默认设为4%（即0.04），表示近似线覆盖 y0-4% 到 y0+4% 的区间
APPROX_DELTA_RANGE = 0.04

# ==========================================
# 核心计算逻辑
# ==========================================
# 生成现金流和时间点
times = np.arange(1, MATURITY + 1)
cashflows = np.full(MATURITY, FACE_VALUE * COUPON_RATE)
cashflows[-1] += FACE_VALUE  # 最后一期加入面值

def bond_price(y, t, cf):
    """计算债券精确价格（支持标量和数组形式的收益率y）"""
    # 如果y是一维数组，扩展维度以便进行广播计算
    if isinstance(y, np.ndarray):
        y_2d = y[:, np.newaxis]
    else:
        y_2d = y
    pv_cf = cf / ((1 + y_2d) ** t)
    return np.sum(pv_cf, axis=-1 if isinstance(y, np.ndarray) else 0)

# 1. 计算初始状态与久期
P0 = bond_price(Y0, times, cashflows)

# 计算麦考利久期
pv_cf_0 = cashflows / ((1 + Y0) ** times)
mac_duration = np.sum(times * pv_cf_0) / P0

# 计算修正久期
mod_duration = mac_duration / (1 + Y0)

# 2. 生成精确价格曲线与久期近似曲线的数据
# 收益率网格：2% 到 9%
y_grid = np.linspace(0.02, 0.09, 500)
P_grid = bond_price(y_grid, times, cashflows)

# 久期近似网格：在 y0 附近，幅度由 APPROX_DELTA_RANGE 控制
y_approx_grid = np.linspace(Y0 - APPROX_DELTA_RANGE, Y0 + APPROX_DELTA_RANGE, 500)
# 久期近似公式：P(y) ≈ P0 * (1 - ModD * (y - y0))
P_approx_grid = P0 * (1 - mod_duration * (y_approx_grid - Y0))

# 3. 报告 +100bp 的精确价格与久期法估计的相对变化
y_up100 = Y0 + 0.01
price_at_up100bp = bond_price(y_up100, times, cashflows)

# 久期法估计的相对价格变化: ΔP/P ≈ -ModD * Δy
dur_approx_change_up100bp = -mod_duration * 0.01

# ==========================================
# 绘图与保存
# ==========================================
# 设置中文字体支持
plt.rcParams['font.sans-serif'] = ['SimHei', 'Arial Unicode MS', 'DejaVu Sans']
plt.rcParams['axes.unicode_minus'] = False

fig, ax = plt.subplots(figsize=(10, 6))

# 绘制精确价格曲线
ax.plot(y_grid * 100, P_grid, label='精确价格曲线', color='blue', linewidth=2)

# 绘制久期近似价格曲线
ax.plot(y_approx_grid * 100, P_approx_grid, label='久期近似价格曲线', 
        color='red', linestyle='--', linewidth=2)

# 标注初始点
ax.scatter([Y0 * 100], [P0], color='black', zorder=5, 
           label=f'初始状态 (y={Y0*100:.1f}%, P={P0:.2f})')

# 标注 +100bp 点
ax.scatter([y_up100 * 100], [price_at_up100bp], color='green', zorder=5, marker='x', s=100,
           label=f'+100bp精确价格 (P={price_at_up100bp:.2f})')

ax.set_title('债券价格-收益率关系及久期近似', fontsize=14)
ax.set_xlabel('收益率 (%)', fontsize=12)
ax.set_ylabel('债券价格', fontsize=12)
ax.legend(fontsize=11)
ax.grid(True, linestyle=':', alpha=0.7)

figure_path = 'bond_duration_convexity_plot.png'
plt.savefig(figure_path, dpi=150, bbox_inches='tight')
plt.close()

# ==========================================
# 封装输出结果
# ==========================================
result = {
    'price_at_up100bp': float(round(price_at_up100bp, 6)),
    'dur_approx_change_up100bp': float(round(dur_approx_change_up100bp, 6)),
    'figure_path': figure_path
}

# 课堂投屏辅助打印
print("--- 计算结果 ---")
print(f"初始收益率: {Y0*100:.1f}%")
print(f"初始精确价格: {P0:.4f}")
print(f"修正久期: {mod_duration:.4f}")
print(f"+100bp后精确价格: {result['price_at_up100bp']:.4f}")
print(f"+100bp久期法估计的相对变化: {result['dur_approx_change_up100bp']:.6f} (即 {result['dur_approx_change_up100bp']*100:.4f}%)")
print(f"图形已保存至: {result['figure_path']}")
