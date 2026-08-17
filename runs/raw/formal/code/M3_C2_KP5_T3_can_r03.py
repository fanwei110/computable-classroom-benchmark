import numpy as np
from scipy.stats import norm

# ==================== 参数设定 ====================
annual_vol = 0.24          # 年化波动率 24%
position = 2700000         # 头寸金额 2,700,000 元
confidence_level = 0.95    # 置信水平 95%

# ==================== 假设处理 ====================
# 假设：一年按 252 个交易日计算（金融市场标准假设）
trading_days_per_year = 252

# ==================== 步骤 1：年化波动率换算到一日期限 ====================
# 根据平方根法则，日波动率 = 年化波动率 / sqrt(一年交易日数)
daily_vol = annual_vol / np.sqrt(trading_days_per_year)

# ==================== 步骤 2：套用 95% 正态分位数 ====================
# 使用 scipy 计算标准正态分布的 95% 分位数
z_score = norm.ppf(confidence_level)

# ==================== 步骤 3：计算 VaR 金额 ====================
# 参数法计算 VaR: 头寸金额 * 日波动率 * 正态分位数
var_95_1d_value = position * daily_vol * z_score

# ==================== 输出契约 ====================
result = {
    'var_95_1d': var_95_1d_value
}

# ==================== 课堂投屏展示 ====================
print("="*50)
print("《证券投资学》课堂实时编程：在险价值(VaR)计算")
print("="*50)
print(f"输入参数:")
print(f"  - 年化波动率: {annual_vol*100:.1f}%")
print(f"  - 头寸金额:   {position:,.2f} 元")
print(f"  - 置信水平:   {confidence_level*100:.1f}%")
print(f"内部假设:")
print(f"  - 一年交易日: {trading_days_per_year} 天")
print("-"*50)
print(f"计算步骤:")
print(f"  1. 日波动率 = {annual_vol} / sqrt({trading_days_per_year}) = {daily_vol:.6f}")
print(f"  2. 95%正态分位数 Z = {z_score:.6f}")
print(f"  3. VaR = {position:,.2f} * {daily_vol:.6f} * {z_score:.6f} = {var_95_1d_value:,.2f} 元")
print("-"*50)
print(f"最终输出字典 result: {result}")
print("="*50)
