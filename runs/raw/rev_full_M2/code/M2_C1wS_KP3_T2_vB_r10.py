import numpy as np
import matplotlib.pyplot as plt

# =============================================================================
# 债券参数
# =============================================================================
face_value = 100.0          # 面值
coupon_rate = 0.046         # 票息率 4.6%
maturity = 7                # 剩余年限 7 年
ytm0 = 0.053                # 当前到期收益率 5.3%
shift_bp = 100              # 收益率变动幅度，单位 bp (可调)
delta_y = shift_bp / 10000.0  # 转换为小数

# 现金流向：每年付息一次，最后一年归还本金
coupon = face_value * coupon_rate
t = np.arange(1, maturity + 1)
cashflows = np.full_like(t, coupon, dtype=float)
cashflows[-1] += face_value  # 最后一年加上本金

# =============================================================================
# 1. 精确价格计算 (支持标量或数组收益率)
# =============================================================================
def exact_price(y):
    """计算任意收益率 y (可数组) 下的精确债券价格"""
    y = np.asarray(y)
    # 对于每个收益率，贴现求和；利用广播
    # (n_times,) 与 (n_y,) 或标量
    discount_factors = (1 + y) ** (-t.reshape(-1, 1) if y.ndim > 0 else -t)
    prices = np.sum(cashflows.reshape(-1, 1) * discount_factors, axis=0) if y.ndim > 0 else np.sum(cashflows * discount_factors)
    return prices

# 当前价格
P0 = exact_price(ytm0)

# =============================================================================
# 2. 久期与凸性 (基于当前收益率)
# =============================================================================
# 麦考利久期
discount_cf = cashflows / (1 + ytm0) ** t
D_mac = np.sum(t * discount_cf) / P0

# 修正久期
D_mod = D_mac / (1 + ytm0)

# 凸性 (如需也可计算，本题仅用久期)
# C = np.sum(t * (t + 1) * discount_cf) / (P0 * (1 + ytm0)**2)

# =============================================================================
# 3. 构建收益率网格并计算曲线
# =============================================================================
y_grid = np.linspace(0.02, 0.09, 500)   # 2% 到 9%
P_exact_grid = exact_price(y_grid)

# 久期近似直线：P(y) ≈ P0 * (1 - D_mod * (y - ytm0))
P_dur_grid = P0 * (1 - D_mod * (y_grid - ytm0))

# =============================================================================
# 4. 计算 +100bp 后的精确价格与久期估计的相对变化
# =============================================================================
y_up = ytm0 + delta_y
P_up_exact = exact_price(y_up).item()   # 精确价格
dur_relative_change = -D_mod * delta_y   # 久期法相对变化 (比例, 负值表示价格下跌)

# =============================================================================
# 5. 绘图
# =============================================================================
fig, ax = plt.subplots(figsize=(10, 6))
ax.plot(y_grid * 100, P_exact_grid, label='精确价格曲线', linewidth=2)
ax.plot(y_grid * 100, P_dur_grid, '--', label='久期近似 (切线)', linewidth=2)
ax.axvline(ytm0 * 100, color='gray', linestyle=':', alpha=0.7, label=f'当前YTM={ytm0*100:.2f}%')
ax.axvline(y_up * 100, color='red', linestyle=':', alpha=0.7, label=f'变动后YTM={y_up*100:.2f}%')
ax.set_xlabel('到期收益率 (%)')
ax.set_ylabel('债券价格')
ax.set_title(f'债券价格-收益率曲线 (面值={face_value}, 票息={coupon_rate*100}%, 期限={maturity}年)')
ax.legend()
ax.grid(True, alpha=0.3)
plt.tight_layout()

figure_path = 'bond_price_yield_curve.png'
fig.savefig(figure_path, dpi=150)
plt.close(fig)

# =============================================================================
# 6. 输出结果字典
# =============================================================================
result = {
    'price_at_up100bp': round(P_up_exact, 4),
    'dur_approx_change_up100bp': round(dur_relative_change, 6),
    'figure_path': figure_path
}

# 打印以便课堂查看
print("=== 债券定价与久期分析结果 ===")
print(f"当前收益率 (YTM): {ytm0*100:.2f}%")
print(f"当前价格: {P0:.4f}")
print(f"修正久期: {D_mod:.4f}")
print(f"+{shift_bp}bp 后精确价格: {result['price_at_up100bp']:.4f}")
print(f"久期法估计的相对变化: {result['dur_approx_change_up100bp']:.6f} ({result['dur_approx_change_up100bp']*100:.4f}%)")
print(f"图表已保存至: {figure_path}")
