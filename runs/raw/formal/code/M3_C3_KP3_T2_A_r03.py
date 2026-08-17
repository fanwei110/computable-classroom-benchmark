import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider

# 债券基本参数
F = 100          # 面值
c = 0.046        # 票息率 4.6%
T = 7            # 期限 7年
y0 = 0.053       # 初始收益率 5.3%
coupon = F * c   # 年票息

# 精确价格计算函数（按年复利）
def bond_price(y):
    return sum(coupon / (1 + y)**t for t in range(1, T + 1)) + F / (1 + y)**T

# 麦考利久期计算函数
def mac_duration(y):
    P = bond_price(y)
    w_sum = sum(t * coupon / (1 + y)**t for t in range(1, T + 1)) + T * F / (1 + y)**T
    return w_sum / P

# 初始状态计算
P0 = bond_price(y0)
mac_d = mac_duration(y0)
mod_d = mac_d / (1 + y0)  # 修正久期

# 久期近似价格函数
def approx_price(y):
    dy = y - y0
    return P0 * (1 - mod_d * dy)

# 要求的输出计算：收益率上升100个基点 (1%)
dy_100bp = 0.01
price_at_up100bp = bond_price(y0 + dy_100bp)
dur_approx_change_up100bp = -mod_d * dy_100bp  # 久期估计的相对价格变化

# 生成绘图数据
ys = np.linspace(0.02, 0.09, 500)
exact_prices = [bond_price(y) for y in ys]
approx_prices = [approx_price(y) for y in ys]

# 绘图
fig, ax = plt.subplots(figsize=(10, 6))
plt.subplots_adjust(bottom=0.25)

ax.plot(ys, exact_prices, label='Exact Price', color='blue', linewidth=2)
ax.plot(ys, approx_prices, label='Duration Approximation', color='red', linestyle='--', linewidth=2)

# 初始点标记和垂直参考线
init_dy = 0.0
point_exact, = ax.plot(y0 + init_dy, bond_price(y0 + init_dy), 'bo', markersize=8)
point_approx, = ax.plot(y0 + init_dy, approx_price(y0 + init_dy), 'ro', markersize=8)
vline = ax.axvline(x=y0 + init_dy, color='gray', linestyle=':', linewidth=1)

ax.set_xlabel('Yield')
ax.set_ylabel('Price')
ax.set_title('Bond Price vs Yield with Duration Approximation')
ax.legend()

# 添加可调收益率变动幅度(Δy)的滑块
ax_slider = plt.axes([0.25, 0.1, 0.5, 0.03])
slider = Slider(ax_slider, 'Δy', -0.033, 0.037, valinit=init_dy, valstep=0.0001)

def update(val):
    dy = slider.val
    y_new = y0 + dy
    point_exact.set_xdata([y_new])
    point_exact.set_ydata([bond_price(y_new)])
    point_approx.set_xdata([y_new])
    point_approx.set_ydata([approx_price(y_new)])
    vline.set_xdata([y_new])
    fig.canvas.draw_idle()

slider.on_changed(update)

# 保存图像
fig_path = 'bond_price_vs_yield.png'
plt.savefig(fig_path)

# 将结果存入字典
result = {
    'price_at_up100bp': price_at_up100bp,
    'dur_approx_change_up100bp': dur_approx_change_up100bp,
    'figure_path': fig_path
}
