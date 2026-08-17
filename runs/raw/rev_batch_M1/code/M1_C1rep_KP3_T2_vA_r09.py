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
    ytm = yield_to_maturity / frequency

    price = sum([coupon / (1 + ytm)**t for t in range(1, int(periods) + 1)]) + \
            face_value / (1 + ytm)**periods
    return price

def bond_duration(face_value, coupon_rate, years_to_maturity, yield_to_maturity, frequency=1):
    """
    计算麦考利久期
    """
    periods = years_to_maturity * frequency
    coupon = face_value * coupon_rate / frequency
    ytm = yield_to_maturity / frequency

    cash_flows = [coupon] * int(periods)
    cash_flows[-1] += face_value  # 最后一期加上面值

    duration = sum([t * cf / (1 + ytm)**t for t, cf in enumerate(cash_flows, 1)]) / \
               sum([cf / (1 + ytm)**t for t, cf in enumerate(cash_flows, 1)])
    return duration / frequency  # 转换为年化久期

def modified_duration(duration, yield_to_maturity, frequency=1):
    """
    计算修正久期
    """
    return duration / (1 + yield_to_maturity / frequency)

# 债券参数
face_value = 100
coupon_rate = 0.046
years_to_maturity = 7
current_yield = 0.053

# 计算当前价格和久期
current_price = bond_price(face_value, coupon_rate, years_to_maturity, current_yield)
mac_duration = bond_duration(face_value, coupon_rate, years_to_maturity, current_yield)
mod_duration = modified_duration(mac_duration, current_yield)

# 计算收益率上升100bp后的精确价格
new_yield_up100bp = current_yield + 0.01
price_up100bp = bond_price(face_value, coupon_rate, years_to_maturity, new_yield_up100bp)

# 计算久期近似的相对价格变化
dur_approx_change = -mod_duration * 0.01 * 100  # 100bp变化的百分比变化

# 创建图形
fig, ax = plt.subplots(figsize=(10, 6))
plt.subplots_adjust(bottom=0.25)

# 生成收益率范围
yields = np.linspace(0.02, 0.09, 100)
prices = [bond_price(face_value, coupon_rate, years_to_maturity, y) for y in yields]

# 计算久期近似线
approx_prices = [current_price * (1 - mod_duration * (y - current_yield)) for y in yields]

# 绘制曲线
line1, = ax.plot(yields, prices, label='精确价格')
line2, = ax.plot(yields, approx_prices, '--', label='久期近似')
ax.set_xlabel('收益率')
ax.set_ylabel('价格')
ax.set_title('债券价格随收益率变化')
ax.legend()
ax.grid(True)

# 添加滑块
axcolor = 'lightgoldenrodyellow'
ax_yield_range = plt.axes([0.2, 0.1, 0.65, 0.03], facecolor=axcolor)
slider_yield_range = Slider(ax_yield_range, '收益率范围', 0.01, 0.15, valinit=0.07)

def update(val):
    range_val = slider_yield_range.val
    yields = np.linspace(current_yield - range_val/2, current_yield + range_val/2, 100)
    yields = np.clip(yields, 0.001, 0.2)  # 防止负收益率

    prices = [bond_price(face_value, coupon_rate, years_to_maturity, y) for y in yields]
    approx_prices = [current_price * (1 - mod_duration * (y - current_yield)) for y in yields]

    line1.set_xdata(yields)
    line1.set_ydata(prices)
    line2.set_xdata(yields)
    line2.set_ydata(approx_prices)

    ax.set_xlim(yields.min(), yields.max())
    ax.set_ylim(min(min(prices), min(approx_prices)) * 0.99,
                max(max(prices), max(approx_prices)) * 1.01)
    fig.canvas.draw_idle()

slider_yield_range.on_changed(update)

# 保存图形
figure_path = 'bond_price_vs_yield.png'
plt.savefig(figure_path)
plt.close()

# 准备结果
result = {
    'price_at_up100bp': price_up100bp,
    'dur_approx_change_up100bp': dur_approx_change,
    'figure_path': os.path.abspath(figure_path)
}

print(result)
