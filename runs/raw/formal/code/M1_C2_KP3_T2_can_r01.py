import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import newton

# 参数设定
face_value = 100
coupon_rate = 0.046
years_to_maturity = 7
current_yield = 0.053
yield_shift_bp = 100  # 可调的收益率变动幅度（基点）

# 计算票息支付频率（假设每年付息一次）
coupon_payment = face_value * coupon_rate
periods_per_year = 1
total_periods = years_to_maturity * periods_per_year

def bond_price(yield_to_maturity, face_value, coupon_payment, total_periods):
    """计算债券精确价格"""
    ytm_period = yield_to_maturity / periods_per_year
    cash_flows = np.full(total_periods, coupon_payment)
    cash_flows[-1] += face_value  # 最后一期包含本金
    periods = np.arange(1, total_periods + 1)
    price = np.sum(cash_flows / ((1 + ytm_period) ** periods))
    return price

def bond_duration(yield_to_maturity, face_value, coupon_payment, total_periods):
    """计算麦考利久期"""
    ytm_period = yield_to_maturity / periods_per_year
    cash_flows = np.full(total_periods, coupon_payment)
    cash_flows[-1] += face_value
    periods = np.arange(1, total_periods + 1)
    discounted_cash_flows = cash_flows / ((1 + ytm_period) ** periods)
    price = np.sum(discounted_cash_flows)
    weighted_cash_flows = discounted_cash_flows * periods
    macaulay_duration = np.sum(weighted_cash_flows) / price
    modified_duration = macaulay_duration / (1 + ytm_period)
    return macaulay_duration, modified_duration

def bond_convexity(yield_to_maturity, face_value, coupon_payment, total_periods):
    """计算凸性"""
    ytm_period = yield_to_maturity / periods_per_year
    cash_flows = np.full(total_periods, coupon_payment)
    cash_flows[-1] += face_value
    periods = np.arange(1, total_periods + 1)
    discounted_cash_flows = cash_flows / ((1 + ytm_period) ** periods)
    price = np.sum(discounted_cash_flows)
    convexity = np.sum(discounted_cash_flows * periods * (periods + 1)) / (price * (1 + ytm_period)**2)
    return convexity

# 1. 生成精确价格-收益率曲线
yield_grid = np.linspace(0.02, 0.09, 100)
prices_exact = np.array([bond_price(y, face_value, coupon_payment, total_periods) for y in yield_grid])

# 2. 计算当前收益率下的久期和凸性
_, mod_duration = bond_duration(current_yield, face_value, coupon_payment, total_periods)
convexity = bond_convexity(current_yield, face_value, coupon_payment, total_periods)

# 久期近似线性近似
def duration_approx(yield_change, current_price, mod_duration):
    return current_price * (1 - mod_duration * yield_change)

current_price = bond_price(current_yield, face_value, coupon_payment, total_periods)
yield_changes = np.linspace(-0.02, 0.02, 50)  # ±2% 的收益率变动
prices_approx = duration_approx(yield_changes, current_price, mod_duration)

# 3. 计算+100bp的精确价格和久期近似变化
yield_up100bp = current_yield + yield_shift_bp / 10000
price_up100bp = bond_price(yield_up100bp, face_value, coupon_payment, total_periods)
dur_approx_change = -mod_duration * (yield_shift_bp / 10000) * 100  # 相对变化百分比

# 绘图
plt.figure(figsize=(10, 6))
plt.plot(yield_grid * 100, prices_exact, label='精确价格-收益率曲线', color='blue')
plt.plot((current_yield + yield_changes) * 100, prices_approx,
         label=f'久期近似 (D={mod_duration:.2f})', color='red', linestyle='--')
plt.scatter(current_yield * 100, current_price, color='green', zorder=5, label='当前点 (5.3%)')
plt.xlabel('收益率 (%)')
plt.ylabel('债券价格')
plt.title(f'债券价格-收益率曲线 (面值={face_value}, 票息={coupon_rate*100}%, 期限={years_to_maturity}年)')
plt.legend()
plt.grid(True)

# 保存图形
figure_path = 'bond_price_yield_curve.png'
plt.savefig(figure_path)
plt.close()

# 填充结果字典
result = {
    'price_at_up100bp': price_up100bp,
    'dur_approx_change_up100bp': dur_approx_change,
    'figure_path': figure_path
}

# 输出结果（供教师查看）
print(result)
