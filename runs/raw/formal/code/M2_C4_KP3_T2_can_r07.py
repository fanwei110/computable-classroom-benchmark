import numpy as np
import matplotlib.pyplot as plt
import os

# ------------------------------
# 债券参数
# ------------------------------
face_value = 100.0            # 面值
coupon_rate = 0.046           # 票息率（小数）
maturity = 7                  # 年限
coupon = face_value * coupon_rate  # 年票息 = 4.6

current_yield = 0.053         # 当前到期收益率（小数）
yield_shift = 0.01            # 可调的收益率变动幅度（此处为 +100bp）

# 时间索引与现金流（1..7年）
t = np.arange(1, maturity + 1)
cf = np.full(maturity, coupon)
cf[-1] += face_value          # 最后一期归还本金

# ------------------------------
# 定价、久期、凸性函数
# ------------------------------
def bond_price(y):
    """给定收益率 y（年复利），返回债券价格"""
    return np.sum(cf / (1 + y) ** t)

def bond_duration_convexity(y):
    """
    返回 (价格, 麦考利久期, 修正久期, 凸性)
    凸性单位：年的平方
    """
    p = bond_price(y)
    disc = cf / (1 + y) ** t
    mac_dur = np.sum(t * disc) / p
    mod_dur = mac_dur / (1 + y)
    conv = np.sum(t * (t + 1) * cf / (1 + y) ** (t + 2)) / p
    return p, mac_dur, mod_dur, conv

# ------------------------------
# 当前时点的计算
# ------------------------------
P0, mac_dur, mod_dur, conv = bond_duration_convexity(current_yield)

# ------------------------------
# 收益率上升 100bp 后的精确价格及一阶相对变化
# ------------------------------
y_up = current_yield + yield_shift
P_up = bond_price(y_up)                     # 精确价格
dur_approx_change = -mod_dur * yield_shift  # 一阶相对变化（负值）

# ------------------------------
# 绘制精确曲线及近似曲线
# ------------------------------
y_grid = np.linspace(0.02, 0.09, 300)
P_exact = np.array([bond_price(y) for y in y_grid])

# 一阶久期近似：P ≈ P0 * [1 - D_mod * (y - y0)]
P_dur_approx = P0 * (1 - mod_dur * (y_grid - current_yield))

# 久期+凸性近似：P ≈ P0 * [1 - D_mod*(y-y0) + 0.5*Conv*(y-y0)^2]
P_dur_conv_approx = P0 * (1 - mod_dur * (y_grid - current_yield) +
                          0.5 * conv * (y_grid - current_yield)**2)

plt.figure(figsize=(10, 6))
plt.plot(y_grid, P_exact, label='Exact Price', linewidth=2)
plt.plot(y_grid, P_dur_approx, '--', label='Duration Approximation', linewidth=1.5)
plt.plot(y_grid, P_dur_conv_approx, ':', label='Duration+Convexity Approximation', linewidth=1.5)
plt.axvline(x=current_yield, color='gray', linestyle='-.', alpha=0.7,
            label=f'Current Yield ({current_yield*100:.2f}%)')
plt.scatter([current_yield], [P0], color='red', zorder=5)
plt.xlabel('Yield (annual compounding)')
plt.ylabel('Price')
plt.title('Bond Price–Yield Curve')
plt.legend()
plt.grid(alpha=0.3)
plt.tight_layout()

figure_path = 'bond_price_yield.png'
plt.savefig(figure_path, dpi=150)
plt.close()

# ------------------------------
# 结果字典
# ------------------------------
result = {
    'price_at_up100bp': P_up,
    'dur_approx_change_up100bp': dur_approx_change,
    'figure_path': os.path.abspath(figure_path)
}

# 课堂演示时打印查看
print(result)
