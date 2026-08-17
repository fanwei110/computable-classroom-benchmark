import numpy as np

def bond_price(C, F, y, T):
    price = sum([C / (1 + y)**t for t in range(1, T + 1)]) + F / (1 + y)**T
    return price

# 参数
C = 4.6
F = 100
y_current = 0.053
y_new = y_current + 0.008
T = 7

# 计算价格
P_current = bond_price(C, F, y_current, T)
P_new = bond_price(C, F, y_new, T)

# 计算跌幅
price_drop_pct = (P_current - P_new) / P_current * 100

result = {
    'price_drop_pct': price_drop_pct
}

print(result)
