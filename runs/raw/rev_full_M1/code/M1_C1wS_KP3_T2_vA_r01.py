import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import PercentFormatter

# 债券参数
face_value = 100
coupon_rate = 0.046
years_to_maturity = 7
current_yield = 0.053
yield_change_bp = 100  # 100个基点变动

# 计算债券价格的函数
def bond_price(yield_to_maturity, face_value, coupon_rate, years_to_maturity):
    coupon_payment = face_value * coupon_rate
    periods = years_to_maturity
    cash_flows = np.array([coupon_payment] * periods + [face_value + coupon_payment])
    discount_factors = (1 + yield_to_maturity) ** np.arange(1, periods + 2)
    price = np.sum(cash_flows / discount_factors)
    return price

# 计算久期和凸性的函数
def bond_duration_convexity(yield_to_maturity, face_value, coupon_rate, years_to_maturity):
    coupon_payment = face_value * coupon_rate
    periods = years_to_maturity
    cash_flows = np.array([coupon_payment] * periods + [face_value + coupon_payment])
    times = np.arange(1, periods + 2)

    # 久期计算
    discount_factors = (1 + yield_to_maturity) ** times
    present_values = cash_flows / discount_factors
    duration = np.sum(times * present_values) / np.sum(present_values) / (1 + yield_to_maturity)

    # 凸性计算
    convexity = np.sum(times * (times + 1) * present_values) / np.sum(present_values) / (1 + yield_to_maturity)**2

    return duration, convexity

# 1. 在2%到9%的收益率网格上计算精确价格
yield_grid = np.linspace(0.02, 0.09, 100)
prices_exact = np.array([bond_price(y, face_value, coupon_rate, years_to_maturity) for y in yield_grid])

# 2. 在5.3%附近计算久期近似
duration, convexity = bond_duration_convexity(current_yield, face_value, coupon_rate, years_to_maturity)
yield_approx = np.linspace(current_yield - 0.02, current_yield + 0.02, 50)
price_approx = bond_price(current_yield, face_value, coupon_rate, years_to_maturity) * (
    1 - duration * (yield_approx - current_yield) + 0.5 * convexity * (yield_approx - current_yield)**2
)

# 3. 报告+100bp的精确价格和久期估计变化
new_yield = current_yield + yield_change_bp / 10000
price_up100bp = bond_price(new_yield, face_value, coupon_rate, years_to_maturity)
dur_approx_change = -duration * (yield_change_bp / 10000) * 100  # 相对变化百分比

# 绘图
plt.figure(figsize=(10, 6))
plt.plot(yield_grid * 100, prices_exact, label='精确价格', color='blue')
plt.plot(yield_approx * 100, price_approx, label='久期近似', color='red', linestyle='--')
plt.scatter(current_yield * 100, bond_price(current_yield, face_value, coupon_rate, years_to_maturity),
            color='green', zorder=5, label='当前收益率(5.3%)')
plt.xlabel('收益率 (%)')
plt.ylabel('债券价格')
plt.title('债券价格与收益率关系')
plt.legend()
plt.grid(True)
plt.gca().xaxis.set_major_formatter(PercentFormatter())

# 保存图形
figure_path = 'bond_price_duration_plot.png'
plt.savefig(figure_path)
plt.close()

# 填充result字典
result = {
    'price_at_up100bp': price_up100bp,
    'dur_approx_change_up100bp': dur_approx_change,
    'figure_path': figure_path
}

# 输出结果以便验证
print(result)
