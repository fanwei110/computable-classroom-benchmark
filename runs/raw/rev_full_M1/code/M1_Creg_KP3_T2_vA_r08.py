import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import newton
import os

def calculate_bond_price(yield_to_maturity, face_value, coupon_rate, years_to_maturity, periods_per_year=2):
    """
    计算债券精确价格
    """
    coupon_payment = face_value * coupon_rate / periods_per_year
    total_periods = years_to_maturity * periods_per_year
    discount_rate = yield_to_maturity / periods_per_year

    # 现金流现值
    cash_flows = np.full(total_periods, coupon_payment)
    cash_flows[-1] += face_value  # 最后一期加上面值

    price = np.sum(cash_flows / (1 + discount_rate) ** np.arange(1, total_periods + 1))
    return price

def calculate_duration(yield_to_maturity, face_value, coupon_rate, years_to_maturity, periods_per_year=2):
    """
    计算麦考利久期
    """
    coupon_payment = face_value * coupon_rate / periods_per_year
    total_periods = years_to_maturity * periods_per_year
    discount_rate = yield_to_maturity / periods_per_year

    cash_flows = np.full(total_periods, coupon_payment)
    cash_flows[-1] += face_value

    # 计算每期现金流的现值
    present_values = cash_flows / (1 + discount_rate) ** np.arange(1, total_periods + 1)
    total_price = np.sum(present_values)

    # 计算久期
    time_periods = np.arange(1, total_periods + 1)
    weighted_cash_flows = time_periods * present_values
    macaulay_duration = np.sum(weighted_cash_flows) / total_price / periods_per_year

    # 修正久期
    modified_duration = macaulay_duration / (1 + yield_to_maturity / periods_per_year)
    return macaulay_duration, modified_duration

def main():
    # 债券参数
    face_value = 100
    coupon_rate = 0.046
    years_to_maturity = 7
    current_yield = 0.053
    yield_change_bp = 100  # 基点变动幅度（可调）

    # 计算当前价格
    current_price = calculate_bond_price(current_yield, face_value, coupon_rate, years_to_maturity)

    # 计算久期
    _, modified_duration = calculate_duration(current_yield, face_value, coupon_rate, years_to_maturity)

    # 收益率范围
    yields = np.linspace(0.02, 0.09, 200)
    prices = np.array([calculate_bond_price(y, face_value, coupon_rate, years_to_maturity) for y in yields])

    # 久期近似
    delta_y = 0.0001  # 微小变动用于近似
    price_up = calculate_bond_price(current_yield + delta_y, face_value, coupon_rate, years_to_maturity)
    price_down = calculate_bond_price(current_yield - delta_y, face_value, coupon_rate, years_to_maturity)
    duration_approx_prices = current_price * (1 - modified_duration * (yields - current_yield))

    # 计算收益率上升100基点后的精确价格
    yield_up_100bp = current_yield + yield_change_bp / 10000
    price_at_up100bp = calculate_bond_price(yield_up_100bp, face_value, coupon_rate, years_to_maturity)

    # 久期法估计的相对价格变化
    dur_approx_change_up100bp = -modified_duration * (yield_change_bp / 10000) * 100

    # 绘图
    plt.figure(figsize=(10, 6))
    plt.plot(yields * 100, prices, label='精确价格-收益率曲线', color='blue')
    plt.plot(yields * 100, duration_approx_prices, '--', label='久期近似', color='red')
    plt.scatter(current_yield * 100, current_price, color='green', zorder=5, label='当前收益率点')
    plt.xlabel('收益率 (%)')
    plt.ylabel('债券价格')
    plt.title(f'债券价格-收益率曲线 (收益率变动幅度: {yield_change_bp}基点)')
    plt.legend()
    plt.grid(True)

    # 保存图片
    figure_path = 'bond_price_yield_curve.png'
    plt.savefig(figure_path)
    plt.close()

    # 准备结果
    result = {
        'price_at_up100bp': price_at_up100bp,
        'dur_approx_change_up100bp': dur_approx_change_up100bp,
        'figure_path': os.path.abspath(figure_path)
    }

    return result

# 执行并输出结果
result = main()
print(result)
