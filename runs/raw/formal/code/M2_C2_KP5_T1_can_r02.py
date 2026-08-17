import numpy as np
from scipy.stats import norm

# ==================== 参数设定 ====================
position_value = 1_850_000.0   # 头寸价值（人民币元）
annual_vol = 0.218            # 年化收益波动率
trading_days = 252            # 假设一年共有252个交易日（行业惯例）

# ==================== 步骤1：年化波动率换算为日波动率 ====================
# 假设收益率独立同分布，波动率按时间平方根缩放
daily_vol = annual_vol / np.sqrt(trading_days)

# ==================== 步骤2：正态分布分位数 ====================
# delta-normal 模型下，VaR 的分位数取标准正态分布的左侧分位数
# 根据对称性：置信水平 α 对应的左侧分位数为 z_α = Φ⁻¹(α)
z_95 = norm.ppf(0.95)   # 95% 置信水平
z_99 = norm.ppf(0.99)   # 99% 置信水平

# ==================== 步骤3：计算 VaR ====================
# 一日 VaR（95%）
var_95_1d = position_value * daily_vol * z_95

# 十日 VaR（99%）先从一日波动率缩放至十日波动率，再结合99%分位数
var_99_10d = position_value * daily_vol * np.sqrt(10) * z_99

# ==================== 输出契约 ====================
result = {
    'var_95_1d': round(var_95_1d, 2),
    'var_99_10d': round(var_99_10d, 2)
}

print(result)
