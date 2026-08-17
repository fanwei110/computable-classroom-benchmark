import numpy as np

# 债券参数
face_value = 100.0          # 面值
annual_coupon_rate = 0.046  # 年票息率
yield_to_maturity = 0.053   # 年收益率（年复利）
maturity_years = 7          # 剩余期限（年）
dy = 0.008                  # 收益率变动（80个基点）

# 1. 计算每期现金流
coupon_payment = face_value * annual_coupon_rate
cash_flows = np.full(maturity_years, coupon_payment)
cash_flows[-1] += face_value  # 最后一期包含面值

# 2. 计算当前价格（现金流贴现之和）
periods = np.arange(1, maturity_years + 1)
discount_factors = (1 + yield_to_maturity) ** periods
price = np.sum(cash_flows / discount_factors)

# 3. 计算麦考利久期
weighted_cash_flows = cash_flows * periods
macaulay_duration = np.sum(weighted_cash_flows / discount_factors) / price

# 4. 计算修正久期
modified_duration = macaulay_duration / (1 + yield_to_maturity)

# 5. 套用经验法则估算价格跌幅
price_drop_pct = modified_duration * dy

# 6. 存入结果字典
result = {
    'price_drop_pct': price_drop_pct
}

# 输出结果（供课堂验证）
print(result)
