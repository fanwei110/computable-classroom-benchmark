import numpy as np
from scipy.stats import norm

# ================= 已知参数 =================
sigma_annual = 0.24          # 年化波动率 24%
position_value = 2700000    # 头寸金额 2,700,000 元
confidence_level = 0.95     # 置信水平 95%

# ================= 假设处理 =================
# 题目未指明年化换算日化的交易日天数，采用金融市场最常用的内部一致假设：一年252个交易日
trading_days_per_year = 252

# ================= 步骤 1：年化波动率换算到一日期限 =================
# 根据平方根法则，日波动率 = 年化波动率 / sqrt(一年的交易日数)
sigma_daily = sigma_annual / np.sqrt(trading_days_per_year)

# ================= 步骤 2：套用 95% 正态分位数 =================
# 使用 scipy 获取标准正态分布下 95% 的单尾分位数
z_score_95 = norm.ppf(confidence_level)

# ================= 步骤 3：计算 VaR 金额 =================
# 参数法（Delta-Normal）计算公式：VaR = 头寸价值 × Z分位数 × 日波动率
var_95_1d = position_value * z_score_95 * sigma_daily

# ================= 输出契约 =================
result = {'var_95_1d': var_95_1d}

# （以下为课堂投屏辅助打印，便于学生理解中间步骤）
print(f"【假设】一年交易日天数: {trading_days_per_year} 天")
print(f"【步骤1】日化波动率: {sigma_annual:.2%} / √{trading_days_per_year} = {sigma_daily:.4%}")
print(f"【步骤2】95%正态分位数(Z值): {z_score_95:.4f}")
print(f"【步骤3】95%一日VaR: {position_value:,.0f} × {z_score_95:.4f} × {sigma_daily:.4%} = {var_95_1d:,.2f} 元")
print(f"\n最终输出字典: {result}")
