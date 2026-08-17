import numpy as np
import matplotlib.pyplot as plt

# 参数设定（可调）
dy = 0.01  # 收益率变动幅度（100bp）
y0 = 0.053
face = 100
coupon = 4.6
T = 7
freq = 1  # 年付息

# ---- 价格计算函数 ----
def bond_price(ytm):
    """年复利下的全价"""
    t = np.arange(1, T + 1)
    cf = np.full(T, coupon)
    cf[-1] += face
    pv = cf / (1 + ytm) ** t
    return pv.sum()

# ---- 精确价格与久期 ----
P0 = bond_price(y0)

# 麦考利久期
t = np.arange(1, T + 1)
cf = np.full(T, coupon)
cf[-1] += face
pv = cf / (1 + y0) ** t
D_mac = np.sum(t * pv) / P0
D_mod = D_mac / (1 + y0)

# 收益率上升100bp
P_up = bond_price(y0 + dy)

# 久期近似的相对价格变化
approx_change = -D_mod * dy

# ---- 画图 ----
y_range = np.linspace(0.02, 0.09, 200)
P_exact = [bond_price(y) for y in y_range]
P_tangent = P0 - P0 * D_mod * (y_range - y0)  # 切线

plt.figure(figsize=(8, 5))
plt.plot(y_range, P_exact, label='Exact Price', color='steelblue')
plt.plot(y_range, P_tangent, '--', label='Duration Approx. (Tangent)', color='darkorange')
plt.axvline(y0, linestyle=':', color='grey', alpha=0.7)
plt.axvline(y0 + dy, linestyle=':', color='grey', alpha=0.7)
plt.xlabel('Yield')
plt.ylabel('Price')
plt.title('Price–Yield Curve (7Y, 4.6% Coupon)')
plt.legend()
plt.tight_layout()

fig_path = 'price_yield_curve.png'
plt.savefig(fig_path)
plt.close()

# ---- 结果 ----
result = {
    'price_at_up100bp': round(P_up, 4),
    'dur_approx_change_up100bp': round(approx_change, 6),
    'figure_path': fig_path
}

# 打印查看
print(result)
