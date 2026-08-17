import numpy as np
import scipy.stats as stats

def calculate_1d_var():
    # 已知参数
    annual_vol = 0.24                  # 年化波动率 24%
    position = 2_700_000               # 头寸金额 2,700,000 元
    trading_days = 252                 # 一年的标准交易日天数
    confidence_level = 0.95            # 置信水平 95%
    
    # 计算日度波动率
    daily_vol = annual_vol / np.sqrt(trading_days)
    
    # 计算正态分布对应的 Z 分位数 (单尾)
    z_score = stats.norm.ppf(confidence_level)
    
    # 计算 95% 一日 VaR: 头寸 * 日度波动率 * Z分位数
    var_95_1d = position * daily_vol * z_score
    
    return var_95_1d

# 按照输出契约，将结果存入字典
result = {
    'var_95_1d': calculate_1d_var()
}

# 打印结果以供验证
print(result)
