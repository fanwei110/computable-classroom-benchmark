import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider
import os

def bond_price(face_value, coupon_rate, years_to_maturity, yield_to_maturity, frequency=1):
    """
    计算债券精确价格
    """
    periods = years_to_maturity * frequency
    coupon = face_value * coupon_rate / frequency
    yield_per_period = yield_to_maturity / frequency

    price = sum([coupon / (1 + yield_per_period)**t for t in range(1, int(periods) + 1)])
    price += face_value / (1 + yield_per_period)**periods
    return price

def duration_macaulay(face_value, coupon_rate, years_to_maturity, yield_to_maturity, frequency=1):
    """
    计算麦考利久期
    """
    periods = years_to_maturity * frequency
    coupon = face_value * coupon_rate / frequency
    yield_per_period = yield_to_maturity / frequency

    cash_flows = [coupon] * int(periods)
    cash_flows[-1] += face_value  # 最后一期加上面值

    weighted_cash_flows = [t * cf / (1 + yield_per_period)**t for t, cf in enumerate(cash_flows, 1)]
    mac_duration = sum(weighted_cash_flows) / bond_price(face_value, coupon_rate, years_to_maturity, yield_to_maturity, frequency)
    return mac_duration / frequency  # 转换为年久期

def duration_modified(face_value, coupon_rate, years_to_maturity, yield_to_maturity, frequency=1):
    """
    计算修正久期
    """
    mac_dur = duration_macaulay(face_value, coupon_rate, years_to_maturity, yield_to_maturity, frequency)
    return mac_dur / (1 + yield_to_maturity / frequency)

# 债券参数
face_value = 100
coupon_rate = 0.046
years_to_maturity = 7
current_yield = 0.053
frequency = 1

# 计算当前价格和久期
current_price = bond_price(face_value, coupon_rate, years_to_maturity, current_yield)
mod_duration = duration_modified(face_value, coupon_rate, years_to_maturity, current_yield)

# 计算收益率上升100bp后的精确价格
yield_up100bp = current_yield + 0.01
price_up100bp = bond_price(face_value, coupon_rate, years_to_maturity, yield_up100bp)

# 计算久期近似的价格变化
dur_approx_change = -mod_duration * 0.01 * 100  # 相对变化百分比

# 创建图形
fig, ax = plt.subplots(figsize=(10, 6))
plt.subplots_adjust(bottom=0.25)

# 生成收益率范围
yields = np.linspace(0.02, 0.09, 100)
prices = [bond_price(face_value, coupon_rate, years_to_maturity, y) for y in yields]

# 绘制精确价格曲线
line_exact, = ax.plot(yields, prices, label='精确价格', color='blue')

# 绘制久期近似线
approx_prices = [current_price * (1 - mod_duration * (y - current_yield)) for y in yields]
line_approx, = ax.plot(yields, approx_prices, label='久期近似', color='red', linestyle='--')

# 标记当前点
ax.scatter(current_yield, current_price, color='green', zorder=5)
ax.annotate(f'当前点\n收益率: {current_yield*100:.1f}%\n价格: {current_price:.2f}',
            xy=(current_yield, current_price),
            xytext=(current_yield+0.005, current_price-5),
            arrowprops=dict(facecolor='black', shrink=0.05))

ax.set_xlabel('收益率')
ax.set_ylabel('价格')
ax.set_title('债券价格与收益率关系')
ax.legend()
ax.grid(True)

# 添加滑动条
axcolor = 'lightgoldenrodyellow'
ax_shift = plt.axes([0.2, 0.1, 0.65, 0.03], facecolor=axcolor)
shift_slider = Slider(ax_shift, '收益率变动幅度(bp)', -100, 100, valinit=0, valstep=1)

def update(val):
    shift = shift_slider.val / 10000  # 转换为百分点
    new_yields = yields + shift
    new_prices = [bond_price(face_value, coupon_rate, years_to_maturity, y) for y in new_yields]
    new_approx_prices = [current_price * (1 - mod_duration * (y - (current_yield + shift))) for y in new_yields]

    line_exact.set_xdata(new_yields)
    line_exact.set_ydata(new_prices)
    line_approx.set_xdata(new_yields)
    line_approx.set_ydata(new_approx_prices)

    ax.set_xlim(new_yields.min(), new_yields.max())
    fig.canvas.draw_idle()

shift_slider.on_changed(update)

# 保存图形
figure_path = 'bond_price_yield_curve.png'
plt.savefig(figure_path)
plt.close()

# 准备结果
result = {
    'price_at_up100bp': price_up100bp,
    'dur_approx_change_up100bp': dur_approx_change,
    'figure_path': os.path.abspath(figure_path)
}

print(result)
