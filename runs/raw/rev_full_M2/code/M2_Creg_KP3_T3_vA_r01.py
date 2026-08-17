import numpy as np

def bond_price(face_value=100, coupon_rate=0.046, ytm=0.053, maturity=7, freq=1):
    """
    计算债券价格
    face_value: 面值
    coupon_rate: 票息率（年化）
    ytm: 到期收益率（年化）
    maturity: 剩余期限（年）
    freq: 每年付息次数（1为年付，2为半年付）
    """
    periods = int(maturity * freq)
    coupon = face_value * coupon_rate / freq
    ytm_period = ytm / freq
    t = np.arange(1, periods + 1)
    cash_flows = np.full(periods, coupon)
    cash_flows[-1] += face_value
    discount_factors = (1 + ytm_period) ** t
    price = np.sum(cash_flows / discount_factors)
    return price

# 参数设置
face_value = 100
coupon_rate = 0.046
ytm_initial = 0.053
maturity = 7
freq = 1  # 假设每年付息一次，若为半年付息改为2

# 计算初始价格
price_initial = bond_price(face_value, coupon_rate, ytm_initial, maturity, freq)

# 收益率上升80个基点后的新价格
ytm_new = ytm_initial + 0.008  # 80 bps = 0.8%
price_new = bond_price(face_value, coupon_rate, ytm_new, maturity, freq)

# 价格跌幅百分比（正数表示下跌）
price_drop_pct = (price_initial - price_new) / price_initial * 100

# 输出结果
result = {
    'price_drop_pct': round(price_drop_pct, 6)  # 保留6位小数，确保可复现
}

print(result)
