import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import PercentFormatter

def bond_price(y, face_value, coupon_rate, years_to_maturity):
    """计算债券精确价格"""
    coupon = face_value * coupon_rate
    cash_flows = np.full(years_to_maturity, coupon)
    cash_flows[-1] += face_value  # 最后一期加上面值
    discount_factors = (1 + y) ** np.arange(1, years_to_maturity + 1)
    return np.sum(cash_flows / discount_factors)

def macaulay_duration(y, face_value, coupon_rate, years_to_maturity):
    """计算麦考利久期"""
    coupon = face_value * coupon_rate
    cash_flows = np.full(years_to_maturity, coupon)
    cash_flows[-1] += face_value
    discount_factors = (1 + y) ** np.arange(1, years_to_maturity + 1)
    discounted_cf = cash_flows / discount_factors
    weights = discounted_cf / np.sum(discounted_cf)
    return np.sum(weights * np.arange(1, years_to_maturity + 1))

def convexity(y, face_value, coupon_rate, years_to_maturity):
    """计算凸性"""
    coupon = face_value * coupon_rate
    cash_flows = np.full(years_to_maturity, coupon)
    cash_flows[-1] += face_value
    discount_factors = (1 + y) ** np.arange(1, years_to_maturity + 2)
    t_t1_cf = cash_flows * np.arange(1, years_to_maturity + 1) * np.arange(2, years_to_maturity + 2)
    convexity_val = np.sum(t_t1_cf / discount_factors) / bond_price(y, face_value, coupon_rate, years_to_maturity)
    return convexity_val

# 债券参数
face_value = 100
coupon_rate = 0.046
years_to_maturity = 7
current_yield = 0.053
yield_change_bp = 100  # 100个基点变动

# 1. 生成收益率网格并计算精确价格
yield_grid = np.linspace(0.02, 0.09, 100)
prices = np.array([bond_price(y, face_value, coupon_rate, years_to_maturity) for y in yield_grid])

# 2. 计算当前点的久期和凸性
mac_dur = macaulay_duration(current_yield, face_value, coupon_rate, years_to_maturity)
mod_dur = mac_dur / (1 + current_yield)
conv = convexity(current_yield, face_value, coupon_rate, years_to_maturity)
current_price = bond_price(current_yield, face_value, coupon_rate, years_to_maturity)

# 生成久期近似线和久期+凸性近似曲线
dy = yield_grid - current_yield
dur_approx = current_price * (1 - mod_dur * dy)
dur_conv_approx = current_price * (1 - mod_dur * dy + 0.5 * conv * dy**2)

# 3. 计算+100bp的精确价格和久期估计变化
new_yield = current_yield + yield_change_bp / 10000
price_up100bp = bond_price(new_yield, face_value, coupon_rate, years_to_maturity)
dur_approx_change = -mod_dur * (yield_change_bp / 10000)

# 绘图
plt.figure(figsize=(10, 6))
plt.plot(yield_grid, prices, label='精确价格-收益率曲线', color='blue')
plt.plot(yield_grid, dur_approx, '--', label='久期近似', color='red')
plt.plot(yield_grid, dur_conv_approx, '-.', label='久期+凸性近似', color='green')
plt.scatter(current_yield, current_price, color='black', zorder=5)
plt.annotate(f'当前点 ({current_yield*100:.1f}%, {current_price:.2f})',
             xy=(current_yield, current_price),
             xytext=(current_yield+0.005, current_price+5),
             arrowprops=dict(facecolor='black', shrink=0.05))

plt.title('债券价格-收益率曲线及久期近似')
plt.xlabel('收益率 (年复利)')
plt.ylabel('债券价格')
plt.gca().xaxis.set_major_formatter(PercentFormatter(1))
plt.gca().yaxis.set_major_formatter('{x:.1f}')
plt.legend()
plt.grid(True)

# 保存图形
figure_path = 'bond_price_yield_curve.png'
plt.savefig(figure_path, dpi=300, bbox_inches='tight')

# 准备结果字典
result = {
    'price_at_up100bp': price_up100bp,
    'dur_approx_change_up100bp': dur_approx_change,
    'figure_path': figure_path
}

# 输出结果以供验证
print(result)
