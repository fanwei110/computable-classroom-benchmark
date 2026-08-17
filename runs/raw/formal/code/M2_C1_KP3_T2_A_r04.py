import numpy as np
import matplotlib.pyplot as plt

# 债券参数
FACE = 100.0
COUPON = 4.6
N = 7
Y0 = 0.053            # 初始收益率
Y_CHANGE = 0.01       # 收益率变动幅度（可调参数，100个基点）

# ---------- 计算函数 ----------
def bond_price(y, face, coupon, n):
    """计算债券全价"""
    cashflows = np.full(n, coupon)
    cashflows[-1] += face
    t = np.arange(1, n + 1)
    return np.sum(cashflows / (1 + y) ** t)

def bond_duration(y, face, coupon, n):
    """计算麦考利久期和修正久期"""
    cashflows = np.full(n, coupon)
    cashflows[-1] += face
    t = np.arange(1, n + 1)
    pv = cashflows / (1 + y) ** t
    price = np.sum(pv)
    mac_dur = np.sum(t * pv) / price
    mod_dur = mac_dur / (1 + y)
    return mac_dur, mod_dur

# ---------- 计算所需值 ----------
P0 = bond_price(Y0, FACE, COUPON, N)
_, D_mod = bond_duration(Y0, FACE, COUPON, N)

# 收益率上升 100 bp 后的精确价格
P_up = bond_price(Y0 + Y_CHANGE, FACE, COUPON, N)

# 久期近似的相对价格变化（小数形式）
dur_approx_change = -D_mod * Y_CHANGE

# ---------- 画图 ----------
y_range = np.linspace(0.02, 0.09, 200)
exact_prices = [bond_price(y, FACE, COUPON, N) for y in y_range]
approx_prices = P0 - P0 * D_mod * (y_range - Y0)

plt.figure(figsize=(9, 5))
plt.plot(y_range, exact_prices, label='Exact Price', linewidth=2)
plt.plot(y_range, approx_prices, label='Duration Approximation',
         linestyle='--', linewidth=2)
plt.axvline(x=Y0, color='gray', linestyle=':', alpha=0.7, label=f'Initial yield = {Y0*100:.2f}%')
plt.axvline(x=Y0 + Y_CHANGE, color='red', linestyle=':', alpha=0.7,
            label=f'Yield + {Y_CHANGE*100:.0f} bp')
plt.xlabel('Yield')
plt.ylabel('Bond Price')
plt.title('Bond Price vs. Yield (Exact and Duration Approximation)')
plt.legend()
plt.grid(alpha=0.3)
plt.tight_layout()

fig_path = 'bond_price_duration.png'
plt.savefig(fig_path, dpi=150)
plt.close()

# ---------- 结果汇总 ----------
result = {
    'price_at_up100bp': P_up,
    'dur_approx_change_up100bp': dur_approx_change,
    'figure_path': fig_path
}

# 打印结果供检查
print(f"初始全价 P0: {P0:.4f}")
print(f"修正久期 D_mod: {D_mod:.4f}")
print(f"收益率上升100bp后精确价格: {P_up:.4f}")
print(f"久期近似相对价格变化: {dur_approx_change:.6f}  ({dur_approx_change*100:.4f}%)")
print(f"图片路径: {fig_path}")
