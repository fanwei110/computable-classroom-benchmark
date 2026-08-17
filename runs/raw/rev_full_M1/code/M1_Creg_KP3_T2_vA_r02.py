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
    price = sum([coupon_payment / (1 + discount_rate)**t for t in range(1, periods + 1)])
    price += face_value / (1 + discount_rate)**periods
    return price

def calculate_duration(yield_to_maturity, face_value, coupon_rate, years_to_maturity, frequency=2):
    """
    计算麦考利久期
    """
    periods = years_to_maturity * frequency
    coupon_payment = face_value * coupon_rate / frequency
    discount_rate = yield_to_maturity / frequency

    # 计算每期现金流的现值
    cash_flows = np.array([coupon_payment] * periods)
    cash_flows[-1] += face_value  # 最后一期加上面值

    present_values = cash_flows / (1 + discount_rate)**np.arange(1, periods + 1)
    bond_price = np.sum(present_values)

    # 计算久期
    weighted_times = np.arange(1, periods + 1) * present_values
    macaulay_duration = np.sum(weighted_times) / bond_price / frequency  # 转换为年

    # 修正久期
    modified_duration = macaulay_duration / (1 + yield_to_maturity / frequency)
    return modified_duration

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
    duration = calculate_duration(current_yield, face_value, coupon_rate, years_to_maturity)

    # 生成收益率范围
    yield_range = np.linspace(0.02, 0.09, 100)
    exact_prices = [calculate_bond_price(y, face_value, coupon_rate, years_to_maturity) for y in yield_range]

    # 久期近似价格
    approx_prices = [current_price * (1 - duration * (y - current_yield)) for y in yield_range]

    # 计算收益率上升100bp后的精确价格
    new_yield = current_yield + yield_change_bp / 10000
    price_at_up100bp = calculate_bond_price(new_yield, face_value, coupon_rate, years_to_maturity)

    # 久期法估计的相对价格变化
    dur_approx_change_up100bp = -duration * (yield_change_bp / 10000) * 100  # 百分比变化

    # 绘图
    plt.figure(figsize=(10, 6))
    plt.plot(yield_range * 100, exact_prices, label='精确价格', color='blue')
    plt.plot(yield_range * 100, approx_prices, label=f'久期近似 (Δ={yield_change_bp}bp)', color='red', linestyle='--')
    plt.scatter(current_yield * 100, current_price, color='green', zorder=5)
    plt.text(current_yield * 100, current_price * 0.99, f'当前点\n({current_yield*100:.1f}%, {current_price:.2f})',
             ha='center', va='top', bbox=dict(facecolor='white', alpha=0.8))
    plt.xlabel('收益率 (%)')
    plt.ylabel('债券价格')
    plt.title(f'债券价格-收益率曲线 (票息={coupon_rate*100}%, 期限={years_to_maturity}年)')
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
