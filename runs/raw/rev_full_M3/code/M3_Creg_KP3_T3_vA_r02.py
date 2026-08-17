import numpy as np

def calculate_bond_price(face_value, coupon_rate, ytm, maturity, freq=1):
    """
    基于贴现现金流计算债券价格
    :param face_value: 面值
    :param coupon_rate: 票息率（年化）
    :param ytm: 到期收益率（年化）
    :param maturity: 期限（年）
    :param freq: 付息频率（次/年），默认为1（按年付息）
    :return: 债券价格
    """
    periods = int(maturity * freq)
    coupon_per_period = face_value * coupon_rate / freq
    discount_rate_per_period = ytm / freq
    
    # 生成时间点数组
    times = np.arange(1, periods + 1)
    
    # 生成现金流数组（每期票息，最后一期加上面值）
    cash_flows = np.full(periods, coupon_per_period)
    cash_flows[-1] += face_value
    
    # 折现计算现值
    pv_cash_flows = cash_flows / (1 + discount_rate_per_period) ** times
    return np.sum(pv_cash_flows)

# ==================== 债券参数设定 ====================
face_value = 100.0
coupon_rate = 0.046
ytm_initial = 0.053
maturity = 7

# 收益率变动：上升 80 个基点
yield_change_bps = 80
yield_change = yield_change_bps / 10000.0  # 0.008

# 假设付息频率为每年1次（若无特殊说明，基础金融题默认按年付息）
freq = 1 

# ==================== 价格与跌幅计算 ====================
# 1. 计算初始价格
price_initial = calculate_bond_price(face_value, coupon_rate, ytm_initial, maturity, freq)

# 2. 计算收益率上升 80bps 后的新价格
ytm_new = ytm_initial + yield_change
price_new = calculate_bond_price(face_value, coupon_rate, ytm_new, maturity, freq)

# 3. 计算价格跌幅百分比（精确变动，相比久期近似更为准确）
price_drop_pct = (price_new - price_initial) / price_initial

# ==================== 输出契约封装 ====================
result = {
    'price_drop_pct': price_drop_pct
}

# ==================== 可选：终端验证打印 ====================
if __name__ == "__main__":
    print(f"初始到期收益率: {ytm_initial:.2%}")
    print(f"初始价格: {price_initial:.4f}")
    print(f"新到期收益率: {ytm_new:.2%}")
    print(f"新价格: {price_new:.4f}")
    print(f"价格大概跌幅: {price_drop_pct:.4%}")
    print(f"\n输出契约 result: {result}")
