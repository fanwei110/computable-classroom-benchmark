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
    cash_flows = np.full(total_periods, coupon_payment)
    cash_flows[-1] += face_value  # 最后一期包含本金

    price = np.sum(cash_flows / (1 + periodic_yield) ** np.arange(1, total_periods + 1))
    return price

# 债券参数
face_value = 100
coupon_rate = 0.046
initial_yield = 0.053
years_to_maturity = 7
yield_increase_bps = 80  # 基点变化

# 计算初始价格
initial_price = calculate_bond_price(
    face_value=face_value,
    coupon_rate=coupon_rate,
    yield_to_maturity=initial_yield,
    years_to_maturity=years_to_maturity
)

# 计算收益率上升后的价格
new_yield = initial_yield + yield_increase_bps / 10000
new_price = calculate_bond_price(
    face_value=face_value,
    coupon_rate=coupon_rate,
    yield_to_maturity=new_yield,
    years_to_maturity=years_to_maturity
)

# 计算价格下跌百分比
price_drop_pct = (initial_price - new_price) / initial_price * 100

# 存储结果
result = {
    'price_drop_pct': price_drop_pct
}

# 输出结果（可选，便于查看）
print(f"初始价格: {initial_price:.4f}")
print(f"新价格: {new_price:.4f}")
print(f"价格下跌百分比: {price_drop_pct:.4f}%")
print("结果已存入 result 字典")
