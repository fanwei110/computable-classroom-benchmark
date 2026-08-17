import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import PercentFormatter

# 债券参数
face_value = 100.0
coupon_rate = 0.046
maturity = 7
y0 = 0.053
coupon = face_value * coupon_rate

# 精确价格函数（年复利）
def bond_price(ytm):
    t = np.arange(1, maturity + 1)
    cf = np.full(maturity, coupon)
    cf[-1] += face_value
    pv = np.sum(cf / (1 + ytm) ** t)
    return pv

P0 = bond_price(y0)
print(f"P0 = {P0:.4f}")

# 收益率上升100bp
delta_y = 0.01
y_up = y0 + delta_y
P_up = bond_price(y_up)
print(f"精确价格 (y+100bp) = {P_up:.4f}")

# 麦考利久期与修正久期
def macaulay_duration(ytm):
    t = np.arange(1, maturity + 1)
    cf = np.full(maturity, coupon)
    cf[-1] += face_value
    pv = cf / (1 + ytm) ** t
    price = np.sum(pv)
    mac_d = np.sum(t * pv) / price
    return mac_d, price

mac_d, _ = macaulay_duration(y0)
mod_d = mac_d / (1 + y0)
print(f"麦考利久期 = {mac_d:.4f}, 修正久期 = {mod_d:.4f}")

# 久期近似相对价格变化
approx_relative_change = -mod_d * delta_y
print(f"久期近似相对价格变化 = {approx_relative_change:.6f}")

# 真实相对变化
exact_relative_change = (P_up - P0) / P0
print(f"精确相对价格变化 = {exact_relative_change:.6f}")

# 画图 --------------------------------------------------------
y_range = np.linspace(0.02, 0.09, 200)
exact_prices = [bond_price(y) for y in y_range]

# 久期近似直线: P_approx = P0 * (1 - mod_d * (y - y0))
approx_prices = P0 * (1 - mod_d * (y_range - y0))

# 可调的收益率变动幅度，用于在图上示意
plot_delta_y = 0.01  # 可调整参数
y_demo = y0 + plot_delta_y
P_demo_exact = bond_price(y_demo)
P_demo_approx = P0 * (1 - mod_d * plot_delta_y)

plt.figure(figsize=(10, 6))
plt.plot(y_range, exact_prices, label='Exact Price', linewidth=2)
plt.plot(y_range, approx_prices, '--', label='Duration Approximation', linewidth=2)

# 标注具体变动
plt.axvline(y0, color='gray', linestyle=':', alpha=0.7)
plt.axvline(y_demo, color='gray', linestyle=':', alpha=0.7)
plt.hlines(P0, 0.02, y0, colors='gray', linestyles=':', alpha=0.5)
plt.hlines(P_demo_exact, 0.02, y_demo, colors='gray', linestyles=':', alpha=0.5)
plt.annotate(f'Exact ΔP/P = {exact_relative_change:.4f}', 
             xy=(y_demo, P_demo_exact), 
             xytext=(y_demo + 0.005, P_demo_exact - 2),
             arrowprops=dict(arrowstyle='->', color='blue'),
             fontsize=10, color='blue')
plt.annotate(f'Approx ΔP/P = {approx_relative_change:.4f}', 
             xy=(y_demo, P_demo_approx), 
             xytext=(y_demo + 0.005, P_demo_approx + 1.5),
             arrowprops=dict(arrowstyle='->', color='red'),
             fontsize=10, color='red')
plt.scatter([y0, y_demo], [P0, P_demo_exact], color='blue', zorder=5)
plt.scatter([y0, y_demo], [P0, P_demo_approx], color='red', zorder=5)

plt.xlabel('Yield to Maturity')
plt.ylabel('Bond Price')
plt.title(f'Bond Price vs Yield (Δy = {plot_delta_y*100:.0f} bp, adjustable)')
plt.legend()
plt.gca().xaxis.set_major_formatter(PercentFormatter(1.0))
plt.gca().yaxis.set_major_formatter(plt.FuncFormatter(lambda x, _: f'{x:.2f}'))
plt.tight_layout()

fig_path = 'price_curve.png'
plt.savefig(fig_path, dpi=150)
plt.close()
print(f"图已保存至 {fig_path}")

# 输出字典
result = {
    'price_at_up100bp': round(P_up, 4),
    'dur_approx_change_up100bp': round(approx_relative_change, 6),
    'figure_path': fig_path
}

print(result)
