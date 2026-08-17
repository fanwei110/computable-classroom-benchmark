import numpy as np
import matplotlib.pyplot as plt

# ================= 债券参数 =================
F = 100                # 面值
coupon_rate = 0.046    # 票息率 4.6%
T = 7                  # 期限 7 年
y0 = 0.053             # 当前收益率 5.3%
C = F * coupon_rate    # 年票息

# ================= 可调参数 =================
yield_low = 0.02       # 画图收益率下限 2%
yield_high = 0.09      # 画图收益率上限 9%
dy = 0.01              # 收益率变动幅度（100个基点 = 0.01，此参数可调）

# ================= 核心计算函数 =================
def bond_price_vec(y_arr, F, C, T):
    """向量化的债券定价函数：计算不同收益率下的债券价格"""
    y_arr = np.asarray(y_arr).reshape(-1, 1)
    t = np.arange(1, T + 1).reshape(1, -1)
    # 票息贴现
    pv_coupons = C / (1 + y_arr)**t
    # 面值贴现
    pv_face = F / (1 + y_arr)**T
    return np.sum(pv_coupons, axis=1) + pv_face.ravel()

def mac_duration(y, F, C, T):
    """计算麦考利久期"""
    t = np.arange(1, T + 1)
    pv_cashflows = C / (1 + y)**t
    pv_face = F / (1 + y)**T
    pv_cashflows[-1] += pv_face  # 期末现金流包含面值
    price = np.sum(pv_cashflows)
    return np.sum(t * pv_cashflows) / price

def mod_duration(y, F, C, T):
    """计算修正久期"""
    return mac_duration(y, F, C, T) / (1 + y)

# ================= 步骤 1 & 2: 精确曲线与久期近似 =================
# 1. 在 2% 到 9% 的收益率网格上为精确曲线定价
y_grid = np.linspace(yield_low, yield_high, 700)
exact_prices = bond_price_vec(y_grid, F, C, T)

# 当前收益率下的价格与修正久期
P0 = bond_price_vec(np.array([y0]), F, C, T)[0]
ModD_y0 = mod_duration(y0, F, C, T)

# 2. 在当前收益率附近叠加基于久期的近似：P ≈ P0 * (1 - ModD * Δy)
approx_prices = P0 * (1 - ModD_y0 * (y_grid - y0))

# ================= 步骤 3: +100bp 的精确价格与相对变化 =================
# 收益率上升 100 个基点 (由可调参数 dy 决定)
y_up = y0 + dy
P_up = bond_price_vec(np.array([y_up]), F, C, T)[0]
# 久期法估计的相对价格变化
dur_approx_rel_change = -ModD_y0 * dy

# ================= 步骤 4: 保存图形 =================
plt.figure(figsize=(10, 6))
plt.plot(y_grid * 100, exact_prices, label='Exact Price-Yield Curve', color='blue', linewidth=2)
plt.plot(y_grid * 100, approx_prices, label='Duration-Based Approximation', color='red', linestyle='--', linewidth=2)

# 标记当前收益率与变动后的位置
plt.plot(y0 * 100, P0, 'ko', label=f'Current Yield ({y0*100:.1f}%)', markersize=8)
plt.axvline(x=y0 * 100, color='gray', linestyle=':', alpha=0.6)
plt.axvline(x=y_up * 100, color='gray', linestyle=':', alpha=0.6, label=f'+{dy*100:.0f}bp Shift')

plt.xlabel('Yield (%)', fontsize=12)
plt.ylabel('Price', fontsize=12)
plt.title('Bond Price-Yield Curve and Duration Approximation', fontsize=14)
plt.legend(fontsize=11)
plt.grid(True, linestyle='--', alpha=0.6)
plt.xticks(np.arange(2, 9.5, 0.5))

fig_path = 'bond_price_yield_curve.png'
plt.savefig(fig_path, dpi=300, bbox_inches='tight')
plt.close()

# ================= 输出契约 =================
result = {
    'price_at_up100bp': P_up,
    'dur_approx_change_up100bp': dur_approx_rel_change,
    'figure_path': fig_path
}
