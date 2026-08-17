import numpy as np
import pandas as pd

# 由于缺失具体数据，结果暂设为 None
result = {'sharpe_annual': None}

# === 以下是当您获取到 df 数据后的计算代码 ===
def calculate_annual_sharpe(returns_series, rf_annual=0.021, freq=252):
    """
    returns_series: 基金收益率序列 (即 fund 列)
    rf_annual: 年化无风险利率，默认 2.1%
    freq: 一年中的交易期数，日度数据通常为 242 或 252，月度为 12
    """
    mean_period = returns_series.mean()
    std_period = returns_series.std()
    
    # 计算年化夏普比率
    sharpe_annual = ((mean_period - rf_annual / freq) / std_period) * np.sqrt(freq)
    
    return sharpe_annual

# 假设您已有 DataFrame 命名为 df：
# sharpe_value = calculate_annual_sharpe(df['fund'], rf_annual=0.021, freq=252)
# result['sharpe_annual'] = sharpe_value
