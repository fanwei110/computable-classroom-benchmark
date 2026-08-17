import numpy as np
import matplotlib.pyplot as plt

# ---------- 债券参数 ----------
face_value = 100
coupon_rate = 0.046
years = 7
current_yield = 0.053
yield_shift_bps = 100          # 收益率变动幅度（可调参数）
yield_shift = yield_shift_bps / 10000  # 转换为小数

# ---------- 现金流 ----------
t = np.arange(1, years + 1)
coupon = face_value * coupon_rate
cash_flows = np.full(years, coupon)
cash_flows[-1] += face_value  # 最后一期还包括本金

# ---------- 定价函数 ----------
def bond_price(ytm):
    return np.sum(cash_flows / (1 + ytm) ** t)

def bond_macaulay_duration(ytm):
    pv = cash_flows / (1 + ytm) ** t
    price = np.sum(pv)
    mac_dur = np.sum(t * pv) / price
    return mac_dur, price

# ---------- 当前价格与久期 ----------
mac_dur_0, price_0 = bond_macaulay_duration(current_yield)
mod_dur_0 = mac_dur_0 / (1 + current_yield)

# ---------- 100bp 上升后的精确价格 ----------
price_up100bp = bond_price(current_yield + yield_shift)

# ---------- 久期近似的相对价格变化 ----------
dur_approx_change = -mod_dur_0 * yield_shift

# ---------- 绘图 ----------
yields = np.linspace(0.02, 0.09, 300)
exact_prices = [bond_price(y) for y in yields]
# 久期近似切线：P(y) ≈ P0 * (1 - MD * (y - y0))
approx_prices = price_0 * (1 - mod_dur_0 * (yields - current_yield))

plt.figure(figsize=(10, 6))
plt.plot(yields * 100, exact_prices, label='精确价格', linewidth=2)
plt.plot(yields * 100, approx_prices, '--', label='久期近似 (切线)', linewidth=2)

# 标记当前收益率和变化后的点
shifted_yield = (current_yield + yield_shift) * 100
plt.axvline(current_yield * 100, color='gray', linestyle=':', alpha=0.7)
plt.axvline(shifted_yield, color='red', linestyle=':', alpha=0.7)
plt.scatter([current_yield * 100, shifted_yield],
            [price_0, price_up100bp],
            color=['black', 'red'], zorder=5)
plt.annotate(f'收益率 +{yield_shift_bps} bp\n精确价格: {price_up100bp:.4f}',
             xy=(shifted_yield, price_up100bp),
             xytext=(shifted_yield + 0.5, price_up100bp - 1),
             arrowprops=dict(arrowstyle="->", color='red'),
             fontsize=9, color='red')

plt.xlabel('到期收益率 (%)')
plt.ylabel('债券价格')
plt.title(f'价格-收益率曲线 (当前收益率 = {current_yield*100:.2f}%)')
plt.legend()
plt.grid(alpha=0.3)
plt.tight_layout()

# ---------- 保存图像 ----------
figure_path = 'price_yield_curve.png'
plt.savefig(figure_path, dpi=150)
plt.show()

# ---------- 构建结果字典 ----------
result = {
    'price_at_up100bp': round(price_up100bp, 6),
    'dur_approx_change_up100bp': round(dur_approx_change, 6),
    'figure_path': figure_path
}

print(result)
