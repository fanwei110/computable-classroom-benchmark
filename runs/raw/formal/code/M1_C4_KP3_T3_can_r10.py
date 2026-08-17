import numpy as np

# 债券参数
face_value = 100.0          # 面值
coupon_rate = 0.046         # 票息率（年）
yield_to_maturity = 0.053   # 收益率（年复利）
years_to_maturity = 7       # 剩余期限（年）
dy = 0.008                  # 收益率变动（80基点）

# 1. 计算每期现金流
periods = years_to_maturity
coupon_payment = face_value * coupon_rate
cash_flows = np.full(periods, coupon_payment)
cash_flows[-1] += face_value  # 最后一期加上面值

# 2. 计算当前价格（现金流贴现之和）
discount_factors = np.array([(1 + yield_to_maturity) ** (-t) for t in range(1, periods + 1)])
current_price = np.sum(cash_flows * discount_factors)

# 3. 计算麦考利久期
time_weights = np.array([t * cash_flows[t-1] * discount_factors[t-1] for t in range(1, periods + 1)])
macaulay_duration = np.sum(time_weights) / current_price

# 4. 计算修正久期
modified_duration = macaulay_duration / (1 + yield_to_maturity)

# 5. 套用经验法则估算价格跌幅
price_drop_pct = modified_duration * dy

# 6. 存入结果字典
result = {
    'price_drop_pct': price_drop_pct
}

# 输出结果（供课堂投屏确认）
print("当前价格:", round(current_price, 4))
print("麦考利久期:", round(macaulay_duration, 4))
print("修正久期:", round(modified_duration, 4))
print("预计价格跌幅（百分比）:", round(price_drop_pct * 100, 4), "%")
