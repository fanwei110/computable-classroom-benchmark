import numpy as np

# 债券参数
face_value = 100
coupon_rate = 0.046
years = 7
yield_rate = 0.053

# 计算价格
def bond_price(face_value, coupon_rate, years, yield_rate):
    price = 0
    coupon = face_value * coupon_rate
    for t in range(1, years + 1):
        price += coupon / (1 + yield_rate)**t
    price += face_value / (1 + yield_rate)**years
    return price

price = bond_price(face_value, coupon_rate, years, yield_rate)

# 计算麦考利久期
def macaulay_duration(face_value, coupon_rate, years, yield_rate):
    coupon = face_value * coupon_rate
    weighted_sum = 0
    total_pv = 0
    
    for t in range(1, years + 1):
        pv = coupon / (1 + yield_rate)**t
        weighted_sum += t * pv
        total_pv += pv
    
    pv_face = face_value / (1 + yield_rate)**years
    weighted_sum += years * pv_face
    total_pv += pv_face
    
    return weighted_sum / total_pv

macaulay_duration_years = macaulay_duration(face_value, coupon_rate, years, yield_rate)

# 修正久期
modified_duration_years = macaulay_duration_years / (1 + yield_rate)

# 凸性
def convexity(face_value, coupon_rate, years, yield_rate):
    coupon = face_value * coupon_rate
    convexity_sum = 0
    total_pv = 0
    
    for t in range(1, years + 1):
        pv = coupon / (1 + yield_rate)**t
        convexity_sum += t * (t + 1) * pv
        total_pv += pv
    
    pv_face = face_value / (1 + yield_rate)**years
    convexity_sum += years * (years + 1) * pv_face
    total_pv += pv_face
    
    return convexity_sum / (total_pv * (1 + yield_rate)**2)

convexity_val = convexity(face_value, coupon_rate, years, yield_rate)

# 存储结果
result = {
    'price': round(price, 4),
    'macaulay_duration_years': round(macaulay_duration_years, 4),
    'modified_duration_years': round(modified_duration_years, 4),
    'convexity': round(convexity_val, 4)
}

print(result)
