import numpy as np
import matplotlib.pyplot as plt

# 债券参数
face = 100.0
coupon_rate = 0.046
maturity = 7
ytm = 0.053

# 现金流
t = np.arange(1, maturity + 1)
cf = np.full(maturity, face * coupon_rate)
cf[-1] += face

# 债券价格函数
def bond_price(y):
    return np.sum(cf / (1 + y) ** t)

# 麦考利久期和修正久期
P0 = bond_price(ytm)
pv = cf / (1 + ytm) ** t
macaulay_duration = np.sum(t * pv) / P0
modified_duration = macaulay_duration / (1 + ytm)

# 收益率上升100个基点的精确价格
dy = 0.01
y_up = ytm + dy
P_up = bond_price(y_up)

# 用久期估算的相对价格变化（小数形式）
dur_approx_change = -modified_duration * dy

# 绘图：收益率从2%到9%
y_range = np.linspace(0.02, 0.09, 200)
P_exact = bond_price(y_range)
# 久期近似（切线）
P_approx = P0 - P0 * modified_duration * (y_range - ytm)

plt.figure(figsize=(8, 5))
plt.plot(y_range * 100, P_exact, label='精确价格', linewidth=2)
plt.plot(y_range * 100, P_approx, '--', label='久期近似', linewidth=2)
plt.axvline(ytm * 100, color='gray', linestyle=':', alpha=0.7)
plt.xlabel('收益率 (%)')
plt.ylabel('价格')
plt.title('债券价格随收益率变化')
plt.legend()
plt.grid(True, alpha=0.3)

# 保存图片
fig_path = 'price_yield_curve.png'
plt.savefig(fig_path)
plt.close()

# 结果字典
result = {
    'price_at_up100bp': round(P_up, 6),           # 精确价格
    'dur_approx_change_up100bp': round(dur_approx_change, 6),  # 久期估计的相对变化
    'figure_path': fig_path                       # 图片路径
}

print(result)
