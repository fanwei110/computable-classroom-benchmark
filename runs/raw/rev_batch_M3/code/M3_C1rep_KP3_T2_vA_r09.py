import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider

# 债券基本参数
face = 100
coupon_rate = 0.046
years = 7
y0 = 0.053  # 初始收益率

# 现金流
cash_flows = np.array([face * coupon_rate] * (years - 1) + [face * (1 + coupon_rate)])
times = np.arange(1, years + 1)

# 精确价格计算函数
def bond_price(y):
    return np.sum(cash_flows / (1 + y) ** times)

# 修正久期计算函数
def bond_modified_duration(y):
    pv = cash_flows / (1 + y) ** times
    mac_dur = np.sum(times * pv) / np.sum(pv)
    return mac_dur / (1 + y)

# 初始值计算
P0 = bond_price(y0)
ModD = bond_modified_duration(y0)

# 久期近似价格计算函数
def dur_approx_price(y):
    return P0 * (1 - ModD * (y - y0))

# 1. 收益率上升100bp后的精确价格
y_up100 = y0 + 0.01
price_at_up100bp = bond_price(y_up100)

# 2. 用久期估算的相对价格变化
dur_approx_change_up100bp = -ModD * 0.01

# 绘图数据
y_range = np.linspace(0.02, 0.09, 500)
exact_prices = [bond_price(y) for y in y_range]
approx_prices = [dur_approx_price(y) for y in y_range]

# 创建图表与滑块
fig, ax = plt.subplots(figsize=(10, 6))
plt.subplots_adjust(bottom=0.25)

# 绘制精确与近似曲线
ax.plot(y_range * 100, exact_prices, label='Exact Price (精确)', color='blue', linewidth=2)
ax.plot(y_range * 100, approx_prices, label='Duration Approximation (久期近似)', color='red', linestyle='--')
ax.set_xlabel('Yield (%)')
ax.set_ylabel('Price')
ax.set_title('Bond Price vs. Yield')
ax.legend()
ax.grid(True)

# 标记初始点
init_shift = 0.0
vline = ax.axvline(x=(y0 + init_shift) * 100, color='gray', linestyle=':')
exact_point, = ax.plot((y0 + init_shift) * 100, bond_price(y0 + init_shift), 'bo', markersize=8)
approx_point, = ax.plot((y0 + init_shift) * 100, dur_approx_price(y0 + init_shift), 'rx', markersize=8)

# 加入收益率变动幅度滑块
ax_slider = plt.axes([0.2, 0.1, 0.6, 0.03])
slider = Slider(ax_slider, 'Yield Shift (bps)', -300, 300, valinit=0, valstep=10)

def update(val):
    shift = slider.val / 10000.0
    y_new = y0 + shift
    vline.set_xdata([y_new * 100, y_new * 100])
    exact_point.set_xdata([y_new * 100])
    exact_point.set_ydata([bond_price(y_new)])
    approx_point.set_xdata([y_new * 100])
    approx_point.set_ydata([dur_approx_price(y_new)])
    fig.canvas.draw_idle()

slider.on_changed(update)

# 保存图表
figure_path = 'bond_price_vs_yield.png'
plt.savefig(figure_path)

# 按要求封装结果
result = {
    'price_at_up100bp': round(price_at_up100bp, 4),
    'dur_approx_change_up100bp': round(dur_approx_change_up100bp, 6),
    'figure_path': figure_path
}

print(result)
