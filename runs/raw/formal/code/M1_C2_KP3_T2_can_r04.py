import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import newton

# 参数设定
face_value = 100
coupon_rate = 0.046
years_to_maturity = 7
current_yield = 0.053
yield_shift_bp = 100  # 100个基点变动
yield_shift = yield_shift_bp / 10000

# 1. 精确定价函数
def bond_price(yield_to_maturity, face_value, coupon_rate, years_to_maturity):
    coupon = face_value * coupon_rate
    periods = years_to_maturity
    cash_flows = np.array([coupon] * periods + [face_value + coupon])
    discount_factors = (1 + yield_to_maturity) ** np.arange(1, periods + 2)
    return np.sum(cash_flows / discount_factors)

# 2. 久期和凸性计算
def bond_duration_convexity(yield_to_maturity, face_value, coupon_rate, years_to_maturity):
    coupon = face_value * coupon_rate
    periods = years_to_maturity
    cash_flows = np.array([coupon] * periods + [face_value + coupon])
    times = np.arange(1, periods + 2)
    discount_factors = (1 + yield_to_maturity) ** times
    discounted_cash_flows = cash_flows / discount_factors
    price = np.sum(discounted_cash_flows)

    # 久期 (Macaulay Duration)
    weighted_cash_flows = discounted_cash_flows * times
    macaulay_duration = np.sum(weighted_cash_flows) / price
    modified_duration = macaulay_duration / (1 + yield_to_maturity)

    # 凸性
    convexity = np.sum(discounted_cash_flows * times * (times + 1)) / (price * (1 + yield_to_maturity)**2)

    return modified_duration, convexity

# 3. 久期近似价格变化
def duration_approx(price, duration, yield_change):
    return price * (-duration * yield_change)

# 4. 凸性调整的近似
def duration_convexity_approx(price, duration, convexity, yield_change):
    return price * (-duration * yield_change + 0.5 * convexity * (yield_change**2))

# 生成收益率网格
yields = np.linspace(0.02, 0.09, 100)
prices = np.array([bond_price(y, face_value, coupon_rate, years_to_maturity) for y in yields])

# 计算当前收益率下的久期和凸性
current_price = bond_price(current_yield, face_value, coupon_rate, years_to_maturity)
duration, convexity = bond_duration_convexity(current_yield, face_value, coupon_rate, years_to_maturity)

# 久期近似线
yield_changes = yields - current_yield
approx_prices = current_price + duration_approx(current_price, duration, yield_changes)

# 计算+100bp后的精确价格和久期近似变化
new_yield = current_yield + yield_shift
new_price = bond_price(new_yield, face_value, coupon_rate, years_to_maturity)
dur_approx_change = duration_approx(current_price, duration, yield_shift) / current_price

# 绘图
plt.figure(figsize=(10, 6))
plt.plot(yields * 100, prices, label='精确价格-收益率曲线', color='blue')
plt.plot(yields * 100, approx_prices, label='久期近似', color='red', linestyle='--')
plt.scatter(current_yield * 100, current_price, color='green', zorder=5, label='当前收益率点')
plt.xlabel('收益率 (%)')
plt.ylabel('债券价格')
plt.title('债券价格-收益率曲线及久期近似')
plt.legend()
plt.grid(True)

# 保存图形
figure_path = 'bond_price_yield_curve.png'
plt.savefig(figure_path)
plt.close()

# 准备结果
result = {
    'price_at_up100bp': new_price,
    'dur_approx_change_up100bp': dur_approx_change,
    'figure_path': figure_path
}

print(result)
