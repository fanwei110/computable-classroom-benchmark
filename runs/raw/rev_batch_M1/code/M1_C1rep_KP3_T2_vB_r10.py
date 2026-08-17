import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter
import os

def calculate_bond_price(face_value, coupon_rate, ytm, years_to_maturity, frequency=1):
    """
    计算债券精确价格
    """
    periods = years_to_maturity * frequency
    coupon = face_value * coupon_rate / frequency
    ytm_period = ytm / frequency

    price = sum([coupon / (1 + ytm_period)**t for t in range(1, periods + 1)]) + \
            face_value / (1 + ytm_period)**periods
    return price

def calculate_duration(face_value, coupon_rate, ytm, years_to_maturity, frequency=1):
    """
    计算麦考利久期
    """
    periods = years_to_maturity * frequency
    coupon = face_value * coupon_rate / frequency
    ytm_period = ytm / frequency

    cash_flows = [coupon] * periods
    cash_flows[-1] += face_value  # 最后一期加上面值

    duration = sum([t * cf / (1 + ytm_period)**t for t, cf in enumerate(cash_flows, 1)]) / \
               sum([cf / (1 + ytm_period)**t for t, cf in enumerate(cash_flows, 1)])
    return duration / frequency  # 转换为年久期

def calculate_modified_duration(macaulay_duration, ytm, frequency=1):
    """
    计算修正久期
    """
    return macaulay_duration / (1 + ytm / frequency)

# 债券参数
face_value = 100
coupon_rate = 0.046
ytm = 0.053
years_to_maturity = 7

# 计算初始价格和久期
initial_price = calculate_bond_price(face_value, coupon_rate, ytm, years_to_maturity)
macaulay_duration = calculate_duration(face_value, coupon_rate, ytm, years_to_maturity)
modified_duration = calculate_modified_duration(macaulay_duration, ytm)

# 收益率范围
yields = np.linspace(0.02, 0.09, 100)
prices = [calculate_bond_price(face_value, coupon_rate, y, years_to_maturity) for y in yields]

# 久期近似价格变化
approx_prices = [initial_price * (1 - modified_duration * (y - ytm)) for y in yields]

# 计算+100bp后的精确价格和久期近似变化
ytm_up100bp = ytm + 0.01
price_at_up100bp = calculate_bond_price(face_value, coupon_rate, ytm_up100bp, years_to_maturity)
dur_approx_change_up100bp = -modified_duration * 0.01 * 100  # 相对变化百分比

# 绘图
plt.figure(figsize=(10, 6))
plt.plot(yields * 100, prices, label='精确价格', color='blue')
plt.plot(yields * 100, approx_prices, '--', label='久期近似', color='red')
plt.scatter([ytm * 100], [initial_price], color='green', zorder=5, label=f'初始点(YTM={ytm*100:.1f}%)')
plt.scatter([ytm_up100bp * 100], [price_at_up100bp], color='purple', zorder=5, label=f'+100bp(YTM={ytm_up100bp*100:.1f}%)')

plt.title('债券价格-收益率曲线', fontsize=14)
plt.xlabel('收益率(%)', fontsize=12)
plt.ylabel('价格', fontsize=12)
plt.grid(True, linestyle='--', alpha=0.6)
plt.legend(fontsize=10)

# 格式化y轴为百分比
plt.gca().yaxis.set_major_formatter(FuncFormatter(lambda x, _: f'{x:.2f}'))

# 保存图片
figure_path = 'bond_price_yield_curve.png'
plt.savefig(figure_path, dpi=300, bbox_inches='tight')
plt.close()

# 存储结果
result = {
    'price_at_up100bp': price_at_up100bp,
    'dur_approx_change_up100bp': dur_approx_change_up100bp,
    'figure_path': os.path.abspath(figure_path)
}

print(result)
