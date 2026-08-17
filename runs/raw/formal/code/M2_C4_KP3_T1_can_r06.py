import numpy as np

def bond_metrics(face=100, coupon_rate=0.046, maturity=7, ytm=0.053):
    """
    计算债券价格、麦考利久期、修正久期和凸性
    约定：面值100元，票息每年支付一次，到期一次还本，估值点在付息日
    """
    # 现金流时间点 1 到 maturity
    t = np.arange(1, maturity + 1, dtype=float)
    # 票息现金流
    coupon = face * coupon_rate
    cf = np.full(maturity, coupon)
    cf[-1] += face  # 最后一年加上面值
    
    # 贴现因子
    discount = (1 + ytm) ** t
    pv = cf / discount
    
    # 价格
    price = np.sum(pv)
    
    # 麦考利久期 = Σ (t * pv) / price
    macaulay_duration = np.sum(t * pv) / price
    
    # 修正久期 = 麦考利久期 / (1 + ytm)
    modified_duration = macaulay_duration / (1 + ytm)
    
    # 凸性 = Σ [t*(t+1)*cf / (1+ytm)^(t+2)] / price
    discount_convex = (1 + ytm) ** (t + 2)
    convexity = np.sum(t * (t + 1) * cf / discount_convex) / price
    
    return price, macaulay_duration, modified_duration, convexity

if __name__ == "__main__":
    price, mac_dur, mod_dur, conv = bond_metrics()
    
    result = {
        'price': round(price, 6),                     # 保留足够精度，避免浮点琐碎差异
        'macaulay_duration_years': round(mac_dur, 6),
        'modified_duration_years': round(mod_dur, 6),
        'convexity': round(conv, 6)
    }
    
    # 输出结果，便于课堂投屏查看
    for k, v in result.items():
        print(f"{k}: {v}")
