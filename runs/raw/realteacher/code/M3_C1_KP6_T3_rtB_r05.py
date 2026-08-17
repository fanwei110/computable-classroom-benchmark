import pandas as pd
import numpy as np

# 假设课程数据文件已加载为 DataFrame，且包含 'fund' 列（日收益率）
# 如果是读取文件，可使用：df = pd.read_csv('你的数据文件.csv')
# daily_returns = df['fund']

# 以下是计算年化 Sharpe Ratio 的核心逻辑
def calculate_annualized_sharpe(daily_returns, rf_annual=0.021, trading_days=252):
    """
    计算年化夏普比率
    :param daily_returns: 日收益率序列
    :param rf_annual: 年化无风险利率
    :param trading_days: 一年的交易日天数，通常为252
    :return: 年化Sharpe Ratio
    """
    # 将年化无风险利率转化为日无风险利率（简单折算，行业惯例）
    rf_daily = rf_annual / trading_days
    
    # 计算日超额收益的均值
    mean_excess_daily = daily_returns.mean() - rf_daily
    
    # 计算日收益率的标准差（样本标准差，ddof=1）
    std_daily = daily_returns.std(ddof=1)
    
    # 计算日夏普比率
    sharpe_daily = mean_excess_daily / std_daily
    
    # 年化夏普比率 = 日夏普比率 * sqrt(252)
    sharpe_annual = sharpe_daily * np.sqrt(trading_days)
    
    return sharpe_annual

# 假设 daily_returns 是从文件中读取的 df['fund']
# sharpe_annual_val = calculate_annualized_sharpe(df['fund'])

# 为方便演示，这里给出最终输出字典的结构（实际运行时请替换为真实计算结果）
# sharpe_annual_val = calculate_annualized_sharpe(df['fund'])
# result = {'sharpe_annual': sharpe_annual_val}

# ===== 假设你直接运行代码并需要输出字典 =====
# 请将 df['fund'] 替换为你实际读取的数据列
# result = {'sharpe_annual': calculate_annualized_sharpe(df['fund'])}

# 如果你是要在当前环境中直接得出结果，代码如下：
# daily_returns = df['fund']  
# rf_daily = 0.021 / 252
# sharpe_annual = ((daily_returns.mean() - rf_daily) / daily_returns.std()) * np.sqrt(252)
# result = {'sharpe_annual': sharpe_annual}
