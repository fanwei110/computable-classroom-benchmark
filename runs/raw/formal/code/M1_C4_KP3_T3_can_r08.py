import numpy as np

# 债券参数
face_value = 100.0
coupon_rate = 0.046
yield_to_maturity = 0.053
years_to_maturity = 7
dy = 0.008  # 收益率变动（80个基点）

# 计算每期现金流（票息和本金）
coupon_payment = face_value * coupon_rate
cash_flows = np.full(years_to_maturity, coupon_payment)
cash_flows[-1] += face_value  # 最后一期包含本金

# 计算当前价格（现金流贴现之和）
periods = np.arange(1, years_to_maturity + 1)
discount_factors = (1 + yield_to_maturity) ** periods
bond_price = np.sum(cash_flows / discount_factors)

# 计算麦考利久期
weighted_cash_flows = periods * cash_flows / discount_factors
macauley_duration = np.sum(weighted_cash_flows) / bond_price

# 计算修正久期
modified_duration = macauley_duration / (1 + yield_to_maturity)

# 使用一阶近似估算价格变动百分比
price_drop_pct = modified_duration * dy

# 存储结果
result = {
    'price_drop_pct': price_drop_pct
}

print(result)
