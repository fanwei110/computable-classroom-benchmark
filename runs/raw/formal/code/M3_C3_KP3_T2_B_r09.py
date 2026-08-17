import numpy as np
import matplotlib.pyplot as plt

# ============================================================
# 债券参数
# ============================================================
F       = 100          # 面值
c_rate  = 0.046        # 票息率（小数）
C       = F * c_rate   # 年票息额 = 4.6
n       = 7            # 期限（年）
y0      = 0.053        # 当前到期收益率（小数）

# ============================================================
# 可调参数 — 变动幅度（可自行修改以观察不同幅度）
# ============================================================
delta_y = 0.01          # 收益率变动幅度，默认 100bp

# ============================================================
# 收益率绘图范围
# ============================================================
y_min = 0.02            # 下限（小数）
y_max = 0.09            # 上限（小数）

# ============================================================
# 核心函数（年复利报价）
# ============================================================
def bond_price(y, C, F, n):
    """年复利下债券精确价格"""
    if abs(y) < 1e-12:
        return C * n + F
    return C * (1 - (1 + y)**(-n)) / y + F * (1 + y)**(-n)

def mac_duration(y, C, F, n):
    """Macaulay 久期"""
    P = bond_price(y, C, F, n)
    wsum = sum(t * C / (1 + y)**t for t in range(1, n + 1))
    wsum += n * F / (1 + y)**n
    return wsum / P

def mod_duration(y, C, F, n):
    """修正久期 = Macaulay / (1+y)"""
    return mac_duration(y, C, F, n) / (1 + y)

# ============================================================
# 当前基准
# ============================================================
P0      = bond_price(y0, C, F, n)
D_mac0  = mac_duration(y0, C, F, n)
D_mod0  = mod_duration(y0, C, F, n)

# ============================================================
# +100bp 后精确价格 & 久期法估计相对变化
# ============================================================
y_up                     = y0 + 0.01
price_at_up100bp         = bond_price(y_up, C, F, n)
dur_approx_change_up100bp = -D_mod0 * 0.01   # ΔP/P ≈ -D_mod × Δy

# ============================================================
# 绘图：精确价格 vs 久期一阶近似
# ============================================================
y_arr      = np.linspace(y_min, y_max, 1000)
exact_arr  = np.array([bond_price(y, C, F, n) for y in y_arr])
approx_arr = P0 * (1 - D_mod0 * (y_arr - y0))

plt.rcParams['font.sans-serif'] = [
    'SimHei', 'Microsoft YaHei', 'STSong',
    'Arial Unicode MS', 'DejaVu Sans'
]
plt.rcParams['axes.unicode_minus'] = False

fig, ax = plt.subplots(figsize=(10, 6.5))

# 精确价格曲线
ax.plot(y_arr * 100, exact_arr,  'b-',  lw=2.2, label='精确价格')
# 久期近似曲线（在 y0 处的一阶 Taylor 展开）
ax.plot(y_arr * 100, approx_arr, 'r--', lw=2.2, label='久期近似价格')

# 当前 YTM 竖线
ax.axvline(y0 * 100, color='gray', ls=':', alpha=0.6,
           label=f'当前 YTM = {y0*100:.1f}%')

# 当前价格点
ax.scatter([y0 * 100], [P0], color='k', s=80, zorder=5,
           label=f'当前价格 = {P0:.4f}')

# +100bp 精确价格点
ax.scatter([y_up * 100], [price_at_up100bp], color='green',
           s=80, zorder=5, marker='v',
           label=f'+100bp 精确价格 = {price_at_up100bp:.4f}')

# +100bp 久期近似价格点
approx_price_up = P0 * (1 + dur_approx_change_up100bp)
ax.scatter([y_up * 100], [approx_price_up], color='red',
           s=80, zorder=5, marker='^',
           label=f'+100bp 久期近似价格 = {approx_price_up:.4f}')

ax.set_xlabel('收益率 (%)', fontsize=13)
ax.set_ylabel('价格', fontsize=13)
ax.set_title(
    f'价格-收益率曲线  |  面值 {F}  票息 {c_rate*100}%  '
    f'期限 {n} 年  当前 YTM {y0*100}%',
    fontsize=13
)
ax.legend(fontsize=10, loc='upper right')
ax.grid(True, alpha=0.3)

fig_path = 'price_yield_curve.png'
fig.savefig(fig_path, dpi=150, bbox_inches='tight')
plt.close()

# ============================================================
# 输出
# ============================================================
result = {
    'price_at_up100bp': round(price_at_up100bp, 6),
    'dur_approx_change_up100bp': round(dur_approx_change_up100bp, 6),
    'figure_path': fig_path
}

print("=== 计算验证 ===")
print(f"当前价格 P0                = {P0:.6f}")
print(f"Macaulay 久期              = {D_mac0:.6f} 年")
print(f"修正久期 D_mod             = {D_mod0:.6f}")
print(f"+100bp 后精确价格          = {price_at_up100bp:.6f}")
print(f"久期法估计相对变化 ΔP/P    = {dur_approx_change_up100bp:.6f}  ({dur_approx_change_up100bp*100:.4f}%)")
actual_rel = (price_at_up100bp - P0) / P0
print(f"实际相对变化 ΔP/P          = {actual_rel:.6f}  ({actual_rel*100:.4f}%)")
print(f"\nresult = {result}")
