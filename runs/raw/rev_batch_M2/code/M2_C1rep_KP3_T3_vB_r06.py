# 计算那只7年期债券（面值100，票息率4.6%，到期收益率5.3%）在收益率上升80个基点时的价格下跌百分比
face_value = 100
coupon_rate = 0.046
yield_initial = 0.053
n = 7
coupon = face_value * coupon_rate

# 初始价格
pv_factors_initial = [1 / (1 + yield_initial)**t for t in range(1, n+1)]
pv_coupons_initial = sum(coupon * pv for pv in pv_factors_initial)
pv_face_initial = face_value / (1 + yield_initial)**n
price_initial = pv_coupons_initial + pv_face_initial

# 新收益率
yield_new = yield_initial + 0.008
pv_factors_new = [1 / (1 + yield_new)**t for t in range(1, n+1)]
pv_coupons_new = sum(coupon * pv for pv in pv_factors_new)
pv_face_new = face_value / (1 + yield_new)**n
price_new = pv_coupons_new + pv_face_new

price_drop_pct = (price_initial - price_new) / price_initial * 100

result = {'price_drop_pct': round(price_drop_pct, 2)}
