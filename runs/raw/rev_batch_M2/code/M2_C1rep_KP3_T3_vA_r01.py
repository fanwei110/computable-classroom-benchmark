import numpy as np

# 债券参数
face_value = 100
coupon_rate = 0.046
ytm_original = 0.053
ytm_new = ytm_original + 0.008  # 上升80个基点
T = 7
coupon = face_value * coupon_rate

# 计算原始价格
cash_flows_original = np.array([coupon] * (T - 1) + [coupon + face_value])
times = np.arange(1, T + 1)
discount_factors_original = (1 + ytm_original) ** times
price_original = np.sum(cash_flows_original / discount_factors_original)

# 计算新价格
discount_factors_new = (1 + ytm_new) ** times
price_new = np.sum(cash_flows_original / discount_factors_new)

# 价格变动百分比
price_drop_pct = (price_new - price_original) / price_original * 100

result = {'price_drop_pct': price_drop_pct}
print(result)
