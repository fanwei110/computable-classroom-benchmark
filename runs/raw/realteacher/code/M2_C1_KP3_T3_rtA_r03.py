# 精确计算债券价格和跌幅
face_value = 100
coupon_rate = 0.046
ytm_initial = 0.053
ytm_new = 0.061
n = 7

# 计算初始价格
coupon = face_value * coupon_rate
pv_coupons_initial = coupon * (1 - (1 + ytm_initial)**-n) / ytm_initial
pv_face_initial = face_value / (1 + ytm_initial)**n
price_initial = pv_coupons_initial + pv_face_initial

# 计算新价格
pv_coupons_new = coupon * (1 - (1 + ytm_new)**-n) / ytm_new
pv_face_new = face_value / (1 + ytm_new)**n
price_new = pv_coupons_new + pv_face_new

# 跌幅百分比
price_drop_pct = (price_initial - price_new) / price_initial * 100

result = {'price_drop_pct': round(price_drop_pct, 4)}
