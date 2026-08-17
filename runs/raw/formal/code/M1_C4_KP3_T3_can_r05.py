import numpy as np

# 债券参数
face_value = 100.0          # 面值
coupon_rate = 0.046         # 票息率 4.6%
yield_to_maturity = 0.053   # 收益率 5.3%
years_to_maturity = 7       # 剩余期限 7 年
frequency = 1               # 年付息一次（年复利）

# 计算每期现金流
coupon_payment = face_value * coupon_rate
cash_flows = np.full(years_to_maturity, coupon_payment)
cash_flows[-1] += face_value  # 最后一期加上面值

# 计算当前价格 P
periods = np.arange(1, years_to_maturity + 1)
discount_factors = (1 + yield_to_maturity) ** periods
price = np.sum(cash_flows / discount_factors)

# 计算麦考利久期
weighted_cash_flows = cash_flows * periods / discount_factors
macaulay_duration = np.sum(weighted_cash_flows) / price

# 计算修正久期
modified_duration = macaulay_duration / (1 + yield_to_maturity)

# 收益率变动 dy = 80 个基点 = 0.008
dy = 0.008

# 估算价格跌幅（正数表示跌幅）
price_drop_pct = modified_duration * dy

# 存入结果字典
result = {
    'price_drop_pct': price_drop_pct
}
