import numpy as np
from scipy.stats import norm

# 给定参数
annual_vol = 0.24          # 年化波动率 24%
position = 2_700_000       # 头寸金额 2,700,000 元
confidence_level = 0.95    # 置信水平 95%
days_per_year = 252        # 年化交易天数
holding_days = 1           # 持有期 1 日

# 根据课堂约定：短期限下均值取零，波动率按 sqrt(天数) 缩放
daily_vol = annual_vol / np.sqrt(days_per_year)   # 日波动率
# 单尾正态分位数（95% → z=1.6448536269514722）
z = norm.ppf(confidence_level)
# 在险价值（为正的损失金额）：VaR = z * sigma * position (均值=0)
var_95_1d = z * daily_vol * position

# 输出字典
result = {
    'var_95_1d': round(var_95_1d, 2)   # 按常规货币金额保留两位小数
}

# （可选）打印结果
print("95% 置信水平下的一日在险价值 (VaR):")
print(f"  {result['var_95_1d']:,.2f} 元")

