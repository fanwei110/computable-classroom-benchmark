import numpy as np
from scipy.stats import norm

# --- 输入参数 ---
annual_vol = 0.24          # 年化波动率 24%
position_value = 2_700_000 # 头寸市值 270万
confidence_level = 0.95    # 置信水平 95%
trading_days = 252         # 一年交易天数（常用假设）

# --- 步骤1：将年化波动率换算为一日期限 ---
daily_vol = annual_vol / np.sqrt(trading_days)

# --- 步骤2：95% 正态分位数（标准正态分布的 95% 分位点）---
z_score = norm.ppf(confidence_level)  # 正值，代表右侧分位数

# --- 步骤3：计算 1 日 VaR 金额 ---
# VaR = 头寸 × 日波动率 × Z(置信水平)
var_95_1d = position_value * daily_vol * z_score

# --- 按照输出契约存入字典 ---
result = {
    'var_95_1d': var_95_1d
}

# （可选）打印以便课堂投屏查看
print(f"年化波动率: {annual_vol*100:.1f}%")
print(f"头寸市值: {position_value:,.0f} 元")
print(f"交易天数假设: {trading_days} 天/年")
print(f"日波动率: {daily_vol:.4%}")
print(f"95% 置信水平对应的正态分位数: {z_score:.4f}")
print(f"95% 一日 VaR: {var_95_1d:,.2f} 元")
print("\n结果字典:", result)
