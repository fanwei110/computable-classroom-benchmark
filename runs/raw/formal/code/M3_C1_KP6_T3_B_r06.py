import pandas as pd
import numpy as np

# 假设数据存储在名为 df 的 DataFrame 中，基金收益率在 'fund' 列
# 根据实际情况调整年化因子（如日度数据为252，月度数据为12，周度数据为52）
# 此处以日度数据为例，annualization_factor = 252

def calculate_annual_sharpe(df, annualization_factor=252):
    # 无风险利率年化 2.1%
    rf_annual = 0.021
    
    # 全样本基金收益率序列
    fund_returns = df['fund']
    
    # 计算每期无风险利率
    rf_period = rf_annual / annualization_factor
    
    # 计算超额收益
    excess_returns = fund_returns - rf_period
    
    # 计算年化夏普比率
    # 年化夏普 = (均值 / 标准差) * 周期平方根
    mean_excess = excess_returns.mean()
    std_returns = fund_returns.std()
    
    sharpe_annual = (mean_excess / std_returns) * np.sqrt(annualization_factor)
    
    return sharpe_annual

# 假设 df 已经定义
# sharpe = calculate_annual_sharpe(df)

# 生成符合契约的输出结果（此处用占位符代表具体计算数值）
result = {
    'sharpe_annual': None # 实际运行时替换为计算出的 sharpe 变量值
}
