import numpy as np
from scipy.stats import norm

# 参数
vol_annual = 0.24
position = 2700000
confidence = 0.95
T = 252

# 计算
z_score = norm.ppf(1 - confidence)  # 左尾分位数（负数）
z_score_abs = abs(z_score)          # VaR 报告为正的损失
vol_daily = vol_annual / np.sqrt(T)
var_pct = z_score_abs * vol_daily
var_amount = position * var_pct

result = {'var_95_1d': round(var_amount, 2)}
