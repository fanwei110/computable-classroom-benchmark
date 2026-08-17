import numpy as np
from scipy.optimize import newton

# 债券参数
face_value = 100
coupon_rate = 0.046  # 票息率 4.6%
maturity_years = 7  # 期限 7年
ytm = 0.053  # 到期收益率 5.3%
coupon_frequency = 1  # 每年支付一次

def bond_price(ytm, face_value, coupon_rate, maturity_years, coupon_frequency=1):
    """计算债券价格"""
    n_periods = int(maturity_years * coupon_frequency)
    coupon = face_value * coupon_rate / coupon_frequency
    period_rate = ytm / coupon_frequency
    
    # 票息现值
    pv_coupons = coupon * (1 - (1 + period_rate) ** (-n_periods)) / period_rate
    # 面值现值
    pv_face = face_value / (1 + period_rate) ** n_periods
    
    return pv_coupons + pv_face

def macaulay_duration(ytm, face_value, coupon_rate, maturity_years, coupon_frequency=1):
    """计算麦考利久期"""
    n_periods = int(maturity_years * coupon_frequency)
    coupon = face_value * coupon_rate / coupon_frequency
    period_rate = ytm / coupon_frequency
    
    price = bond_price(ytm, face_value, coupon_rate, maturity_years, coupon_frequency)
    
    # 计算加权平均时间
    weighted_time = 0
    for t in range(1, n_periods + 1):
        if t < n_periods:
            cf = coupon
        else:
            cf = coupon + face_value
        
        pv_cf = cf / (1 + period_rate) ** t
        weighted_time += t * pv_cf
    
    duration_periods = weighted_time / price
    duration_years = duration_periods / coupon_frequency
    
    return duration_years

def modified_duration(macaulay_dur, ytm, coupon_frequency=1):
    """计算修正久期"""
    return macaulay_dur / (1 + ytm / coupon_frequency)

def convexity(ytm, face_value, coupon_rate, maturity_years, coupon_frequency=1):
    """计算凸性"""
    n_periods = int(maturity_years * coupon_frequency)
    coupon = face_value * coupon_rate / coupon_frequency
    period_rate = ytm / coupon_frequency
    
    price = bond_price(ytm, face_value, coupon_rate, maturity_years, coupon_frequency)
    
    # 计算凸性
    weighted_time_squared = 0
    for t in range(1, n_periods + 1):
        if t < n_periods:
            cf = coupon
        else:
            cf = coupon + face_value
        
        pv_cf = cf / (1 + period_rate) ** t
        weighted_time_squared += t * (t + 1) * pv_cf
    
    convexity_periods = weighted_time_squared / (price * (1 + period_rate) ** 2)
    convexity_years = convexity_periods / (coupon_frequency ** 2)
    
    return convexity_years

# 计算各项指标
price = bond_price(ytm, face_value, coupon_rate, maturity_years, coupon_frequency)
macaulay_dur = macaulay_duration(ytm, face_value, coupon_rate, maturity_years, coupon_frequency)
modified_dur = modified_duration(macaulay_dur, ytm, coupon_frequency)
conv = convexity(ytm, face_value, coupon_rate, maturity_years, coupon_frequency)

# 输出结果
result = {
    'price': round(price, 4),
    'macaulay_duration_years': round(macaulay_dur, 4),
    'modified_duration_years': round(modified_dur, 4),
    'convexity': round(conv, 4)
}

print("债券价格:", result['price'])
print("麦考利久期 (年):", result['macaulay_duration_years'])
print("修正久期 (年):", result['modified_duration_years'])
print("凸性:", result['convexity'])
