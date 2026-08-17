import numpy as np
from scipy.stats import norm

# ==================== 给定参数 ====================
annual_vol = 0.24            # 年化波动率 (24%)
position   = 2_700_000.0     # 头寸金额 (人民币)
trading_days = 252           # 每年交易日
confidence = 0.95            # 置信水平

# ==================== 1. 波动率去年化 ====================
# 日波动率 = 年化波动率 / sqrt(252)
daily_vol = annual_vol / np.sqrt(trading_days)

# ==================== 2. 单尾正态分位数 ====================
# 95%置信度下对应的标准正态分位数 (均值取零)
z_score = norm.ppf(confidence)   # 约 1.64485

# ==================== 3. 计算 VaR (正损失金额) ====================
var_95_1d = position * daily_vol * z_score

# ==================== 输出 ====================
result = {'var_95_1d': var_95_1d}
print(result)
