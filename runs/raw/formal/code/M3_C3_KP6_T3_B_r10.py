import numpy as np
import pandas as pd

# 假设您的数据已经加载为 DataFrame df，包含 'fund' 列
# df = pd.read_csv('your_data.csv') 
# fund_returns = df['fund']

def calculate_sharpe_annual(fund_returns, rf_annual=0.021, trading_days=252):
    # 1. 计算日连续复利无风险利率
    rf_daily = np.exp(rf_annual / trading_days) - 1
    
    # 2. 计算日超额收益率
    excess_returns = fund_returns - rf_daily
    
    # 3. 计算均值与样本标准差 (ddof=1 严格遵循约定)
    mean_excess_daily = np.mean(excess_returns)
    std_excess_daily = np.std(excess_returns, ddof=1)
    
    # 4. 计算年化夏普比率
    sharpe_daily = mean_excess_daily / std_excess_daily
    sharpe_annual = sharpe_daily * np.sqrt(trading_days)
    
    return sharpe_annual

# 获取计算结果 (此处因无数据用占位符表示)
# sharpe_value = calculate_sharpe_annual(fund_returns)

# 按输出契约存入字典
result = {
    'sharpe_annual': None  # 请将 None 替换为用上述代码计算出的实际数值
}
