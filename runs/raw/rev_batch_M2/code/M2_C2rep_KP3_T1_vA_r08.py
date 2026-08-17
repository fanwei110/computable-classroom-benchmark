import numpy as np

def bond_price_macaulay_modified_convexity(face, coupon_rate, maturity_years, ytm, freq=1):
    """
    计算债券价格、麦考利久期、修正久期和凸性。
    
    参数:
        face: 面值
        coupon_rate: 票息率（年化）
        maturity_years: 到期年限
        ytm: 到期收益率（年化，小数形式）
        freq: 每年付息次数（默认1，即每年付息一次）
    
    返回:
        dict: 包含价格、麦考利久期、修正久期和凸性
    """
    periods = int(maturity_years * freq)
    coupon = face * coupon_rate / freq
    # 时间点（年）
    times = np.arange(1, periods + 1) / freq
    # 现金流
    cashflows = np.full(periods, coupon)
    cashflows[-1] += face  # 最后一次还本
    
    # 每期贴现因子
    discount_factors = (1 + ytm / freq) ** (-times)
    pv_cashflows = cashflows * discount_factors
    
    # 价格
    price = np.sum(pv_cashflows)
    
    # 麦考利久期（年）
    macaulay_duration = np.sum(times * pv_cashflows) / price
    
    # 修正久期（年）
    modified_duration = macaulay_duration / (1 + ytm / freq)
    
    # 凸性
    # 凸性公式: 1/P * sum( t*(t+1/freq) * CF_t / (1+ytm/freq)^{t+2} )  (其中t以年为单位)
    # 或者等效地: 1/(P*(1+ytm/freq)^2) * sum( t*(t+1/freq) * PV(CF_t) ) 这里t是年数
    # 为与标准教科书一致，采用:
    convexity = np.sum(times * (times + 1/freq) * pv_cashflows) / (price * (1 + ytm/freq)**2)
    
    return {
        'price': price,
        'macaulay_duration_years': macaulay_duration,
        'modified_duration_years': modified_duration,
        'convexity': convexity
    }

# 债券参数
face_value = 100.0
coupon_rate = 0.046
maturity = 7
ytm = 0.053

# 计算结果
result = bond_price_macaulay_modified_convexity(
    face=face_value,
    coupon_rate=coupon_rate,
    maturity_years=maturity,
    ytm=ytm,
    freq=1
)

# 输出结果，便于课堂投屏查看
for key, value in result.items():
    print(f"{key}: {value:.6f}")

# 最终 result 字典已按要求命名
