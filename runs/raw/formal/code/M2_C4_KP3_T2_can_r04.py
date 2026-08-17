import numpy as np
import matplotlib.pyplot as plt
import os

# ==================== 债券参数 ====================
FACE = 100.0          # 面值
COUPON = 4.6          # 票息（年付一次）
MATURITY = 7          # 期限（年）
Y0 = 0.053            # 当前收益率（年复利，小数）

# 近似曲线展示的收益率窗口（可调参数，例如 0.015 表示 ±1.5% 范围）
APPROX_WINDOW = 0.02  # 在 Y0 ± APPROX_WINDOW 内绘制久期/凸性近似

# 用于报告的收益率变动（默认 100 bp）
DY_REPORT = 0.01

# ==================== 定价与风险指标函数 ====================
def bond_price(y, face=FACE, coupon=COUPON, maturity=MATURITY):
    """
    计算年付息债券的精确价格（现金流贴现之和）。
    y 可以是标量或一维数组。
    """
    y = np.asarray(y, dtype=float)
    t = np.arange(1, maturity + 1)
    cf = np.full(maturity, coupon)
    cf[-1] += face
    if y.ndim == 0:
        return np.sum(cf / (1 + y) ** t)
    else:
        return np.sum(cf / (1 + y[:, np.newaxis]) ** t, axis=1)

def macaulay_duration(y, face=FACE, coupon=COUPON, maturity=MATURITY):
    """麦考利久期"""
    t = np.arange(1, maturity + 1)
    cf = np.full(maturity, coupon)
    cf[-1] += face
    pv = np.sum(cf / (1 + y) ** t)
    weighted = np.sum(t * cf / (1 + y) ** t)
    return weighted / pv

def modified_duration(y, mac_dur=None):
    """修正久期"""
    if mac_dur is None:
        mac_dur = macaulay_duration(y)
    return mac_dur / (1 + y)

def convexity(y, face=FACE, coupon=COUPON, maturity=MATURITY):
    """凸性（单位：年的平方）"""
    t = np.arange(1, maturity + 1)
    cf = np.full(maturity, coupon)
    cf[-1] += face
    pv = np.sum(cf / (1 + y) ** t)
    conv = np.sum(t * (t + 1) * cf / (1 + y) ** (t + 2)) / pv
    return conv

# ==================== 关键指标计算 ====================
P0 = bond_price(Y0)
D_mac = macaulay_duration(Y0)
D_mod = modified_duration(Y0, D_mac)
C = convexity(Y0)

print(f"当前收益率: {Y0*100:.2f}%")
print(f"精确价格 P0: {P0:.4f}")
print(f"麦考利久期: {D_mac:.4f} 年")
print(f"修正久期:   {D_mod:.4f}")
print(f"凸性:       {C:.4f} 年²")

# ==================== 一、精确价格-收益率曲线 ====================
y_grid = np.linspace(0.02, 0.09, 300)       # 2% - 9%
P_exact = bond_price(y_grid)

# ==================== 二、近似曲线 ====================
# 一阶久期近似（切线）： P(y) ≈ P0 * (1 - D_mod * (y - Y0))
P_approx1 = P0 * (1 - D_mod * (y_grid - Y0))

# 二阶久期+凸性近似： P(y) ≈ P0 * (1 - D_mod*(y-Y0) + 0.5 * C * (y-Y0)^2)
P_approx2 = P0 * (1 - D_mod * (y_grid - Y0) + 0.5 * C * (y_grid - Y0)**2)

# 根据可调窗口限制近似曲线的显示范围（其余设为 NaN 以免画线）
mask = (y_grid >= Y0 - APPROX_WINDOW) & (y_grid <= Y0 + APPROX_WINDOW)
P_approx1_display = np.where(mask, P_approx1, np.nan)
P_approx2_display = np.where(mask, P_approx2, np.nan)

# ==================== 绘图 ====================
fig, ax = plt.subplots(figsize=(10, 6))

# 精确曲线
ax.plot(y_grid * 100, P_exact, 'b-', linewidth=2, label='精确价格 (Exact)')

# 一阶久期直线（仅在窗口内显示）
ax.plot(y_grid * 100, P_approx1_display, 'r--', linewidth=2, 
        label=f'久期近似 (Duration, ±{APPROX_WINDOW*100:.0f}bp)')

# 久期+凸性曲线（仅在窗口内显示）
ax.plot(y_grid * 100, P_approx2_display, 'g-.', linewidth=2, 
        label=f'久期+凸性近似 (Duration+Convexity, ±{APPROX_WINDOW*100:.0f}bp)')

# 标记当前收益率点
ax.plot(Y0 * 100, P0, 'ko', markersize=8, label=f'当前收益率 ({Y0*100:.1f}%)')

ax.set_xlabel('收益率 (%)', fontsize=12)
ax.set_ylabel('价格', fontsize=12)
ax.set_title('债券价格-收益率曲线', fontsize=14)
ax.legend(fontsize=10)
ax.grid(True, alpha=0.3)
plt.tight_layout()

# 保存图片
figure_path = os.path.abspath('bond_price_curve.png')
fig.savefig(figure_path, dpi=150)
plt.close(fig)   # 释放内存

# ==================== 三、报告收益率上升 100bp 的影响 ====================
y_up = Y0 + DY_REPORT
P_up_exact = bond_price(y_up)
dur_approx_change = -D_mod * DY_REPORT  # 一阶相对变化（小数，下跌为负）

print(f"\n收益率上升 {DY_REPORT*100:.0f} bp: {Y0*100:.2f}% -> {y_up*100:.2f}%")
print(f"精确价格: {P_up_exact:.4f}")
print(f"一阶相对变化 (dP/P): {dur_approx_change:.6f} ({dur_approx_change*100:.4f}%)")

# ==================== 输出结果字典 ====================
result = {
    'price_at_up100bp': round(float(P_up_exact), 6),
    'dur_approx_change_up100bp': round(float(dur_approx_change), 8),
    'figure_path': figure_path
}

print("\n=== 输出字典 ===")
print(result)
