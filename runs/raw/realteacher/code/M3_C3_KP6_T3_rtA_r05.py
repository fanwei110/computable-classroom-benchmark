import pandas as pd
import numpy as np

# 假设数据已加载为 DataFrame df，且包含 'fund' 列（日收益率）
# daily_returns = df['fund']

def calculate_sharpe(daily_returns):
    # 计算约定参数
    rf_annual = 0.021         # 无风险利率 2.1%，小数表示
    trading_days = 252        # 每年252个交易日
    
    # 去除可能的空值
    daily_returns = daily_returns.dropna()
    
    # 计算日收益率均值
    mean_daily = daily_returns.mean()
    
    # 计算日收益率标准差（样本估计量，ddof=1）
    std_daily = daily_returns.std(ddof=1)
    
    # 将年化无风险利率转为日无风险利率（按单利拆解，与常用年化方式匹配）
    rf_daily = rf_annual / trading_days
    
    # 计算年化夏普比率
    # 年化超额收益 = (日均值 - 日无风险) * 252
    # 年化波动率 = 日标准差 * sqrt(252)
    # 夏普比率 = 年化超额收益 / 年化波动率 = (日均值 - 日无风险) / 日标准差 * sqrt(252)
    sharpe_annual = (mean_daily - rf_daily) / std_daily * np.sqrt(trading_days)
    
    # 按输出契约存入字典
    result = {'sharpe_annual': sharpe_annual}
    
    return result

# 调用示例（假设 df 为你的数据文件 DataFrame）：
# result = calculate_sharpe(df['fund'])
