import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import PercentFormatter

# 债券参数
face_value = 100
coupon_rate = 0.046
years_to_maturity = 7
current_yield = 0.053
yield_change_bp = 100  # 100个基点变动

# 计算债券价格的函数
def bond_price(yield_to_maturity, face_value, coupon_rate, years_to_maturity):
    coupon_payment = face_value * coupon_rate
    periods = years_to_maturity
    price = sum([coupon_payment / (1 + yield_to_maturity) ** t for t in range(1, periods + 1)]) + \
            face_value / (1 + yield_to_maturity) ** periods
    return price

# 计算久期的函数 (Macaulay Duration)
def macaulay_duration(yield_to_maturity, face_value, coupon_rate, years_to_maturity):
    coupon_payment = face_value * coupon_rate
    periods = years_to_maturity
    cash_flows = [coupon_payment] * periods
    cash_flows[-1] += face_value  # 最后一期加上面值

    weighted_cash_flows = [t * cf / (1 + yield_to_maturity) ** t for t, cf in enumerate(cash_flows, 1)]
    price = sum([cf / (1 + yield_to_maturity) ** t for t, cf in enumerate(cash_flows, 1)])
    duration = sum(weighted_cash_flows) / price
    return duration

# 计算修正久期 (Modified Duration)
def modified_duration(yield_to_maturity, face_value, coupon_rate, years_to_maturity):
    mac_dur = macaulay_duration(yield_to_maturity, face_value, coupon_rate, years_to_maturity)
    mod_dur = mac_dur / (1 + yield_to_maturity)
    return mod_dur

# 1. 在2%到9%的收益率网格上定价
yield_grid = np.linspace(0.02, 0.09, 100)
price_grid = np.array([bond_price(y, face_value, coupon_rate, years_to_maturity) for y in yield_grid])

# 2. 在5.3%附近叠加久期近似
mod_dur = modified_duration(current_yield, face_value, coupon_rate, years_to_maturity)
price_at_current = bond_price(current_yield, face_value, coupon_rate, years_to_maturity)
approx_price_grid = price_at_current * (1 - mod_dur * (yield_grid - current_yield))

# 3. 报告+100bp的精确价格与久期法估计的相对变化
yield_up100bp = current_yield + yield_change_bp / 10000
price_at_up100bp = bond_price(yield_up100bp, face_value, coupon_rate, years_to_maturity)
dur_approx_change_up100bp = -mod_dur * (yield_up100bp - current_yield) * 100  # 百分比变化

# 绘图
plt.figure(figsize=(10, 6))
plt.plot(yield_grid * 100, price_grid, label='精确价格', color='blue')
plt.plot(yield_grid * 100, approx_price_grid, label='久期近似', color='red', linestyle='--')
plt.scatter(current_yield * 100, price_at_current, color='green', zorder=5, label='当前点 (5.3%)')
plt.xlabel('收益率 (%)')
plt.ylabel('债券价格')
plt.title('债券价格与收益率关系 (久期近似 vs 精确价格)')
plt.legend()
plt.grid(True)
plt.gca().xaxis.set_major_formatter(PercentFormatter())

# 保存图形
figure_path = 'bond_price_duration_approximation.png'
plt.savefig(figure_path)
plt.close()

# 填充result字典
result = {
    'price_at_up100bp': price_at_up100bp,
    'dur_approx_change_up100bp': dur_approx_change_up100bp,
    'figure_path': figure_path
}

# 输出结果（供教师查看）
print(result)
