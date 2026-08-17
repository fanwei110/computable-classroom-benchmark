import numpy as np
from scipy import stats

# --- 输入参数 ---
annual_vol = 0.24          # 年化波动率 24%
position_value = 2700000  # 头寸规模 2,700,000 元
confidence_level = 0.95   # 95% 置信水平
trading_days = 252        # 假设一年有252个交易日

# --- 计算过程 ---
# 1. 将年化波动率转换为日波动率 (假设日收益率为独立同分布，使用平方根时间法则)
daily_vol = annual_vol / np.sqrt(trading_days)

# 2. 获取95%置信水平下的标准正态分布分位数 (Z-score)
z_score = stats.norm.ppf(confidence_level)

# 3. 计算95%一日VaR (参数法/方差-协方差法)
var_95_1d = position_value * daily_vol * z_score

# --- 输出契约 ---
result = {
    'var_95_1d': var_95_1d
}

# (可选) 打印验证
print(f"日波动率: {daily_vol:.6f}")
print(f"Z-score (95%): {z_score:.6f}")
print(f"95% 一日 VaR: {var_95_1d:.2f} 元")
print(f"结果字典: {result}")
