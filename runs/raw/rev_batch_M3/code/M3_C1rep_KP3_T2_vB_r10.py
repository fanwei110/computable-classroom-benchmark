import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider

# ============================================================
# 债券参数
# ============================================================
F = 100           # 面值
c_rate = 0.046    # 票息率
n = 7             # 期限（年）
y0 = 0.053        # 当前到期收益率

# ============================================================
# 债券计算函数
# ============================================================
def bond_price(y, F=F, c_rate=c_rate, n=n):
    """精确债券价格（年付息，年复利）"""
    coupon = F * c_rate
    if abs(y) < 1e-12:
        return coupon * n + F
    pv_coupons = coupon * (1 - (1 + y)**(-n)) / y
    pv_face = F * (1 + y)**(-n)
    return pv_coupons + pv_face

def macaulay_duration(y, F=F, c_rate=c_rate, n=n):
    """Macaulay久期"""
    P = bond_price(y, F, c_rate, n)
    coupon = F * c_rate
    total = 0.0
    for t in range(1, n + 1):
        total += t * coupon / (1 + y)**t
    total += n * F / (1 + y)**n
    return total / P

def modified_duration(y, F=F, c_rate=c_rate, n=n):
    """修正久期"""
    return macaulay_duration(y, F, c_rate, n) / (1 + y)

def convexity(y, F=F, c_rate=c_rate, n=n):
    """凸性"""
    P = bond_price(y, F, c_rate, n)
    coupon = F * c_rate
    total = 0.0
    for t in range(1, n + 1):
        total += t * (t + 1) * coupon / (1 + y)**(t + 2)
    total += n * (n + 1) * F / (1 + y)**(n + 2)
    return total / P

# ============================================================
# 当前值计算
# ============================================================
P0 = bond_price(y0)
D_mac = macaulay_duration(y0)
MD = modified_duration(y0)
Conv = convexity(y0)

print(f"当前价格 P0 = {P0:.6f}")
print(f"Macaulay久期 D = {D_mac:.6f}")
print(f"修正久期 MD = {MD:.6f}")
print(f"凸性 Conv = {Conv:.6f}")

# ============================================================
# 收益率范围与曲线
# ============================================================
yields = np.linspace(0.02, 0.09, 1000)
exact_prices = np.array([bond_price(y) for y in yields])
approx_prices = P0 * (1 - MD * (yields - y0))

# ============================================================
# +100bp 关键结果
# ============================================================
delta_y_100bp = 0.01
y_up = y0 + delta_y_100bp
price_at_up100bp = bond_price(y_up)
dur_approx_rel_change_up100bp = -MD * delta_y_100bp
price_dur_approx_100bp = P0 * (1 + dur_approx_rel_change_up100bp)

print(f"\n收益率+100bp后:")
print(f"  精确价格 = {price_at_up100bp:.6f}")
print(f"  久期法相对变化 = {dur_approx_rel_change_up100bp:.6f} ({dur_approx_rel_change_up100bp*100:.4f}%)")
print(f"  久期法近似价格 = {price_dur_approx_100bp:.6f}")

# ============================================================
# 绘图
# ============================================================
fig, ax = plt.subplots(figsize=(14, 9))
plt.subplots_adjust(bottom=0.22, left=0.08, right=0.95, top=0.93)

# 精确价格-收益率曲线
ax.plot(yields * 100, exact_prices, 'b-', linewidth=2.5,
        label='精确价格 (Exact Price)', zorder=3)

# 久期近似（切线）
ax.plot(yields * 100, approx_prices, 'r--', linewidth=2,
        label='久期近似 (Duration Approx)', alpha=0.85, zorder=3)

# 当前YTM点
ax.plot(y0 * 100, P0, 'ko', markersize=10, zorder=6)
ax.annotate(f'YTM={y0*100:.1f}%\nP₀={P0:.2f}',
            xy=(y0*100, P0), xytext=(y0*100 - 2.2, P0 + 5),
            fontsize=10, fontweight='bold',
            arrowprops=dict(arrowstyle='->', color='black', lw=1.5),
            bbox=dict(boxstyle='round,pad=0.3', facecolor='lightyellow', alpha=0.9))

# +100bp 标记
ax.plot(y_up * 100, price_at_up100bp, 'g^', markersize=13, zorder=6,
        label=f'YTM+100bp 精确={price_at_up100bp:.4f}')
ax.plot(y_up * 100, price_dur_approx_100bp, 'rs', markersize=11, zorder=6,
        label=f'YTM+100bp 久期近似={price_dur_approx_100bp:.4f}')

# +100bp处精确与近似的连线
ax.plot([y_up*100, y_up*100], [price_at_up100bp, price_dur_approx_100bp],
        'g-', linewidth=2, alpha=0.7, zorder=5)

# 水平参考线
ax.plot([y0*100, y_up*100], [price_at_up100bp, price_at_up100bp],
        'g:', linewidth=1, alpha=0.5)
ax.plot([y0*100, y_up*100], [price_dur_approx_100bp, price_dur_approx_100bp],
        'r:', linewidth=1, alpha=0.5)

# 信息框
info = (
    f'面值={F}  票息={c_rate*100}%  期限={n}年  YTM={y0*100}%\n'
    f'P₀={P0:.4f}  D_mac={D_mac:.4f}  MD={MD:.4f}  Conv={Conv:.4f}\n'
    f'──────────────────────────────\n'
    f'YTM+100bp → 精确价格 = {price_at_up100bp:.4f}\n'
    f'久期法相对变化 = {dur_approx_rel_change_up100bp*100:.4f}%\n'
    f'久期法近似价格 = {price_dur_approx_100bp:.4f}\n'
    f'误差 = {price_dur_approx_100bp-price_at_up100bp:.4f} '
    f'({(price_dur_approx_100bp-price_at_up100bp)/price_at_up100bp*100:.4f}%)\n'
    f'(凸性修正: +0.5×Conv×Δy² = {0.5*Conv*0.01**2*100:.4f}%)'
)
ax.text(0.02, 0.02, info, transform=ax.transAxes, fontsize=10,
        verticalalignment='bottom', fontfamily='monospace',
        bbox=dict(boxstyle='round', facecolor='lightyellow', alpha=0.9, edgecolor='gray'))

ax.set_xlabel('收益率 Yield (%)', fontsize=14)
ax.set_ylabel('价格 Price', fontsize=14)
ax.set_title('债券价格-收益率曲线 (精确 vs 久期近似)', fontsize=15, fontweight='bold')
ax.legend(loc='upper right', fontsize=11, framealpha=0.9)
ax.grid(True, alpha=0.3)
ax.set_xlim(2, 9)
ax.set_ylim(70, 130)

# ============================================================
# 变动幅度可调滑块
# ============================================================
ax_slider = plt.axes([0.2, 0.06, 0.6, 0.03])
slider = Slider(ax_slider, 'Δy (bp)', -330, 370, valinit=100, valstep=5,
                color='lightblue')

# 动态元素
marker_exact, = ax.plot([], [], 'g^', markersize=13, zorder=7)
marker_approx, = ax.plot([], [], 'rs', markersize=11, zorder=7)
vline_dyn, = ax.plot([], [], 'g-', linewidth=2, alpha=0.7, zorder=5)
axvline_dyn, = ax.plot([], [], color='gray', linestyle=':', alpha=0.3, zorder=2)

slider_text = ax.text(0.98, 0.98, '', transform=ax.transAxes, fontsize=10,
                       verticalalignment='top', horizontalalignment='right',
                       bbox=dict(boxstyle='round', facecolor='lightcyan', alpha=0.9,
                                 edgecolor='steelblue'))

def update(val):
    delta_y = slider.val / 10000
    y_new = y0 + delta_y

    if y_new < 0.02 or y_new > 0.09:
        slider_text.set_text('超出收益率范围 [2%, 9%]')
        for obj in [marker_exact, marker_approx, vline_dyn, axvline_dyn]:
            obj.set_data([], [])
        fig.canvas.draw_idle()
        return

    p_exact = bond_price(y_new)
    dur_rel = -MD * delta_y
    p_approx = P0 * (1 + dur_rel)

    marker_exact.set_data([y_new * 100], [p_exact])
    marker_approx.set_data([y_new * 100], [p_approx])
    vline_dyn.set_data([y_new*100, y_new*100], [p_exact, p_approx])
    axvline_dyn.set_data([y_new*100, y_new*100], [70, 130])

    slider_text.set_text(
        f'Δy = {delta_y*10000:.0f}bp → YTM = {y_new*100:.2f}%\n'
        f'精确价格 = {p_exact:.4f}\n'
        f'久期近似价格 = {p_approx:.4f}\n'
        f'久期法相对变化 = {dur_rel*100:.4f}%\n'
        f'误差 = {p_approx - p_exact:.4f} ({(p_approx-p_exact)/p_exact*100:.4f}%)'
    )
    fig.canvas.draw_idle()

slider.on_changed(update)
update(100)

# 保存图片
plt.savefig('price_yield_curve.png', dpi=150, bbox_inches='tight')
plt.close()

# ============================================================
# 结果字典
# ============================================================
result = {
    'price_at_up100bp': round(price_at_up100bp, 4),
    'dur_approx_change_up100bp': round(dur_approx_rel_change_up100bp, 4),
    'figure_path': 'price_yield_curve.png'
}

print(f"\nResult: {result}")
