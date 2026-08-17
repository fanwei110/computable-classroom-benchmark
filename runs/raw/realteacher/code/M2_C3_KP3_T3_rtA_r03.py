import numpy as np

# 债券参数
face_value = 100
coupon_rate = 0.046
years = 7
ytm_initial = 0.053
ytm_change = 0.008  # 80个基点
ytm_new = ytm_initial + ytm_change

# 现金流：每年票息，最后一年加上本金
times = np.arange(1, years + 1)
cash_flows = np.full(years, face_value * coupon_rate)
cash_flows[-1] += face_value

# 计算价格：按年复利折现
def bond_price(ytm):
    discounts = (1 + ytm) ** times
    return np.sum(cash_flows / discounts)

P0 = bond_price(ytm_initial)
P1 = bond_price(ytm_new)

# 跌幅百分比，正数表示价格下跌的百分比
price_drop_pct = (P0 - P1) / P0 * 100

# 结果保留两位小数
result = {'price_drop_pct': round(price_drop_pct, 2)}
print(result)
