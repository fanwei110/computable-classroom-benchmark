import numpy as np
import scipy.optimize as opt
import pandas as pd
import matplotlib.pyplot as plt

# 债券参数
face_value = 100.0        # 面值
coupon_rate = 0.046       # 票息率（年化）
yield_initial = 0.053     # 初始到期收益率
yield_shift = 0.008       # 收益率上升 80 个基点，即 0.008
n_periods = 7             # 期限（年）
# 假设每年付息一次
coupon = face_value * coupon_rate  # 年票息

def bond_price(ytm, n, c, fv):
    """计算债券价格（年付息）"""
    periods = np.arange(1, n + 1)
    pv_coupons = np.sum(c / (1 + ytm) ** periods)
    pv_face = fv / (1 + ytm) ** n
    return pv_coupons + pv_face

# 计算初始价格
price_initial = bond_price(yield_initial, n_periods, coupon, face_value)

# 计算收益率上升后的价格
yield_new = yield_initial + yield_shift
price_new = bond_price(yield_new, n_periods, coupon, face_value)

# 价格下跌百分比（正值表示下跌幅度）
price_drop_pct = (price_initial - price_new) / price_initial * 100

# 将结果存入字典
result = {
    'price_drop_pct': price_drop_pct
}

# 输出结果（便于查看）
print(result)
