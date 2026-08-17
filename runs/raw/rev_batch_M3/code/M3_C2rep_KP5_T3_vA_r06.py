import numpy as np
from scipy.stats import norm

# ================== 参数设置 ==================
annual_vol = 0.24          # 年化波动率 24%
position = 2700000         # 头寸金额 2,700,000 元

# 假设：金融市场通常按一年 252 个交易日计算
# 题目未指明，此处采用 252 天作为时间尺度换算基础
trading_days_per_year = 252

# ================== 计算步骤 ==================

# 步骤1：将年化波动率换算到一日期限
# 根据独立同分布假设下的“时间平方根法则”，日波动率 = 年化波动率 / sqrt(交易天数)
daily_vol = annual_vol / np.sqrt(trading_days_per_year)

# 步骤2：套用 95% 正态分位数
# 计算 95% 置信水平下的单尾正态分布分位数（即左尾 5% 对应的临界值的绝对值）
z_95 = norm.ppf(0.95)

# 步骤3：计算 95% 一日 VaR
# 参数法: VaR = 头寸绝对值 × 日波动率 × 分位数
var_95_1d = position * daily_vol * z_95

# ================== 输出契约 ==================
result = {
    'var_95_1d': var_95_1d
}

# 投屏展示中间过程与最终结果
print(f"1. 年化波动率 {annual_vol*100:.0f}% 换算为日波动率: {daily_vol*100:.4f}%")
print(f"2. 95% 正态分位数 Z值: {z_95:.4f}")
print(f"3. 95% 一日 VaR 金额: {var_95_1d:,.2f} 元")
print(f"\n输出字典 result: {result}")
