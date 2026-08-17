import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter

def calculate_bond_price(face_value, coupon_rate, years_to_maturity, ytm, frequency=1):
    """
    计算债券精确价格
    """
    periods = years_to_maturity * frequency
    coupon = face_value * coupon_rate / frequency
    ytm_period = ytm / frequency

    price = sum([coupon / (1 + ytm_period)**t for t in range(1, int(periods) + 1)]) + \
            face_value / (1 + ytm_period)**periods
    return price

def calculate_duration(face_value, coupon_rate, years_to_maturity, ytm, frequency=1):
    """
    计算麦考利久期
    """
    periods = years_to_maturity * frequency
    coupon = face_value * coupon_rate / frequency
    ytm_period = ytm / frequency

    cash_flows = [coupon] * int(periods)
    cash_flows[-1] += face_value  # 最后一期加上面值

    present_values = [cf / (1 + ytm_period)**t for t, cf in enumerate(cash_flows, 1)]
    price = sum(present_values)

    duration = sum([t * pv for t, pv in zip(range(1, int(periods) + 1), present_values)]) / price
    duration /= frequency  # 转换为年化久期

    return duration

def calculate_modified_duration(duration, ytm, frequency=1):
    """
    计算修正久期
    """
    return duration / (1 + ytm / frequency)

# 债券参数
face_value = 100
coupon_rate = 0.046
years_to_maturity = 7
ytm = 0.053

# 收益率范围
yields = np.linspace(0.02, 0.09, 100)

# 计算精确价格和久期近似价格
exact_prices = [calculate_bond_price(face_value, coupon_rate, years_to_maturity, y) for y in yields]
duration = calculate_duration(face_value, coupon_rate, years_to_maturity, ytm)
mod_duration = calculate_modified_duration(duration, ytm)
dur_approx_prices = [calculate_bond_price(face_value, coupon_rate, years_to_maturity, ytm) *
                     (1 - mod_duration * (y - ytm)) for y in yields]

# 计算+100bp后的精确价格和久期近似变化
ytm_up100bp = ytm + 0.01
price_at_up100bp = calculate_bond_price(face_value, coupon_rate, years_to_maturity, ytm_up100bp)
dur_approx_change_up100bp = -mod_duration * 0.01 * 100  # 相对变化百分比

# 绘图
plt.figure(figsize=(10, 6))
plt.plot(yields * 100, exact_prices, label='精确价格', color='blue')
plt.plot(yields * 100, dur_approx_prices, label='久期近似', color='red', linestyle='--')
plt.scatter([ytm * 100], [calculate_bond_price(face_value, coupon_rate, years_to_maturity, ytm)],
            color='green', zorder=5, label='当前YTM点')

plt.title('债券价格-收益率曲线')
plt.xlabel('收益率 (%)')
plt.ylabel('价格')
plt.legend()
plt.grid(True)

# 格式化y轴为百分比
plt.gca().xaxis.set_major_formatter(FuncFormatter(lambda x, _: f'{x:.1f}%'))

# 保存图片
figure_path = 'bond_price_yield_curve.png'
plt.savefig(figure_path)
plt.close()

# 存储结果
result = {
    'price_at_up100bp': price_at_up100bp,
    'dur_approx_change_up100bp': dur_approx_change_up100bp * 100,  # 转换为百分比
    'figure_path': figure_path
}

print(result)
