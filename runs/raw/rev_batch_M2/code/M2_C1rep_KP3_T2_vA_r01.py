import numpy as np
import matplotlib.pyplot as plt

# 债券参数
face_value = 100
coupon_rate = 0.046
coupon = face_value * coupon_rate
n = 7
y0 = 0.053  # 初始收益率

# ---------- 精确价格计算函数 ----------
def bond_price(y):
    """计算年付息债券的精确价格"""
    pv_annuity = coupon * (1 - (1 + y)**(-n)) / y
    pv_face = face_value * (1 + y)**(-n)
    return pv_annuity + pv_face

P0 = bond_price(y0)

# ---------- 修正久期 ----------
# 现金流现值
pv_cf = [coupon / (1 + y0)**t for t in range(1, n)] + [(coupon + face_value) / (1 + y0)**n]
# 麦考利久期
mac_dur = sum((t+1) * pv_cf[t] for t in range(n)) / P0
modified_dur = mac_dur / (1 + y0)

# 收益率上升100个基点
dy = 0.01
y_up = y0 + dy
P_up = bond_price(y_up)                     # 精确价格
dur_approx_change = -modified_dur * dy      # 久期估算的相对价格变化（小数）

# ---------- 画图 ----------
y_range = np.linspace(0.02, 0.09, 200)      # 2% 到 9%
exact_prices = [bond_price(y) for y in y_range]

# 久期近似价格： P_approx(y) = P0 * (1 - modified_dur * (y - y0))
approx_prices = P0 * (1 - modified_dur * (y_range - y0))

fig, ax = plt.subplots(figsize=(10, 6))
ax.plot(y_range * 100, exact_prices, label='精确价格', linewidth=2)
ax.plot(y_range * 100, approx_prices, '--', label='久期近似 (修正久期)', linewidth=2)
ax.axvline(y0*100, color='gray', linestyle=':', alpha=0.7, label=f'初始收益率 {y0*100:.1f}%')
ax.axvline(y_up*100, color='red', linestyle=':', alpha=0.7, label=f'上升100bp后 {y_up*100:.1f}%')
ax.set_xlabel('收益率 (%)')
ax.set_ylabel('债券价格')
ax.set_title('债券价格随收益率变化曲线 (面值100, 票息4.6%, 7年)')
ax.legend()
ax.grid(True, alpha=0.3)
plt.tight_layout()

figure_path = './price_duration_curve.png'
fig.savefig(figure_path, dpi=150)
plt.close(fig)

# 结果汇总
result = {
    'price_at_up100bp': round(P_up, 6),          # 收益率上升100bp后的精确价格
    'dur_approx_change_up100bp': round(dur_approx_change, 6),  # 久期估算的相对价格变化
    'figure_path': figure_path
}

result
