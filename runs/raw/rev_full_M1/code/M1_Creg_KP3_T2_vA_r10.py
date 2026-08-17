import numpy as np
from scipy.optimize import newton
import matplotlib.pyplot as plt
import os

def calculate_bond_price(yield_to_maturity, face_value, coupon_rate, years_to_maturity, frequency=2):
    """
    计算债券精确价格
    """
    periods = years_to_maturity * frequency
    coupon_payment = face_value * coupon_rate / frequency
    discount_rate = yield_to_maturity / frequency

    # 现金流折现
    price = sum([coupon_payment / (1 + discount_rate) ** t for t in range(1, periods + 1)])
    price += face_value / (1 + discount_rate) ** periods
    return price

def calculate_duration(yield_to_maturity, face_value, coupon_rate, years_to_maturity, frequency=2):
    """
    计算麦考利久期
    """
    periods = years_to_maturity * frequency
    coupon_payment = face_value * coupon_rate / frequency
    discount_rate = yield_to_maturity / frequency

    # 计算每期现金流的现值
    cash_flows = [coupon_payment] * periods
    cash_flows[-1] += face_value  # 最后一期加上面值

    present_values = [cf / (1 + discount_rate) ** t for t, cf in enumerate(cash_flows, 1)]
    bond_price = sum(present_values)

    # 计算久期
    duration = sum([t * pv for t, pv in zip(range(1, periods + 1), present_values)]) / bond_price
    duration /= frequency  # 转换为年化久期

    return duration

def calculate_modified_duration(macaulay_duration, yield_to_maturity, frequency=2):
    """
    计算修正久期
    """
    return macaulay_duration / (1 + yield_to_maturity / frequency)

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
    mac_duration = calculate_duration(current_yield, face_value, coupon_rate, years_to_maturity)
    mod_duration = calculate_modified_duration(mac_duration, current_yield)

    # 收益率范围
    yields = np.linspace(0.02, 0.09, 100)
    exact_prices = [calculate_bond_price(y, face_value, coupon_rate, years_to_maturity) for y in yields]

    # 久期近似
    approx_prices = [current_price * (1 - mod_duration * (y - current_yield)) for y in yields]

    # 计算收益率上升100bp后的精确价格
    new_yield = current_yield + yield_change_bp / 10000
    price_at_up100bp = calculate_bond_price(new_yield, face_value, coupon_rate, years_to_maturity)

    # 久期法估计的相对价格变化
    dur_approx_change_up100bp = -mod_duration * (yield_change_bp / 10000) * 100

    # 绘图
    plt.figure(figsize=(10, 6))
    plt.plot(yields * 100, exact_prices, label='精确价格', color='blue')
    plt.plot(yields * 100, approx_prices, label='久期近似', color='red', linestyle='--')

    # 标记当前点
    plt.scatter(current_yield * 100, current_price, color='green', zorder=5)
    plt.annotate(f'当前点 ({current_yield*100:.1f}%, {current_price:.2f})',
                 xy=(current_yield * 100, current_price),
                 xytext=(current_yield * 100 + 0.5, current_price - 5),
                 arrowprops=dict(facecolor='black', shrink=0.05))

    plt.title('债券价格-收益率曲线')
    plt.xlabel('收益率 (%)')
    plt.ylabel('价格')
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

# 运行并输出结果
result = main()
print(result)
