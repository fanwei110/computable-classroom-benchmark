import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import PercentFormatter

# 债券参数
face_value = 100
coupon_rate = 0.046
years_to_maturity = 7
current_yield = 0.053
yield_change_bp = 100  # 100个基点变动

# 1. 计算精确价格-收益率曲线
def bond_price(yield_to_maturity, face_value, coupon_rate, years_to_maturity):
    coupon = face_value * coupon_rate
    cash_flows = np.array([coupon] * years_to_maturity)
    cash_flows[-1] += face_value  # 最后一期支付本金
    discount_factors = (1 + yield_to_maturity) ** np.arange(1, years_to_maturity + 1)
    price = np.sum(cash_flows / discount_factors)
    return price

# 收益率网格
yield_grid = np.linspace(0.02, 0.09, 100)
prices = np.array([bond_price(y, face_value, coupon_rate, years_to_maturity) for y in yield_grid])

# 2. 计算久期和凸性
def macaulay_duration_convexity(yield_to_maturity, face_value, coupon_rate, years_to_maturity):
    coupon = face_value * coupon_rate
    cash_flows = np.array([coupon] * years_to_maturity)
    cash_flows[-1] += face_value
    times = np.arange(1, years_to_maturity + 1)

    # 麦考利久期
    discounted_cf = cash_flows / (1 + yield_to_maturity) ** times
    mac_dur = np.sum(times * discounted_cf) / np.sum(discounted_cf)

    # 修正久期
    mod_dur = mac_dur / (1 + yield_to_maturity)

    # 凸性
    convexity = np.sum(times * (times + 1) * cash_flows / (1 + yield_to_maturity) ** (times + 2)) / np.sum(discounted_cf)

    return mac_dur, mod_dur, convexity

mac_dur, mod_dur, convexity = macaulay_duration_convexity(
    current_yield, face_value, coupon_rate, years_to_maturity
)

# 久期近似直线
def duration_approx(y, y0, p0, mod_dur):
    return p0 * (1 - mod_dur * (y - y0))

# 久期+凸性近似曲线
def duration_convexity_approx(y, y0, p0, mod_dur, convexity):
    dy = y - y0
    return p0 * (1 - mod_dur * dy + 0.5 * convexity * dy ** 2)

# 当前价格
current_price = bond_price(current_yield, face_value, coupon_rate, years_to_maturity)

# 近似曲线
approx_line = duration_approx(yield_grid, current_yield, current_price, mod_dur)
approx_curve = duration_convexity_approx(yield_grid, current_yield, current_price, mod_dur, convexity)

# 3. 计算+100bp的精确价格和久期估计变化
new_yield = current_yield + yield_change_bp / 10000
new_price = bond_price(new_yield, face_value, coupon_rate, years_to_maturity)
dur_approx_change = -mod_dur * (new_yield - current_yield)

# 4. 绘图
plt.figure(figsize=(10, 6))
plt.plot(yield_grid, prices, label='精确价格', color='blue')
plt.plot(yield_grid, approx_line, '--', label='久期近似', color='red')
plt.plot(yield_grid, approx_curve, '--', label='久期+凸性近似', color='green')
plt.scatter(current_yield, current_price, color='black', zorder=5)
plt.annotate(f'当前点 ({current_yield*100:.1f}%, {current_price:.2f})',
             xy=(current_yield, current_price),
             xytext=(current_yield + 0.005, current_price - 5),
             arrowprops=dict(arrowstyle='->'))

plt.title('债券价格-收益率曲线及久期/凸性近似')
plt.xlabel('收益率 (年复利)')
plt.ylabel('价格')
plt.gca().xaxis.set_major_formatter(PercentFormatter(1.0))
plt.gca().yaxis.set_major_formatter('{x:.1f}')
plt.legend()
plt.grid(True)

# 保存图形
figure_path = 'bond_price_yield_curve.png'
plt.savefig(figure_path)
plt.close()

# 填充result字典
result = {
    'price_at_up100bp': new_price,
    'dur_approx_change_up100bp': dur_approx_change,
    'figure_path': figure_path
}

# 输出结果以供验证
print(result)
