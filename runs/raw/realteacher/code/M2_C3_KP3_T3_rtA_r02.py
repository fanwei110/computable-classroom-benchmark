# 债券参数
face_value = 100
coupon_rate = 0.046
yield_initial = 0.053
maturity = 7
delta_y = 0.008  # 80个基点

# 现金流：每年付息一次，到期还本
coupon = face_value * coupon_rate
cash_flows = [coupon] * (maturity - 1) + [coupon + face_value]

# 计算原价格
price_old = sum(cf / (1 + yield_initial) ** t for t, cf in enumerate(cash_flows, start=1))

# 计算新收益率下的价格
yield_new = yield_initial + delta_y
price_new = sum(cf / (1 + yield_new) ** t for t, cf in enumerate(cash_flows, start=1))

# 价格下跌百分比（正数表示损失）
price_drop_pct = (price_old - price_new) / price_old

result = {'price_drop_pct': price_drop_pct}
