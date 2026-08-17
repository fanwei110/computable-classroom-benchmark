import numpy as np
from scipy.stats import norm

# 给定数据
position = 2_700_000          # 头寸金额（元）
annual_vol = 0.24            # 年化波动率
confidence = 0.95            # 置信水平
trading_days = 252           # 年交易日数（金融常用假设）

# 1. 年化波动率换算为日波动率
daily_vol = annual_vol / np.sqrt(trading_days)

# 2. 95% 置信水平下的正态分布分位数（左尾 5%）
z_alpha = norm.ppf(1 - confidence)  # 对于 95% 得到约 -1.64485
# VaR 定义为损失的绝对值，因此取分位数的绝对值
var_95_1d = position * daily_vol * abs(z_alpha)

# 3. 按要求构建输出字典
result = {
    'var_95_1d': var_95_1d
}

if __name__ == '__main__':
    print(result)
