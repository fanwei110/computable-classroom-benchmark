import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import newton

# 参数设定
face_value = 100
coupon_rate = 0.046
years_to_maturity = 7
current_yield = 0.053
yield_change_bp = 100  # 100个基点变动
yield_change = yield_change_bp / 10000

# 1. 精确定价函数
def bond_price(yield_to_maturity, face_value, coupon_rate, years_to_maturity):
    coupon_payment = face_value * coupon_rate
    periods = years_to_maturity
    cash_flows = np.array([coupon_payment] * periods)
    cash_flows[-1] += face_value  # 最后一期加上面值

    discount_factors = (1 + yield_to_maturity) ** np.arange(1, periods + 1)
    present_values = cash_flows / discount_factors
    return np.sum(present_values)

# 2. 计算久期和凸性
def bond_duration_convexity(yield_to_maturity, face_value, coupon_rate, years_to_maturity):
    coupon_payment = face_value * coupon_rate
    periods = years_to_maturity
    cash_flows = np.array([coupon_payment] * periods)
    cash_flows[-1] += face_value

    times = np.arange(1, periods + 1)
    discount_factors = (1 + yield_to_maturity) ** times
    present_values = cash_flows / discount_factors

    # 久期计算
    weighted_pv = present_values * times
    duration = np.sum(weighted_pv) / np.sum(present_values) / (1 + yield_to_maturity)

    # 凸性计算
    weighted_pv2 = present_values * times * (times + 1)
    convexity = np.sum(weighted_pv2) / np.sum(present_values) / (1 + yield_to_maturity)**2

    return duration, convexity

# 计算当前价格和久期、凸性
current_price = bond_price(current_yield, face_value, coupon_rate, years_to_maturity)
duration, convexity = bond_duration_convexity(current_yield, face_value, coupon_rate, years_to_maturity)

# 3. 生成收益率网格和精确价格曲线
yield_grid = np.linspace(0.02, 0.09, 100)
exact_prices = np.array([bond_price(y, face_value, coupon_rate, years_to_maturity) for y in yield_grid])

# 4. 久期近似曲线
def duration_approximation(price, duration, yield_change):
    return price * (1 - duration * yield_change)

# 计算久期近似价格
approx_prices = duration_approximation(current_price, duration, yield_grid - current_yield)

# 5. 计算+100bp的精确价格和久期近似变化
yield_up100bp = current_yield + yield_change
price_up100bp = bond_price(yield_up100bp, face_value, coupon_rate, years_to_maturity)
dur_approx_change = -duration * yield_change * 100  # 百分比变化

# 6. 绘图
plt.figure(figsize=(10, 6))
plt.plot(yield_grid * 100, exact_prices, label='Exact Price-Yield Curve', color='blue')
plt.plot(yield_grid * 100, approx_prices, label='Duration Approximation', color='red', linestyle='--')
plt.scatter(current_yield * 100, current_price, color='green', zorder=5, label='Current Yield (5.3%)')
plt.xlabel('Yield to Maturity (%)')
plt.ylabel('Bond Price')
plt.title('Bond Price-Yield Curve with Duration Approximation')
plt.legend()
plt.grid(True)

# 保存图形
figure_path = 'bond_price_yield_curve.png'
plt.savefig(figure_path)
plt.close()

# 7. 准备结果字典
result = {
    'price_at_up100bp': price_up100bp,
    'dur_approx_change_up100bp': dur_approx_change,
    'figure_path': figure_path
}

# 输出结果以便验证
print(result)
