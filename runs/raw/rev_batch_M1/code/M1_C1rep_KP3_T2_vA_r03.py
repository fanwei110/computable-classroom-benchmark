import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider
import os

def bond_price(face_value, coupon_rate, years_to_maturity, ytm, frequency=1):
    """
    计算债券精确价格
    """
    periods = years_to_maturity * frequency
    coupon = face_value * coupon_rate / frequency
    ytm_period = ytm / frequency

    price = sum([coupon / (1 + ytm_period)**t for t in range(1, int(periods) + 1)]) + \
            face_value / (1 + ytm_period)**periods
    return price

def duration_macaulay(face_value, coupon_rate, years_to_maturity, ytm, frequency=1):
    """
    计算麦考利久期
    """
    periods = years_to_maturity * frequency
    coupon = face_value * coupon_rate / frequency
    ytm_period = ytm / frequency

    cash_flows = [coupon] * int(periods)
    cash_flows[-1] += face_value  # 最后一期加上面值

    weighted_cash_flows = [t * cf / (1 + ytm_period)**t for t, cf in enumerate(cash_flows, 1)]
    mac_duration = sum(weighted_cash_flows) / bond_price(face_value, coupon_rate, years_to_maturity, ytm, frequency)

    return mac_duration / frequency  # 转换为年化久期

def duration_modified(face_value, coupon_rate, years_to_maturity, ytm, frequency=1):
    """
    计算修正久期
    """
    mac_dur = duration_macaulay(face_value, coupon_rate, years_to_maturity, ytm, frequency)
    return mac_dur / (1 + ytm / frequency)

def price_approx_change(duration_mod, ytm_change):
    """
    使用久期近似计算价格变化
    """
    return -duration_mod * ytm_change

# 债券参数
face_value = 100
coupon_rate = 0.046
years_to_maturity = 7
current_ytm = 0.053
ytm_change_bps = 100  # 100个基点

# 计算当前价格
current_price = bond_price(face_value, coupon_rate, years_to_maturity, current_ytm)

# 计算久期
mod_duration = duration_modified(face_value, coupon_rate, years_to_maturity, current_ytm)

# 计算收益率上升100bp后的精确价格
new_ytm = current_ytm + ytm_change_bps / 10000
new_price = bond_price(face_value, coupon_rate, years_to_maturity, new_ytm)

# 计算久期近似的价格变化
price_change_approx = price_approx_change(mod_duration, ytm_change_bps / 10000)
dur_approx_change = price_change_approx * 100  # 转换为百分比

# 创建结果字典
result = {
    'price_at_up100bp': new_price,
    'dur_approx_change_up100bp': dur_approx_change,
    'figure_path': None
}

# 绘制图形
fig, ax = plt.subplots(figsize=(10, 6))
plt.subplots_adjust(bottom=0.25)

# 生成收益率范围
ytm_range = np.linspace(0.02, 0.09, 100)
prices = [bond_price(face_value, coupon_rate, years_to_maturity, y) for y in ytm_range]

# 计算久期近似线
current_price = bond_price(face_value, coupon_rate, years_to_maturity, current_ytm)
mod_duration = duration_modified(face_value, coupon_rate, years_to_maturity, current_ytm)
approx_prices = [current_price * (1 + price_approx_change(mod_duration, y - current_ytm)) for y in ytm_range]

# 绘制曲线
line_exact, = ax.plot(ytm_range * 100, prices, label='精确价格', color='blue')
line_approx, = ax.plot(ytm_range * 100, approx_prices, label='久期近似', color='red', linestyle='--')

ax.set_xlabel('收益率 (%)')
ax.set_ylabel('债券价格')
ax.set_title('债券价格与收益率关系')
ax.legend()
ax.grid(True)

# 添加滑块
axcolor = 'lightgoldenrodyellow'
ax_ytm_change = plt.axes([0.2, 0.1, 0.65, 0.03], facecolor=axcolor)
slider_ytm_change = Slider(ax_ytm_change, '收益率变动幅度 (bps)', 1, 200, valinit=ytm_change_bps, valstep=1)

def update(val):
    change_bps = slider_ytm_change.val
    new_ytm = current_ytm + change_bps / 10000
    new_price = bond_price(face_value, coupon_rate, years_to_maturity, new_ytm)
    approx_change = price_approx_change(mod_duration, change_bps / 10000) * 100

    # 更新近似线
    approx_prices = [current_price * (1 + price_approx_change(mod_duration, y - current_ytm)) for y in ytm_range]
    line_approx.set_ydata(approx_prices)

    fig.canvas.draw_idle()

slider_ytm_change.on_changed(update)

# 保存图形
figure_path = 'bond_price_vs_ytm.png'
plt.savefig(figure_path)
result['figure_path'] = os.path.abspath(figure_path)

plt.show()

# 输出结果
print(result)
