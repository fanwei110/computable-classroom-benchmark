import numpy as np
import matplotlib.pyplot as plt

# ==========================================
# 债券参数与假设
# ==========================================
FV = 100                  # 面值
coupon_rate = 0.046       # 票息率
C = FV * coupon_rate      # 每期票息
T = 7                     # 期限（年）
y0 = 0.053                # 当前收益率

# 假设：票息按年支付，现金流发生在每年末
# 收益率变动幅度（可调参数）
dy = 0.01                 # 100个基点 = 1% = 0.01

# ==========================================
# 1. 在 2% 到 9% 的收益率网格上为精确曲线定价
# ==========================================
y_min, y_max = 0.02, 0.09
yields = np.linspace(y_min, y_max, 500)
t = np.arange(1, T + 1)

# 利用广播机制计算精确价格
# yields[:, None] 维度为 (500, 1), t 维度为 (7,)
# (1 + yields[:, None])**t 维度为 (500, 7)
exact_prices = np.sum(C / (1 + yields[:, None])**t, axis=1) + FV / (1 + yields)**T

# ==========================================
# 2. 在 5.3% 附近叠加基于久期的近似
# ==========================================
# 计算当前收益率 y0 下的精确价格 P0
P0 = np.sum(C / (1 + y0)**t) + FV / (1 + y0)**T

# 计算 Macaulay 久期
mac_duration = (np.sum(t * C / (1 + y0)**t) + T * FV / (1 + y0)**T) / P0

# 计算修正久期
mod_duration = mac_duration / (1 + y0)

# 久期法一阶近似价格: P(y) ≈ P0 * [1 - ModD * (y - y0)]
approx_prices = P0 * (1 - mod_duration * (yields - y0))

# ==========================================
# 3. 报告 +100bp 的精确价格与久期法估计的相对变化
# ==========================================
y_up = y0 + dy
price_at_up100bp = np.sum(C / (1 + y_up)**t) + FV / (1 + y_up)**T

# 久期法估计的相对价格变化: ΔP/P0 ≈ -ModD * Δy
dur_approx_change_up100bp = -mod_duration * dy

# ==========================================
# 4. 保存图形并填充 result
# ==========================================
plt.figure(figsize=(10, 6))
plt.plot(yields * 100, exact_prices, label='Exact Price-Yield Curve', color='blue', linewidth=2)
plt.plot(yields * 100, approx_prices, label='Duration-based Approximation', color='red', linestyle='--', linewidth=2)

# 标注当前收益率点和+100bp点
plt.axvline(y0 * 100, color='gray', linestyle=':', label=f'Current Yield ({y0*100:.1f}%)')
plt.scatter([y0 * 100], [P0], color='blue', zorder=5)
plt.scatter([y_up * 100], [price_at_up100bp], color='green', zorder=5, label=f'Price at +100bp ({price_at_up100bp:.2f})')

plt.xlabel('Yield to Maturity (%)')
plt.ylabel('Bond Price')
plt.title('Bond Price-Yield Curve and Duration Approximation')
plt.legend()
plt.grid(True, linestyle='--', alpha=0.6)

figure_path = 'bond_price_yield_curve.png'
plt.savefig(figure_path, dpi=300, bbox_inches='tight')
plt.close()

# 构建 result 字典
result = {
    'price_at_up100bp': price_at_up100bp,
    'dur_approx_change_up100bp': dur_approx_change_up100bp,
    'figure_path': figure_path
}

# 以下为控制台输出验证（可选，便于教师投屏展示结果）
print(f"当前收益率下精确价格 P0: {P0:.4f}")
print(f"Macaulay 久期: {mac_duration:.4f}")
print(f"修正久期: {mod_duration:.4f}")
print(f"+100bp后精确价格: {result['price_at_up100bp']:.4f}")
print(f"久期法估计的相对价格变化: {result['dur_approx_change_up100bp']:.4%}")
print(f"图形已保存至: {result['figure_path']}")
