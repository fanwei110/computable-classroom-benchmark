import numpy as np
import matplotlib.pyplot as plt

# ============================================================
# 债券参数 (可根据需要调整)
# ============================================================
face_value = 100.0          # 面值
coupon_rate = 0.046         # 票息率 (4.6%)
maturity = 7                # 年限 (年)
y0 = 0.053                  # 当前到期收益率 (5.3%)

# ============================================================
# 现金流设置 (每年付息一次)
# ============================================================
t = np.arange(1, maturity + 1)               # 现金流时间点 (1..7)
coupon = face_value * coupon_rate            # 每年票息
cash_flows = np.full(maturity, coupon)       # 前6年只付利息
cash_flows[-1] += face_value                 # 最后一年加上本金

# ============================================================
# 计算当前价格、久期与凸性 (按课程公式)
# ============================================================
# 各期现金流现值
pv = cash_flows / (1 + y0) ** t
P0 = np.sum(pv)                              # 当前价格

# 麦考利久期
D_mac = np.sum(t * pv) / P0

# 修正久期
D_mod = D_mac / (1 + y0)

# 凸性 (单位: 年的平方)
# 公式: Conv = Σ[t(t+1) * CF_t / (1+y)^(t+2)] / P
conv = np.sum(t * (t + 1) * pv) / (P0 * (1 + y0) ** 2)

# ============================================================
# 收益率网格: 2% ~ 9%
# ============================================================
y_grid = np.linspace(0.02, 0.09, 500)

# 精确价格曲线
price_exact = np.sum(cash_flows / (1 + y_grid[:, np.newaxis]) ** t, axis=1)

# 一阶近似 (仅久期)
price_dur = P0 - D_mod * P0 * (y_grid - y0)

# 二阶近似 (久期 + 凸性)
price_dur_conv = (P0
                  - D_mod * P0 * (y_grid - y0)
                  + 0.5 * conv * P0 * (y_grid - y0) ** 2)

# ============================================================
# 收益率变动幅度 (可调参数)
# ============================================================
YIELD_SHIFT = 0.01          # +100bp = 0.01，可根据需要调整
y_up = y0 + YIELD_SHIFT

# 精确价格 (收益率上升100bp后)
price_up = np.sum(cash_flows / (1 + y_up) ** t)

# 久期法估计的一阶相对价格变化 (小数，下跌为负)
dur_approx_change = -D_mod * YIELD_SHIFT

# ============================================================
# 绘图并保存
# ============================================================
plt.figure(figsize=(10, 6))

plt.plot(y_grid * 100, price_exact, label='精确价格', linewidth=2)
plt.plot(y_grid * 100, price_dur, '--', label='久期一阶近似', linewidth=1.5)
plt.plot(y_grid * 100, price_dur_conv, ':', label='久期+凸性近似', linewidth=1.5)

# 标记当前收益率和上升100bp后的位置
plt.axvline(y0 * 100, color='gray', linestyle='-.', alpha=0.7,
            label=f'当前收益率 {y0*100:.1f}%')
plt.axvline(y_up * 100, color='red', linestyle='-.', alpha=0.7,
            label=f'上升100bp: {y_up*100:.1f}%')

plt.xlabel('收益率 (%)')
plt.ylabel('价格')
plt.title('债券价格-收益率曲线及近似 (面值100, 票息4.6%, 7年期)')
plt.legend()
plt.grid(True, alpha=0.3)
plt.tight_layout()

# 保存图形
fig_path = 'bond_price_yield.png'
plt.savefig(fig_path, dpi=150)
plt.show()

# ============================================================
# 输出结果字典
# ============================================================
result = {
    'price_at_up100bp': price_up,
    'dur_approx_change_up100bp': dur_approx_change,
    'figure_path': fig_path
}

print("===== 计算结果 =====")
print(f"当前收益率: {y0*100:.2f}%")
print(f"当前债券价格: {P0:.4f}")
print(f"麦考利久期: {D_mac:.4f} 年")
print(f"修正久期: {D_mod:.4f}")
print(f"凸性: {conv:.4f} 年²")
print(f"\n收益率上升 100bp 后:")
print(f"  精确价格: {price_up:.4f}")
print(f"  久期一阶相对变化 (小数): {dur_approx_change:.6f} ({dur_approx_change*100:.4f}%)")
print(f"\n图形已保存至: {fig_path}")
print("\n===== 结果字典 =====")
print(result)
