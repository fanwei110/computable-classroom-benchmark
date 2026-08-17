import numpy as np
import matplotlib.pyplot as plt

# 债券参数
FACE = 100.0
COUPON = 4.6
MATURITY = 7
YIELD0 = 0.053  # 当前收益率（小数）

# 收益率变动（可调参数）
DY = 0.01  # 100个基点

# ----- 定价函数（年复利）-----
def bond_price(y):
    t = np.arange(1, MATURITY + 1)
    pv_coupons = COUPON / (1 + y) ** t
    pv_face = FACE / (1 + y) ** MATURITY
    return np.sum(pv_coupons) + pv_face

# ----- 当前价格 -----
P0 = bond_price(YIELD0)

# ----- 麦考利久期与修正久期 -----
t = np.arange(1, MATURITY + 1)
pv_coupons = COUPON / (1 + YIELD0) ** t
pv_face = FACE / (1 + YIELD0) ** MATURITY
weights = (t * pv_coupons).sum() + MATURITY * pv_face
D_mac = weights / P0          # 麦考利久期
D_mod = D_mac / (1 + YIELD0)  # 修正久期

# ----- 要求：收益率上升100bp后的精确价格 -----
P_up = bond_price(YIELD0 + DY)

# ----- 久期近似的相对价格变化（修正久期法）-----
delta_approx = -D_mod * DY

# ----- 结果字典 -----
result = {
    'price_at_up100bp': P_up,
    'dur_approx_change_up100bp': delta_approx,
    'figure_path': 'price_duration_curve.png'
}

# ----- 画图 -----
y_range = np.linspace(0.02, 0.09, 300)
prices_exact = [bond_price(y) for y in y_range]
# 久期近似直线：切线在 y=YIELD0 处
prices_approx = P0 * (1 - D_mod * (y_range - YIELD0))

plt.figure(figsize=(8, 5))
plt.plot(y_range * 100, prices_exact, label='Exact Price', linewidth=2)
plt.plot(y_range * 100, prices_approx, '--', label='Duration Approximation', linewidth=2)

# 标注当前点与变动点
plt.axvline(YIELD0 * 100, color='gray', linestyle=':', alpha=0.7)
plt.axvline((YIELD0 + DY) * 100, color='gray', linestyle=':', alpha=0.7)
plt.plot(YIELD0 * 100, P0, 'ko', markersize=6)
plt.plot((YIELD0 + DY) * 100, P_up, 'ro', markersize=6, label=f'Exact at +{DY*100:.0f}bp')
plt.plot((YIELD0 + DY) * 100, P0 * (1 + delta_approx), 'rX', markersize=8,
         label=f'Approx at +{DY*100:.0f}bp')

plt.xlabel('Yield (%)')
plt.ylabel('Price')
plt.title(f'Bond Price vs Yield (dy = {DY*100:.0f}bp)')
plt.legend()
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.savefig(result['figure_path'], dpi=150)
plt.close()

print(result)
