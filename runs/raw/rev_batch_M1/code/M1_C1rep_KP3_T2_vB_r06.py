import numpy as np
import matplotlib.pyplot as plt
import os

# 参数
face_value = 100
coupon_rate = 0.046
ytm_initial = 0.053
n_years = 7
y_min = 0.02
y_max = 0.09
step = 0.001

# 计算精确价格
def bond_price(ytm, coupon, face_value, n_years):
    periods = n_years
    coupon_payment = coupon * face_value
    price = sum([coupon_payment / (1 + ytm)**t for t in range(1, periods + 1)]) + face_value / (1 + ytm)**periods
    return price

# 计算久期和凸性
def duration_convexity(ytm, coupon, face_value, n_years):
    periods = n_years
    coupon_payment = coupon * face_value
    cash_flows = [coupon_payment] * periods
    cash_flows[-1] += face_value  # 最后一期加上面值

    # 久期
    discounted_cf = [cf / (1 + ytm)**t for t, cf in enumerate(cash_flows, 1)]
    price = sum(discounted_cf)
    duration = sum([t * cf for t, cf in zip(range(1, periods + 1), discounted_cf)]) / price

    # 凸性
    convexity = sum([t * (t + 1) * cf for t, cf in zip(range(1, periods + 1), discounted_cf)]) / (price * (1 + ytm)**2)
    return duration, convexity

# 计算久期近似价格
def dur_approx_price(price, duration, convexity, delta_ytm):
    return price * (1 - duration * delta_ytm + 0.5 * convexity * delta_ytm**2)

# 生成收益率范围
y_range = np.arange(y_min, y_max + step, step)
exact_prices = [bond_price(y, coupon_rate, face_value, n_years) for y in y_range]

# 计算初始久期和凸性
D, C = duration_convexity(ytm_initial, coupon_rate, face_value, n_years)
initial_price = bond_price(ytm_initial, coupon_rate, face_value, n_years)
dur_approx_prices = [dur_approx_price(initial_price, D, C, y - ytm_initial) for y in y_range]

# 计算YTM+100bp后的精确价格和久期近似变化
ytm_up100bp = ytm_initial + 0.01
price_at_up100bp = bond_price(ytm_up100bp, coupon_rate, face_value, n_years)
dur_approx_change_up100bp = -D * 0.01 * 100  # 相对变化百分比

# 绘图
plt.figure(figsize=(10, 6))
plt.plot(y_range * 100, exact_prices, label='精确价格', color='blue')
plt.plot(y_range * 100, dur_approx_prices, label='久期近似价格', color='red', linestyle='--')
plt.xlabel('收益率 (%)')
plt.ylabel('价格')
plt.title('价格收益率曲线')
plt.legend()
plt.grid(True)

# 保存图片
figure_path = 'bond_price_yield_curve.png'
plt.savefig(figure_path)
plt.close()

# 结果存入字典
result = {
    'price_at_up100bp': price_at_up100bp,
    'dur_approx_change_up100bp': dur_approx_change_up100bp,
    'figure_path': os.path.abspath(figure_path)
}

print(result)
