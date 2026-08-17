import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import newton

# 参数设定
face_value = 100
coupon_rate = 0.046
years_to_maturity = 7
current_yield = 0.053
yield_shift_bp = 100  # 100 basis points for reporting
yield_shift = yield_shift_bp / 10000  # Convert basis points to decimal

# 收益率网格
yields = np.linspace(0.02, 0.09, 100)

# 1. 精确债券定价函数
def bond_price(yield_to_maturity, face_value, coupon_rate, years_to_maturity):
    coupon_payment = face_value * coupon_rate
    periods = years_to_maturity
    cash_flows = np.array([coupon_payment] * periods + [face_value + coupon_payment])
    discount_factors = (1 + yield_to_maturity) ** np.arange(1, periods + 2)
    price = np.sum(cash_flows / discount_factors)
    return price

# 计算精确价格曲线
prices_exact = np.array([bond_price(y, face_value, coupon_rate, years_to_maturity) for y in yields])

# 2. 久期和凸性计算
def bond_duration_convexity(yield_to_maturity, face_value, coupon_rate, years_to_maturity):
    coupon_payment = face_value * coupon_rate
    periods = years_to_maturity
    cash_flows = np.array([coupon_payment] * periods + [face_value + coupon_payment])
    times = np.arange(1, periods + 2)
    discount_factors = (1 + yield_to_maturity) ** times
    discounted_cash_flows = cash_flows / discount_factors
    price = np.sum(discounted_cash_flows)

    # Duration (Macaulay)
    weighted_cash_flows = discounted_cash_flows * times
    macaulay_duration = np.sum(weighted_cash_flows) / price
    modified_duration = macaulay_duration / (1 + yield_to_maturity)

    # Convexity
    convexity = np.sum(discounted_cash_flows * times * (times + 1)) / (price * (1 + yield_to_maturity)**2)

    return modified_duration, convexity

# 计算当前收益率下的久期和凸性
duration, convexity = bond_duration_convexity(current_yield, face_value, coupon_rate, years_to_maturity)

# 基于久期的近似价格曲线
def duration_approx_price(yield_change, current_price, duration, convexity):
    return current_price * (1 - duration * yield_change + 0.5 * convexity * (yield_change**2))

current_price = bond_price(current_yield, face_value, coupon_rate, years_to_maturity)
yield_changes = yields - current_yield
prices_approx = duration_approx_price(yield_changes, current_price, duration, convexity)

# 3. 报告 +100bp 的精确价格和久期法估计的相对变化
price_up100bp = bond_price(current_yield + yield_shift, face_value, coupon_rate, years_to_maturity)
dur_approx_change = -duration * yield_shift + 0.5 * convexity * (yield_shift**2)

# 4. 绘图
plt.figure(figsize=(10, 6))
plt.plot(yields * 100, prices_exact, label='Exact Price-Yield Curve', color='blue')
plt.plot(yields * 100, prices_approx, label='Duration-based Approximation', color='red', linestyle='--')
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

# 填充 result 字典
result = {
    'price_at_up100bp': price_up100bp,
    'dur_approx_change_up100bp': dur_approx_change,
    'figure_path': figure_path
}

# 输出 result 以便检查
print(result)
