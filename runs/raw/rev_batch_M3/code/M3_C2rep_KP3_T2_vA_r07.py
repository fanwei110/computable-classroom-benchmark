import numpy as np
import matplotlib.pyplot as plt

# ==========================================
# 参数设定 (内部一致的假设：按年付息)
# ==========================================
FV = 100                      # 面值
coupon_rate = 0.046           # 票息率 4.6%
n_years = 7                   # 期限 7 年
y_current = 0.053             # 当前收益率 5.3%

# 收益率变动幅度（可调参数）：久期近似在当前收益率两侧的展示范围
YIELD_DELTA_RANGE = 0.02     # 默认上下 2%，教师可随时修改此值

# ==========================================
# 核心计算函数
# ==========================================
def bond_price(y, c_rate, fv, n):
    """计算债券精确价格（支持标量和向量）"""
    cf = np.array([c_rate * fv] * (n - 1) + [c_rate * fv + fv])
    t = np.arange(1, n + 1)
    y = np.asarray(y)
    if y.ndim == 0:
        return np.sum(cf / (1 + y) ** t)
    else:
        return np.sum(cf / (1 + y[:, None]) ** t, axis=1)

def mac_duration(y, c_rate, fv, n):
    """计算麦考利久期"""
    cf = np.array([c_rate * fv] * (n - 1) + [c_rate * fv + fv])
    t = np.arange(1, n + 1)
    p = bond_price(y, c_rate, fv, n)
    return np.sum(t * cf / (1 + y) ** t) / p

# ==========================================
# 计算当前状态与久期
# ==========================================
P0 = bond_price(y_current, coupon_rate, FV, n_years)
MacD = mac_duration(y_current, coupon_rate, FV, n_years)
ModD = MacD / (1 + y_current)  # 修正久期

# ==========================================
# 生成网格与定价
# ==========================================
# 1. 在 2% 到 9% 的收益率网格上为精确曲线定价
y_grid = np.linspace(0.02, 0.09, 500)
exact_prices = bond_price(y_grid, coupon_rate, FV, n_years)

# 2. 在 5.3% 附近叠加基于久期的近似 (P_approx = P0 * (1 - ModD * Δy))
y_approx_grid = np.linspace(y_current - YIELD_DELTA_RANGE, 
                             y_current + YIELD_DELTA_RANGE, 200)
approx_prices = P0 * (1 - ModD * (y_approx_grid - y_current))

# 3. 报告 +100bp 的精确价格与久期法估计的相对变化
y_up100 = y_current + 0.01
price_up100 = bond_price(y_up100, coupon_rate, FV, n_years)
dur_approx_change_up100 = -ModD * 0.01

# ==========================================
# 绘图
# ==========================================
plt.figure(figsize=(10, 6))
plt.plot(y_grid * 100, exact_prices, label='Exact Price-Yield Curve', color='blue', linewidth=2)
plt.plot(y_approx_grid * 100, approx_prices, label='Duration Approximation', color='red', linestyle='--', linewidth=2)

# 标记当前收益率点
plt.scatter([y_current * 100], [P0], color='black', zorder=5)
plt.annotate(f'Current Point\n(y={y_current*100:.1f}%, P={P0:.2f})', 
             xy=(y_current*100, P0), 
             xytext=(y_current*100 + 1.0, P0 + 2),
             arrowprops=dict(facecolor='black', shrink=0.05, width=1, headwidth=6))

plt.title('Bond Price-Yield Curve and Duration Approximation', fontsize=14)
plt.xlabel('Yield to Maturity (%)', fontsize=12)
plt.ylabel('Bond Price', fontsize=12)
plt.legend(fontsize=11)
plt.grid(True, linestyle=':', alpha=0.7)

# 保存图形
fig_path = 'price_yield_curve.png'
plt.savefig(fig_path, dpi=300, bbox_inches='tight')
plt.close()

# ==========================================
# 输出契约存入 result 字典
# ==========================================
result = {
    'price_at_up100bp': price_up100,
    'dur_approx_change_up100bp': dur_approx_change_up100,
    'figure_path': fig_path
}

# 课堂展示打印输出
print("="*50)
print("《证券投资学》债券定价与久期计算结果：")
print(f"当前收益率: {y_current*100:.1f}%")
print(f"当前精确价格: {P0:.4f}")
print(f"麦考利久期: {MacD:.4f}")
print(f"修正久期: {ModD:.4f}")
print("-"*50)
print(f"收益率上升 100bp 后:")
print(f"  精确价格: {result['price_at_up100bp']:.4f}")
print(f"  久期法估计的相对变化: {result['dur_approx_change_up100bp']:.4f} ({result['dur_approx_change_up100bp']*100:.2f}%)")
print(f"图表已保存至: {result['figure_path']}")
print("="*50)
