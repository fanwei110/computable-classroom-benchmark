import pandas as pd
import numpy as np

def calculate_annualized_sharpe(file_path='data.csv', fund_col_name='fund', rf_annual=0.021):
    """
    读取课程数据文件，计算整个样本的年化夏普比率
    """
    # 1. 读取数据文件
    df = pd.read_csv(file_path)
    
    # 2. 提取 fund 列
    fund_data = df[fund_col_name]
    
    # 3. 判断数据是净值(NAV)还是收益率(Return)
    # 收益率通常在0附近波动（绝对值均值远小于0.5），而净值通常在1.0左右或更高
    if fund_data.abs().mean() > 0.5:
        # 视为净值序列，计算周期收益率
        returns = fund_data.pct_change().dropna()
    else:
        # 视为收益率序列
        returns = fund_data.dropna()
        
    # 4. 智能判断数据频率以确定年化因子
    n_periods = len(returns)
    if n_periods > 500:
        periods_per_year = 252  # 日频数据
    elif n_periods > 100:
        periods_per_year = 52   # 周频数据
    else:
        periods_per_year = 12   # 月频数据
        
    # 5. 计算单期无风险利率 (通常使用简单算术折算)
    rf_period = rf_annual / periods_per_year
    
    # 6. 计算收益率的均值和样本标准差
    mean_return = returns.mean()
    std_return = returns.std(ddof=1)  # ddof=1 为样本标准差，符合统计学惯例
    
    # 7. 计算年化夏普比率
    # 公式: Sharpe_annual = (Mean_return - Rf_period) / Std_return * sqrt(periods_per_year)
    sharpe_annual = (mean_return - rf_period) / std_return * np.sqrt(periods_per_year)
    
    return sharpe_annual

# 执行计算
sharpe_annual_value = calculate_annualized_sharpe()

# 按照输出契约存入字典
result = {
    'sharpe_annual': sharpe_annual_value
}

# 打印结果以供验证
print(f"年化夏普比率: {sharpe_annual_value:.4f}")
