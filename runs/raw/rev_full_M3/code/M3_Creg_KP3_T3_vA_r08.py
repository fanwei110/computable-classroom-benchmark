import numpy as np

# --- 债券基本参数 ---
face_value = 100           # 面值
coupon_rate = 0.046        # 票息率 4.6%
maturity = 7               # 期限 7年
initial_yield = 0.053      # 初始收益率 5.3%
yield_change_bps = 80      # 收益率上升 80 个基点

# --- 计算准备 ---
yield_change = yield_change_bps / 10000  # 将基点转换为小数 (0.008)
periods = np.arange(1, maturity + 1)     # 产生 [1, 2, 3, 4, 5, 6, 7]
coupon_payment = face_value * coupon_rate

# 构建现金流序列：前6期为票息，第7期为票息+本金
cash_flows = np.full(maturity, coupon_payment)
cash_flows[-1] += face_value

# --- 债券定价函数 ---
def calculate_bond_price(ytm, cash_flows, periods):
    """
    根据给定的收益率(ytm)对现金流进行折现，计算债券价格
    """
    discount_factors = (1 + ytm) ** periods
    present_values = cash_flows / discount_factors
    return np.sum(present_values)

# --- 计算初始与变动后的价格 ---
price_initial = calculate_bond_price(initial_yield, cash_flows, periods)
new_yield = initial_yield + yield_change
price_new = calculate_bond_price(new_yield, cash_flows, periods)

# --- 计算价格大概下跌百分比 ---
# (初始价格 - 新价格) / 初始价格
price_drop_pct = (price_initial - price_new) / price_initial

# --- 输出契约：按要求存入字典 ---
result = {
    'price_drop_pct': price_drop_pct
}

if __name__ == "__main__":
    print(f"初始收益率: {initial_yield:.3%}")
    print(f"变动后收益率: {new_yield:.3%}")
    print(f"初始价格: {price_initial:.4f}")
    print(f"变动后价格: {price_new:.4f}")
    print(f"价格下跌百分比: {price_drop_pct:.4%}")
    print("Result:", result)
