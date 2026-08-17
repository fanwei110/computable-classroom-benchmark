import numpy as np
from scipy.stats import norm

# --- 参数设定 ---
vol_annual = 0.24          # 年化波动率 24%
position = 2700000         # 头寸 270万
confidence = 0.95          # 95% 置信水平
# 假设：业界标准的一年交易日为 252 天，用于年化转日化的平方根法则
trading_days = 252        

# --- 步骤1：把年化波动率换算到一日期限 ---
# 根据平方根法则：日波动率 = 年化波动率 / sqrt(一年交易日)
vol_daily = vol_annual / np.sqrt(trading_days)

# --- 步骤2：套用 95% 正态分位数 ---
# 使用 Delta-Normal（参数法），获取标准正态分布的 95% 分位数
z_score = norm.ppf(confidence)

# --- 步骤3：计算 VaR 金额并存入 result ---
# VaR = 头寸绝对金额 × 日波动率 × 正态分位数
var_95_1d = position * vol_daily * z_score

# 按照输出契约存入字典
result = {
    'var_95_1d': var_95_1d
}

# ================== 课堂展示用打印 ==================
print(f"【计算参数】")
print(f"  年化波动率: {vol_annual:.2%}")
print(f"  一年交易日: {trading_days} 天 (行业惯例)")
print(f"  头寸金额: {position:,.0f}")
print(f"  置信水平: {confidence:.0%}\n")

print(f"【计算步骤】")
print(f"  1. 日波动率 = {vol_annual} / sqrt({trading_days}) = {vol_daily:.6f}")
print(f"  2. 95%正态分位数 Z = {z_score:.6f}")
print(f"  3. VaR = {position:,.0f} × {vol_daily:.6f} × {z_score:.6f} = {var_95_1d:,.2f}\n")

print(f"【输出契约结果】")
print(f"  result = {result}")
