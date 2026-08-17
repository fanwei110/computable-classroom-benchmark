import numpy as np
import matplotlib.pyplot as plt

# 债券参数
face_value = 100
coupon_rate = 0.046
coupon = face_value * coupon_rate
n = 7
ytm0 = 0.053

# -------------------- 精确价格计算函数 --------------------
def bond_price(ytm):
    t = np.arange(1, n + 1)
    cashflows = np.full(n, coupon)
    cashflows[-1] += face_value
    pv = cashflows / (1 + ytm) ** t
    return np.sum(pv)

# 初始价格与现金流现值
t = np.arange(1, n + 1)
cashflows = np.full(n, coupon)
cashflows[-1] += face_value
pv0 = cashflows / (1 + ytm0) ** t
P0 = np.sum(pv0)

# 麦考利久期与修正久期
mac_duration = np.sum(t * pv0) / P0
mod_duration = mac_duration / (1 + ytm0)

# -------------------- 收益率 +100bp 计算 --------------------
y_up = ytm0 + 0.01  # +100bp
P_up_exact = bond_price(y_up)

# 久期近似相对变化 (ΔP/P)
approx_relative_change = -mod_duration * 0.01

# -------------------- 画图：价格‑收益率曲线 --------------------
yields = np.linspace(0.02, 0.09, 200)
prices_exact = [bond_price(y) for y in yields]
# 久期近似直线: P(y) ≈ P0 * (1 - D_mod * (y - y0))
prices_approx = P0 * (1 - mod_duration * (yields - ytm0))

plt.figure(figsize=(8, 5))
plt.plot(yields * 100, prices_exact, label='Exact Price', linewidth=2)
plt.plot(yields * 100, prices_approx, '--', label='Duration Approximation', linewidth=2)
plt.axvline(ytm0 * 100, color='gray', linestyle=':', alpha=0.7, label=f'YTM = {ytm0*100}%')
plt.axvline(y_up * 100, color='red', linestyle=':', alpha=0.7, label=f'YTM +100bp = {y_up*100}%')
plt.xlabel('Yield to Maturity (%)')
plt.ylabel('Price')
plt.title('Price-Yield Curve and Duration Approximation')
plt.legend()
plt.grid(True)
plt.tight_layout()

fig_path = 'price_yield_curve.png'
plt.savefig(fig_path)
plt.close()

# -------------------- 结果输出 --------------------
result = {
    'price_at_up100bp': round(P_up_exact, 4),
    'dur_approx_change_up100bp': round(approx_relative_change, 6),
    'figure_path': fig_path
}

result
