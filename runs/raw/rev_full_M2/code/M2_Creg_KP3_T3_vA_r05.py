import numpy as np

# 债券参数
FACE_VALUE = 100.0
COUPON_RATE = 0.046          # 年票息率
YIELD_RATE = 0.053           # 初始年收益率
MATURITY = 7                 # 剩余年限
FREQUENCY = 1                # 付息频率（1=每年, 2=每半年）
YIELD_SHIFT_BPS = 80         # 收益率上升基点
YIELD_SHIFT = YIELD_SHIFT_BPS / 10000

# 计算现金流
periods = MATURITY * FREQUENCY
coupon = FACE_VALUE * COUPON_RATE / FREQUENCY
yield_period = YIELD_RATE / FREQUENCY

cash_flows = np.full(periods, coupon)
cash_flows[-1] += FACE_VALUE

# 折现因子
t = np.arange(1, periods + 1)
discount_factors = (1 + yield_period) ** -t
price = np.sum(cash_flows * discount_factors)

# 新收益率下的价格
yield_new_period = (YIELD_RATE + YIELD_SHIFT) / FREQUENCY
discount_factors_new = (1 + yield_new_period) ** -t
price_new = np.sum(cash_flows * discount_factors_new)

# 价格下跌百分比（正数表示下跌）
price_drop_pct = (price - price_new) / price * 100

# 按要求输出
result = {
    'price_drop_pct': price_drop_pct
}

print(result)
