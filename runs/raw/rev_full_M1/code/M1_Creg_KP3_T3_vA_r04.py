import numpy as np
from scipy.optimize import root

def calculate_bond_price(face_value, coupon_rate, yield_to_maturity, years_to_maturity, periods_per_year=2):
    """
    计算债券价格
    :param face_value: 面值
    :param coupon_rate: 票息率（年化）
    :param yield_to_maturity: 收益率（年化）
    :param years_to_maturity: 剩余期限（年）
    :param periods_per_year: 每年付息次数
    :return: 债券价格
    """
    coupon_payment = face_value * coupon_rate / periods_per_year
    total_periods = years_to_maturity * periods_per_year
    periodic_yield = yield_to_maturity / periods_per_year

    # 计算现金流的现值
    price = np.sum([coupon_payment / (1 + periodic_yield) ** t for t in range(1, int(total_periods) + 1)]) + \
            face_value / (1 + periodic_yield) ** total_periods

    return price

# 债券参数
face_value = 100
coupon_rate = 0.046
initial_yield = 0.053
years_to_maturity = 7
yield_increase_bps = 80  # 基点

# 计算初始价格
initial_price = calculate_bond_price(face_value, coupon_rate, initial_yield, years_to_maturity)

# 计算收益率上升后的价格
new_yield = initial_yield + yield_increase_bps / 10000
new_price = calculate_bond_price(face_value, coupon_rate, new_yield, years_to_maturity)

# 计算价格下跌百分比
price_drop_pct = (initial_price - new_price) / initial_price * 100

# 存储结果
result = {
    'price_drop_pct': price_drop_pct
}

print(result)
