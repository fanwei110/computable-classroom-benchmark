import numpy as np
from scipy.stats import norm

# ==================== 已知条件 ====================
position_value = 1_850_000  # 头寸价值（人民币元）
annual_vol = 0.218         # 年化收益波动率

# ==================== 假设条件 ====================
# 假设一年有252个交易日，这是金融计算中将年化波动率转换为日波动率的常用标准
trading_days_per_year = 252

# ==================== 步骤1：年化波动率换算到一日期限 ====================
# Delta-normal模型下，波动率与时间的平方根成正比：sigma_daily = sigma_annual / sqrt(T)
daily_vol = annual_vol / np.sqrt(trading_days_per_year)

# ==================== 步骤2：对两个置信水平套用正态分位数 ====================
# 95%和99%置信水平下的标准正态分布分位数（上侧分位数）
z_95 = norm.ppf(0.95)
z_99 = norm.ppf(0.99)

# ==================== 步骤3：计算VaR并缩放到十日期限 ====================
# (i) 95% 一日 VaR
# VaR = 头寸价值 × 分位数 × 波动率
var_95_1d = position_value * z_95 * daily_vol

# (ii) 99% 十日 VaR
# 十日波动率 = 一日波动率 × sqrt(10)
ten_day_vol = daily_vol * np.sqrt(10)
var_99_10d = position_value * z_99 * ten_day_vol

# ==================== 步骤4：填充 result ====================
result = {
    'var_95_1d': var_95_1d,
    'var_99_10d': var_99_10d
}

# 打印结果以供课堂投屏验证
print(f"95% 一日 VaR: {result['var_95_1d']:.2f} 元")
print(f"99% 十日 VaR: {result['var_99_10d']:.2f} 元")
