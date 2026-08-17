import numpy as np

def bond_price(C, F, y, T):
    price = sum([C / (1 + y)**t for t in range(1, T + 1)]) + F / (1 + y)**T
    return price

# 参数
C = 4.6
F = 100
y0 = 0.053
y1 = y0 + 0.008
T = 7

# 计算价格
P0 = bond_price(C, F, y0, T)
P1 = bond_price(C, F, y1, T)

# 价格跌幅
price_drop_pct = (P0 - P1) / P0 * 100

result = {
    'price_drop_pct': price_drop_pct
}

print(result)
