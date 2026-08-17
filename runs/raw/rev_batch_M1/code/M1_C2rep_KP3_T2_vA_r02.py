import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import newton

# 参数设定
face_value = 100
coupon_rate = 0.046
years_to_maturity = 7
current_yield = 0.053
yield_shift_bp = 100  # 可调的收益率变动幅度（基点）

# 计算票息现金流
coupon_payment = face_value * coupon_rate
cash_flows = np.full(years_to_maturity, coupon_payment)
cash_flows[-1] += face_value  # 最后一期包含本金

# 精确定价函数
def bond_price(yield_to_maturity):
    periods = np.arange(1, years_to_maturity + 1)
    discounted_cash_flows = cash_flows / ((1 + yield_to_maturity) ** periods)
    return np.sum(discounted_cash_flows)

# 久期和凸性计算
def macaulay_duration_convexity(yield_to_maturity):
    periods = np.arange(1, years_to_maturity + 1)
    discounted_cash_flows = cash_flows / ((1 + yield_to_maturity) ** periods)
    weights = discounted_cash_flows / bond_price(yield_to_maturity)
    duration = np.sum(periods * weights)
    convexity = np.sum(periods * (periods + 1) * weights) / (1 + yield_to_maturity)**2
    return duration, convexity

# 久期近似价格变化
def duration_approx_price(yield_to_maturity, yield_change, duration, convexity):
    modified_duration = duration / (1 + yield_to_maturity)
    price_change = (-modified_duration * yield_change) + (0.5 * convexity * (yield_change**2))
    return bond_price(yield_to_maturity) * (1 + price_change)

# 1. 生成精确价格曲线
yield_grid = np.linspace(0.02, 0.09, 100)
exact_prices = np.array([bond_price(y) for y in yield_grid])

# 2. 计算当前收益率下的久期和凸性
current_duration, current_convexity = macaulay_duration_convexity(current_yield)
modified_duration = current_duration / (1 + current_yield)

# 久期近似曲线（在当前收益率附近）
yield_change_grid = yield_grid - current_yield
approx_prices = duration_approx_price(current_yield, yield_change_grid, current_duration, current_convexity)

# 3. 报告+100bp的精确价格和久期法估计变化
yield_up100bp = current_yield + yield_shift_bp / 10000
price_at_up100bp = bond_price(yield_up100bp)
dur_approx_change_up100bp = -modified_duration * (yield_shift_bp / 10000) * 100  # 相对变化百分比

# 绘图
plt.figure(figsize=(10, 6))
plt.plot(yield_grid * 100, exact_prices, label='精确价格', color='blue')
plt.plot(yield_grid * 100, approx_prices, label='久期近似', color='red', linestyle='--')
plt.scatter(current_yield * 100, bond_price(current_yield), color='green', zorder=5)
plt.xlabel('收益率 (%)')
plt.ylabel('债券价格')
plt.title(f'债券价格-收益率曲线 (票息={coupon_rate*100}%, 期限={years_to_maturity}年)')
plt.legend()
plt.grid(True)

# 保存图形
figure_path = 'bond_price_yield_curve.png'
plt.savefig(figure_path)
plt.close()

# 填充结果字典
result = {
    'price_at_up100bp': price_at_up100bp,
    'dur_approx_change_up100bp': dur_approx_change_up100bp,
    'figure_path': figure_path
}

# 输出结果（供教师查看）
print(result)
