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
def bond_price(yield_to_maturity, face_value, coupon_rate, years_to_maturity):
    coupon = face_value * coupon_rate
    periods = years_to_maturity
    cash_flows = np.array([coupon] * periods + [face_value + coupon])
    discount_factors = (1 + yield_to_maturity) ** np.arange(1, periods + 2)
    price = np.sum(cash_flows / discount_factors)
    return price

# 计算久期的函数 (Macaulay Duration)
def macaulay_duration(yield_to_maturity, face_value, coupon_rate, years_to_maturity):
    coupon = face_value * coupon_rate
    periods = years_to_maturity
    cash_flows = np.array([coupon] * periods + [face_value + coupon])
    discount_factors = (1 + yield_to_maturity) ** np.arange(1, periods + 2)
    discounted_cash_flows = cash_flows / discount_factors
    weights = discounted_cash_flows / np.sum(discounted_cash_flows)
    time_periods = np.arange(1, periods + 2)
    duration = np.sum(weights * time_periods)
    return duration

# 计算修正久期 (Modified Duration)
def modified_duration(yield_to_maturity, face_value, coupon_rate, years_to_maturity):
    mac_dur = macaulay_duration(yield_to_maturity, face_value, coupon_rate, years_to_maturity)
    mod_dur = mac_dur / (1 + yield_to_maturity)
    return mod_dur

# 1. 在2%到9%的收益率网格上计算精确价格
yield_grid = np.linspace(0.02, 0.09, 100)
exact_prices = np.array([bond_price(y, face_value, coupon_rate, years_to_maturity) for y in yield_grid])

# 2. 在5.3%附近叠加久期近似
mod_dur = modified_duration(current_yield, face_value, coupon_rate, years_to_maturity)
approx_prices = bond_price(current_yield, face_value, coupon_rate, years_to_maturity) * (1 - mod_dur * (yield_grid - current_yield))

# 3. 报告+100bp的精确价格和久期法估计的相对变化
new_yield_up100bp = current_yield + yield_change_bp / 10000
price_at_up100bp = bond_price(new_yield_up100bp, face_value, coupon_rate, years_to_maturity)
dur_approx_change_up100bp = -mod_dur * (yield_change_bp / 10000) * 100  # 相对变化百分比

# 绘图
plt.figure(figsize=(10, 6))
plt.plot(yield_grid * 100, exact_prices, label='Exact Price', color='blue')
plt.plot(yield_grid * 100, approx_prices, label='Duration Approximation', color='red', linestyle='--')
plt.scatter(current_yield * 100, bond_price(current_yield, face_value, coupon_rate, years_to_maturity),
            color='green', zorder=5, label='Current Yield (5.3%)')
plt.xlabel('Yield to Maturity (%)')
plt.ylabel('Bond Price')
plt.title('Bond Price vs Yield to Maturity')
plt.legend()
plt.grid(True)

# 格式化y轴为货币格式
plt.gca().yaxis.set_major_formatter(FuncFormatter(lambda x, _: f'${x:,.2f}'))

# 保存图形
figure_path = 'bond_price_duration_approximation.png'
plt.savefig(figure_path, dpi=300, bbox_inches='tight')
plt.close()

# 填充result字典
result = {
    'price_at_up100bp': price_at_up100bp,
    'dur_approx_change_up100bp': dur_approx_change_up100bp,
    'figure_path': figure_path
}

# 输出结果以供验证
print(result)
