import numpy as np
import matplotlib.pyplot as plt

# ============================
# 债券参数（全部可调）
# ============================
FACE = 100.0                # 面值
COUPON_RATE = 0.046         # 票息率（年化）
MATURITY = 7                # 期限（年）
Y0 = 0.053                  # 当前收益率
FREQ = 1                    # 每年付息次数（1 代表年付）
DELTA_Y_DISPLAY = 0.02      # （可调）图形中展示近似有效的变动范围（±）
UP_SHIFT = 0.01             # 上升 100 个基点

# ============================
# 1. 生成现金流
# ============================
periods = np.arange(1, MATURITY + 1)        # 1,2,...,7
coupon = FACE * COUPON_RATE
cash_flows = np.full(MATURITY, coupon)
cash_flows[-1] += FACE                       # 最后一期归还本金

# ============================
# 2. 定价函数（可向量化）
# ============================
def bond_price(ytm):
    """计算给定收益率 ytm（标量或数组）下的债券价格"""
    ytm = np.asarray(ytm)
    # cash_flows[:, None] shape (7,1), ytm shape (n,)
    # 返回每期贴现值的和
    pv = cash_flows[:, None] / (1 + ytm) ** periods[:, None]
    return np.sum(pv, axis=0)

# 5.3% 处的价格与现金流现值
pv0 = cash_flows / (1 + Y0) ** periods
p0 = np.sum(pv0)

# ============================
# 3. 计算久期（麦考利久期 & 修正久期）
# ============================
weights = pv0 / p0
mac_duration = np.sum(periods * weights)        # 麦考利久期
mod_duration = mac_duration / (1 + Y0)          # 修正久期

# ============================
# 4. 精确价格曲线
# ============================
y_grid = np.linspace(0.02, 0.09, 500)          # 2% 到 9%
exact_prices = bond_price(y_grid)

# 久期近似：P_approx(y) = P(y0) * [1 - D_mod * (y - y0)]
approx_prices = p0 * (1 - mod_duration * (y_grid - Y0))

# ============================
# 5. 上升 100 个基点的精确价格与久期估计
# ============================
y_up = Y0 + UP_SHIFT
price_up = bond_price(y_up).item()              # 精确价格（标量）
# 久期估计的相对价格变化：ΔP/P ≈ -D_mod * Δy
relative_change_approx = -mod_duration * UP_SHIFT

# ============================
# 6. 绘图并保存
# ============================
fig, ax = plt.subplots(figsize=(8, 5))
ax.plot(y_grid * 100, exact_prices, label='Exact Price', linewidth=2)
ax.plot(y_grid * 100, approx_prices, '--', label='Duration Approximation', linewidth=2)

# 标注当前收益率
ax.axvline(x=Y0*100, color='gray', linestyle=':', alpha=0.7)
ax.text(Y0*100 + 0.1, p0, f'Y0={Y0*100:.1f}%', va='bottom', fontsize=9, color='gray')

# 标注 +100bp 的位置
ax.axvline(x=y_up*100, color='red', linestyle=':', alpha=0.5)
ax.axhline(y=price_up, color='red', linestyle=':', alpha=0.5)

# 显示近似有效的可调范围（根据 DELTA_Y_DISPLAY）
ax.axvspan((Y0 - DELTA_Y_DISPLAY)*100, (Y0 + DELTA_Y_DISPLAY)*100,
           alpha=0.1, color='blue', label=f'Adjustable range (±{DELTA_Y_DISPLAY*100:.0f}bp)')

ax.set_xlabel('Yield to Maturity (%)')
ax.set_ylabel('Bond Price')
ax.set_title('Bond Price vs Yield : Exact vs Duration-Based Approximation')
ax.legend()
ax.grid(True, alpha=0.3)

figure_path = 'bond_duration_convexity.png'
fig.savefig(figure_path, dpi=150)
plt.close(fig)

# ============================
# 7. 填充输出字典
# ============================
result = {
    'price_at_up100bp': round(price_up, 6),
    'dur_approx_change_up100bp': round(relative_change_approx, 6),
    'figure_path': figure_path
}

# 打印结果，便于课堂查看
print("===== Bond Duration & Convexity Demo =====")
print(f"面值={FACE}, 票息率={COUPON_RATE*100}%, 期限={MATURITY}年")
print(f"当前收益率 Y0={Y0*100}%")
print(f"当前价格 P0 = {p0:.6f}")
print(f"麦考利久期 = {mac_duration:.4f} 年")
print(f"修正久期   = {mod_duration:.4f}")
print()
print(f"收益率上升 100bp 后 (y={y_up*100}%)：")
print(f"  精确价格                 = {price_up:.6f}")
print(f"  久期估计的相对价格变化   = {relative_change_approx:.6f} ({relative_change_approx*100:.4f}%)")
print()
print("结果字典 result:")
print(result)
