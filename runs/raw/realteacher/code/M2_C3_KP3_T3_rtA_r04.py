import numpy as np

# 债券参数
face_value = 100
coupon_rate = 0.046
ytm = 0.053
years = 7
dy = 0.008  # 80个基点

# 计算初始价格（年复利）
coupon = face_value * coupon_rate
t = np.arange(1, years + 1)
pv_coupons = np.sum(coupon / (1 + ytm)**t)
pv_face = face_value / (1 + ytm)**years
initial_price = pv_coupons + pv_face

# 计算新收益率下的价格
new_ytm = ytm + dy
pv_coupons_new = np.sum(coupon / (1 + new_ytm)**t)
pv_face_new = face_value / (1 + new_ytm)**years
new_price = pv_coupons_new + pv_face_new

# 价格跌幅百分比
price_drop_pct = (initial_price - new_price) / initial_price * 100

result = {'price_drop_pct': price_drop_pct}
print(result)
