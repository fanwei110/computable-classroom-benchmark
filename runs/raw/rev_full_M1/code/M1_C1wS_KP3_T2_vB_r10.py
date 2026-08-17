import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import root_scalar

# 债券参数
face_value = 100
coupon_rate = 0.046
years_to_maturity = 7
ytm_initial = 0.053  # 初始YTM
yield_shift = 0.01   # 100bp变动

# 现金流生成
def generate_cash_flows(face_value, coupon_rate, years_to_maturity):
    coupon_payment = face_value * coupon_rate
    cash_flows = np.full(years_to_maturity, coupon_payment)
    cash_flows[-1] += face_value  # 最后一期加上面值
    return cash_flows

cash_flows = generate_cash_flows(face_value, coupon_rate, years_to_maturity)

# 精确债券定价函数
def bond_price(yield_to_maturity, cash_flows, years_to_maturity):
    periods = np.arange(1, years_to_maturity + 1)
    present_values = cash_flows / ((1 + yield_to_maturity) ** periods)
    return np.sum(present_values)

# 久期和凸性计算
def macaulay_duration_convexity(yield_to_maturity, cash_flows, years_to_maturity):
    periods = np.arange(1, years_to_maturity + 1)
    discounted_cash_flows = cash_flows / ((1 + yield_to_maturity) ** periods)
    price = np.sum(discounted_cash_flows)

    # 麦考利久期
    weighted_cash_flows = discounted_cash_flows * periods
    mac_duration = np.sum(weighted_cash_flows) / price

    # 修正久期
    mod_duration = mac_duration / (1 + yield_to_maturity)

    # 凸性
    convexity = np.sum(discounted_cash_flows * periods * (periods + 1)) / (price * (1 + yield_to_maturity)**2)

    return mac_duration, mod_duration, convexity

# 1. 在2%到9%收益率网格上精确定价
yield_grid = np.linspace(0.02, 0.09, 100)
price_grid = np.array([bond_price(y, cash_flows, years_to_maturity) for y in yield_grid])

# 2. 在5.3%附近叠加久期近似
mac_dur, mod_dur, convexity = macaulay_duration_convexity(ytm_initial, cash_flows, years_to_maturity)

# 久期近似价格变化
def duration_approx_price(yield_change, mod_duration, current_price):
    return current_price * (1 - mod_duration * yield_change)

# 凸性调整的久期近似
def duration_convexity_approx_price(yield_change, mod_duration, convexity, current_price):
    return current_price * (1 - mod_duration * yield_change + 0.5 * convexity * (yield_change**2))

# 当前价格
current_price = bond_price(ytm_initial, cash_flows, years_to_maturity)

# 久期近似曲线
yield_approx = np.linspace(ytm_initial - 0.02, ytm_initial + 0.02, 50)
price_approx = np.array([duration_approx_price(y - ytm_initial, mod_dur, current_price) for y in yield_approx])

# 3. +100bp的精确价格与久期法估计的相对变化
ytm_up100bp = ytm_initial + yield_shift
price_up100bp_exact = bond_price(ytm_up100bp, cash_flows, years_to_maturity)
price_change_exact = (price_up100bp_exact - current_price) / current_price

# 久期法估计的价格变化
price_up100bp_dur_approx = duration_approx_price(yield_shift, mod_dur, current_price)
price_change_dur_approx = (price_up100bp_dur_approx - current_price) / current_price

# 4. 绘图并保存
plt.figure(figsize=(10, 6))
plt.plot(yield_grid, price_grid, label='Exact Price-Yield Curve', color='blue')
plt.plot(yield_approx, price_approx, '--', label='Duration Approximation', color='red')
plt.scatter(ytm_initial, current_price, color='green', zorder=5, label='Initial YTM (5.3%)')
plt.scatter(ytm_up100bp, price_up100bp_exact, color='purple', zorder=5, label='+100bp YTM')
plt.xlabel('Yield to Maturity')
plt.ylabel('Bond Price')
plt.title('Bond Price-Yield Curve with Duration Approximation')
plt.legend()
plt.grid(True)

# 保存图形
figure_path = 'bond_price_yield_curve.png'
plt.savefig(figure_path)
plt.close()

# 填充result字典
result = {
    'price_at_up100bp': price_up100bp_exact,
    'dur_approx_change_up100bp': price_change_dur_approx,
    'figure_path': figure_path
}

# 输出result以便验证
print(result)
