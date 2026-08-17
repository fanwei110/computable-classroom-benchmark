import numpy as np

def bond_price(face_value, coupon_rate, ytm, maturity, freq=1):
    """
    计算债券价格（给定面值、票息率、到期收益率、期限和付息频率）。
    假设每年付息 freq=1，若 freq=2 为半年付息。
    """
    coupon = face_value * coupon_rate          # 年票息金额
    periods = maturity * freq                  # 总付息期数
    coupon_per_period = coupon / freq          # 每期票息
    ytm_per_period = ytm / freq                # 每期收益率
    
    # 每期现金流：最后一期包含面值
    cash_flows = np.full(periods, coupon_per_period)
    cash_flows[-1] += face_value
    
    # 期数（从 1 开始）
    t = np.arange(1, periods + 1)
    
    # 折现因子
    discounts = (1 + ytm_per_period) ** t
    
    price = np.sum(cash_flows / discounts)
    return price

# 债券参数
face_value = 100.0        # 面值
coupon_rate = 0.046       # 票息率 4.6%
ytm = 0.053               # 初始收益率 5.3%
maturity = 7              # 期限 7 年
freq = 1                  # 年付息（缺省假设）

# 初始价格
price_old = bond_price(face_value, coupon_rate, ytm, maturity, freq)

# 收益率上升 80 个基点后的新收益率与新价格
ytm_new = ytm + 0.008     # 80 bps = 0.8%
price_new = bond_price(face_value, coupon_rate, ytm_new, maturity, freq)

# 价格下跌幅度（百分比，正数表示下跌）
price_drop_pct = (price_old - price_new) / price_old * 100

# 按契约存储结果
result = {
    'price_drop_pct': price_drop_pct
}

print(result)
