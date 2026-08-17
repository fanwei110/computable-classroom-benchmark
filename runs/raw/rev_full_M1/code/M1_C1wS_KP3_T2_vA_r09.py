import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter

# 债券参数
face_value = 100
coupon_rate = 0.046
years_to_maturity = 7
current_yield = 0.053
yield_change_bp = 100  # 100个基点变动

# 计算债券价格的函数
def bond_price(face_value, coupon_rate, years_to_maturity, yield_to_maturity):
    coupon = face_value * coupon_rate
    periods = years_to_maturity
    yield_per_period = yield_to_maturity

    # 现金流
    cash_flows = np.full(periods, coupon)
    cash_flows[-1] += face_value  # 最后一期加上面值

    # 贴现因子
    discount_factors = np.power(1 + yield_per_period, -np.arange(1, periods + 1))

    # 价格计算
    price = np.sum(cash_flows * discount_factors)
    return price

# 计算久期的函数 (Macaulay Duration)
def macaulay_duration(face_value, coupon_rate, years_to_maturity, yield_to_maturity):
    coupon = face_value * coupon_rate
    periods = years_to_maturity
    yield_per_period = yield_to_maturity

    cash_flows = np.full(periods, coupon)
    cash_flows[-1] += face_value

    discount_factors = np.power(1 + yield_per_period, -np.arange(1, periods + 1))
    discounted_cash_flows = cash_flows * discount_factors

    price = np.sum(discounted_cash_flows)
    weighted_time = np.sum(discounted_cash_flows * np.arange(1, periods + 1)) / price

    return weighted_time

# 计算修正久期
def modified_duration(macaulay_dur, yield_to_maturity):
    return macaulay_dur / (1 + yield_to_maturity)

# 1. 生成收益率网格并计算精确价格
yield_grid = np.linspace(0.02, 0.09, 100)
exact_prices = np.array([bond_price(face_value, coupon_rate, years_to_maturity, y) for y in yield_grid])

# 2. 在当前收益率附近计算久期近似
mac_dur = macaulay_duration(face_value, coupon_rate, years_to_maturity, current_yield)
mod_dur = modified_duration(mac_dur, current_yield)

# 久期近似线
approx_prices = exact_prices[np.argmin(np.abs(yield_grid - current_yield))] * (1 - mod_dur * (yield_grid - current_yield))

# 3. 计算+100bp的精确价格和久期估计变化
new_yield = current_yield + yield_change_bp / 10000
price_up100bp = bond_price(face_value, coupon_rate, years_to_maturity, new_yield)
dur_approx_change = -mod_dur * (new_yield - current_yield) * 100  # 相对变化百分比

# 4. 绘图
plt.figure(figsize=(10, 6))
plt.plot(yield_grid * 100, exact_prices, label='精确价格', color='blue')
plt.plot(yield_grid * 100, approx_prices, label='久期近似', color='red', linestyle='--')

# 标记当前点
current_price = bond_price(face_value, coupon_rate, years_to_maturity, current_yield)
plt.scatter(current_yield * 100, current_price, color='green', zorder=5)
plt.text(current_yield * 100, current_price * 0.99, f'当前点 ({current_yield*100:.1f}%, {current_price:.2f})',
         ha='center', va='top', color='green')

plt.title('债券价格与收益率关系')
plt.xlabel('收益率 (%)')
plt.ylabel('价格')
plt.legend()
plt.grid(True)

# 格式化y轴为百分比
plt.gca().xaxis.set_major_formatter(FuncFormatter(lambda x, _: f'{x:.1f}%'))

# 保存图形
figure_path = 'bond_price_duration_plot.png'
plt.savefig(figure_path, dpi=300, bbox_inches='tight')
plt.close()

# 准备结果字典
result = {
    'price_at_up100bp': price_up100bp,
    'dur_approx_change_up100bp': dur_approx_change,
    'figure_path': figure_path
}

# 输出结果以供验证
print(result)
