import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import newton

# 参数设定
face_value = 100
coupon_rate = 0.046
years_to_maturity = 7
current_yield = 0.053
yield_change_bp = 100  # 100 basis points = 1%

# 1. 精确定价函数
def bond_price(yield_to_maturity, face_value, coupon_rate, years_to_maturity):
    coupon_payment = face_value * coupon_rate
    periods = years_to_maturity
    cash_flows = np.array([coupon_payment] * periods + [face_value + coupon_payment])
    discount_factors = np.array([(1 + yield_to_maturity) ** (-t) for t in range(1, periods + 2)])
    price = np.sum(cash_flows * discount_factors)
    return price

# 2. 久期和凸性计算
def bond_duration_convexity(yield_to_maturity, face_value, coupon_rate, years_to_maturity):
    coupon_payment = face_value * coupon_rate
    periods = years_to_maturity
    cash_flows = np.array([coupon_payment] * periods + [face_value + coupon_payment])
    times = np.arange(1, periods + 2)

    # 久期计算
    discount_factors = np.array([(1 + yield_to_maturity) ** (-t) for t in times])
    present_values = cash_flows * discount_factors
    price = np.sum(present_values)
    weighted_times = times * present_values
    macaulay_duration = np.sum(weighted_times) / price
    modified_duration = macaulay_duration / (1 + yield_to_maturity)

    # 凸性计算
    convexity = np.sum(present_values * times * (times + 1)) / (price * (1 + yield_to_maturity) ** 2)

    return modified_duration, convexity

# 3. 久期近似价格变化
def duration_approx_price(yield_change, current_price, modified_duration, convexity):
    delta_y = yield_change
    approx_change = -modified_duration * delta_y + 0.5 * convexity * (delta_y ** 2)
    approx_price = current_price * (1 + approx_change)
    return approx_price

# 生成收益率网格
yield_grid = np.linspace(0.02, 0.09, 100)
exact_prices = np.array([bond_price(y, face_value, coupon_rate, years_to_maturity) for y in yield_grid])

# 计算当前价格、久期和凸性
current_price = bond_price(current_yield, face_value, coupon_rate, years_to_maturity)
modified_duration, convexity = bond_duration_convexity(current_yield, face_value, coupon_rate, years_to_maturity)

# 久期近似曲线
yield_change_range = np.linspace(-0.02, 0.02, 50)  # ±2% 收益率变化
approx_prices = np.array([duration_approx_price(dy, current_price, modified_duration, convexity)
                          for dy in yield_change_range])
approx_yields = current_yield + yield_change_range

# 计算 +100bp 的精确价格和久期近似变化
yield_up100bp = current_yield + yield_change_bp / 10000
price_up100bp = bond_price(yield_up100bp, face_value, coupon_rate, years_to_maturity)
dur_approx_change = -modified_duration * (yield_change_bp / 10000) * 100  # 相对变化百分比

# 绘图
plt.figure(figsize=(10, 6))
plt.plot(yield_grid * 100, exact_prices, label='Exact Price-Yield Curve', color='blue')
plt.plot(approx_yields * 100, approx_prices, label='Duration Approximation', color='red', linestyle='--')
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

# 填充结果字典
result = {
    'price_at_up100bp': price_up100bp,
    'dur_approx_change_up100bp': dur_approx_change,
    'figure_path': figure_path
}

# 输出结果以供验证
print(result)
