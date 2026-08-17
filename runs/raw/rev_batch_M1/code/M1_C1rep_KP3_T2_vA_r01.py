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

def modified_duration(face_value, coupon_rate, years_to_maturity, ytm, frequency=1):
    """
    计算修正久期
    """
    mac_dur = duration_macaulay(face_value, coupon_rate, years_to_maturity, ytm, frequency)
    return mac_dur / (1 + ytm / frequency)

def plot_bond_price_with_duration(face_value, coupon_rate, years_to_maturity, initial_ytm, ytm_range=(0.02, 0.09), bp_change=100):
    """
    绘制债券价格随收益率变化曲线，并叠加久期近似线
    """
    # 计算精确价格曲线
    ytm_values = np.linspace(ytm_range[0], ytm_range[1], 100)
    exact_prices = [bond_price(face_value, coupon_rate, years_to_maturity, y) for y in ytm_values]

    # 计算久期近似线
    current_price = bond_price(face_value, coupon_rate, years_to_maturity, initial_ytm)
    mod_dur = modified_duration(face_value, coupon_rate, years_to_maturity, initial_ytm)
    approx_prices = [current_price * (1 - mod_dur * (y - initial_ytm)) for y in ytm_values]

    # 创建图形
    fig, ax = plt.subplots(figsize=(10, 6))
    plt.subplots_adjust(bottom=0.25)

    # 绘制曲线
    exact_line, = ax.plot(ytm_values * 100, exact_prices, label='精确价格', color='blue')
    approx_line, = ax.plot(ytm_values * 100, approx_prices, label='久期近似', color='red', linestyle='--')

    # 设置图形属性
    ax.set_xlabel('收益率 (%)')
    ax.set_ylabel('债券价格')
    ax.set_title('债券价格随收益率变化')
    ax.legend()
    ax.grid(True)

    # 添加滑块
    axcolor = 'lightgoldenrodyellow'
    ax_bp = plt.axes([0.2, 0.1, 0.65, 0.03], facecolor=axcolor)
    bp_slider = Slider(ax_bp, '基点变动', 1, 300, valinit=bp_change, valstep=1)

    def update(val):
        bp = bp_slider.val
        new_ytm = initial_ytm + bp / 10000
        if new_ytm > ytm_range[1]:
            new_ytm = ytm_range[1]
        elif new_ytm < ytm_range[0]:
            new_ytm = ytm_range[0]

        # 更新近似线
        current_price = bond_price(face_value, coupon_rate, years_to_maturity, initial_ytm)
        mod_dur = modified_duration(face_value, coupon_rate, years_to_maturity, initial_ytm)
        approx_prices = [current_price * (1 - mod_dur * (y - initial_ytm)) for y in ytm_values]
        approx_line.set_ydata(approx_prices)

        # 更新图形
        fig.canvas.draw_idle()

    bp_slider.on_changed(update)

    # 保存图形
    figure_path = 'bond_price_duration_plot.png'
    plt.savefig(figure_path)
    plt.close()

    # 计算收益率上升100bp后的精确价格
    new_ytm = initial_ytm + bp_change / 10000
    price_at_up100bp = bond_price(face_value, coupon_rate, years_to_maturity, new_ytm)

    # 计算久期近似的相对价格变化
    mod_dur = modified_duration(face_value, coupon_rate, years_to_maturity, initial_ytm)
    dur_approx_change_up100bp = -mod_dur * (bp_change / 10000) * 100  # 转换为百分比

    return {
        'price_at_up100bp': price_at_up100bp,
        'dur_approx_change_up100bp': dur_approx_change_up100bp,
        'figure_path': os.path.abspath(figure_path)
    }

# 债券参数
face_value = 100
coupon_rate = 0.046
years_to_maturity = 7
initial_ytm = 0.053

# 生成结果
result = plot_bond_price_with_duration(face_value, coupon_rate, years_to_maturity, initial_ytm)

# 输出结果
print(result)
