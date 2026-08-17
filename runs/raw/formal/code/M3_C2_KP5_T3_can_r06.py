import numpy as np
from scipy.stats import norm

# =====================
# 参数与假设设置
# =====================
annual_vol = 0.24          # 年化波动率 24%
position_value = 2700000   # 头寸金额 2,700,000 元
confidence_level = 0.95    # 置信水平 95%

# 假设：一年有252个交易日（金融市场标准惯例）
# 也可使用365，此处采用252以符合主流证券投资学教材惯例
trading_days = 252

# =====================
# 步骤1：年化波动率换算到一日期限
# =====================
# 平方根法则：日波动率 = 年化波动率 / sqrt(一年内交易日天数)
daily_vol = annual_vol / np.sqrt(trading_days)

# =====================
# 步骤2：套用 95% 正态分位数
# =====================
# 使用参数法（Delta-Normal），假设损益服从正态分布
# 获取标准正态分布下 95% 的单尾分位数 (Z-score)
z_95 = norm.ppf(confidence_level)

# =====================
# 步骤3：计算 95% 一日 VaR 并存入 result
# =====================
# VaR = 头寸金额 × 日波动率 × Z分位数
var_95_1d = position_value * daily_vol * z_95

# 按输出契约存入字典
result = {'var_95_1d': var_95_1d}

# =====================
# 课堂投屏展示辅助打印 (便于学生理解计算过程)
# =====================
print("="*40)
print("《证券投资学》- 在险价值 (VaR) 计算")
print("="*40)
print(f"1. 年化波动率换算为日波动率: {annual_vol:.2%} / sqrt({trading_days}) = {daily_vol:.4%}")
print(f"2. 95% 正态分位数 Z-score: {z_95:.4f}")
print(f"3. 95% 一日 VaR 金额: {position_value:,.2f} × {daily_vol:.4%} × {z_95:.4f} = {var_95_1d:,.2f} 元")
print("-" * 40)
print(f"输出结果 result: {result}")
