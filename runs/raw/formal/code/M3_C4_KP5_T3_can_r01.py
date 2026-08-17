import numpy as np
from scipy.stats import norm

# ==================
# 已知参数设定
# ==================
annual_vol = 0.24          # 年化波动率 (小数表示)
position = 2700000         # 头寸金额 (人民币元)
trading_days = 252         # 每年交易日数
confidence_level = 0.95    # 置信水平

# ==================
# 步骤 1: 去年化波动率到一日
# ==================
daily_vol = annual_vol / np.sqrt(trading_days)

# ==================
# 步骤 2: 获取单尾 95% 正态分位数 (均值取零)
# ==================
z_score = norm.ppf(confidence_level)

# ==================
# 步骤 3: 计算 VaR 并作为正的损失金额存入字典
# ==================
var_95_1d = position * z_score * daily_vol

# 严格按契约存入字典
result = {'var_95_1d': var_95_1d}

# 投屏展示计算结果
print(f"日波动率: {daily_vol:.6f}")
print(f"95%正态分位数: {z_score:.6f}")
print(f"95% 一日 VaR: {var_95_1d:.2f} 元")
print(f"result字典: {result}")
