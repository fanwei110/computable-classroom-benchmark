import pandas as pd
import numpy as np
from scipy import stats

def calculate_sharpe_ratio():
    """
    计算 fund 列的全样本年化夏普比率
    无风险利率: 2.1%
    """
    
    # 读取数据
    df = pd.read_csv('data/market_snapshot_v1.csv')
    
    # 提取 fund 列收益率
    fund_returns = df['fund']
    
    # 设定无风险利率（年化）
    risk_free_rate_annual = 0.021  # 2.1%
    
    # 计算年化收益率
    # 假设数据为日频收益率，一年252个交易日
    # 如果是月频收益率，一年12个月；如果是周频，一年52周
    # 先检查数据频率，或直接采用日频假设（常见课程设置）
    
    # 计算平均收益率
    mean_return = fund_returns.mean()
    std_return = fund_returns.std(ddof=1)  # 使用样本标准差
    
    # 判断数据观测数量，推断频率
    n_obs = len(fund_returns)
    
    # 常见假设：252个交易日/年（日频），12个月/年（月频），52周/年（周频）
    # 根据数据量判断：如果大于200，大概率日频；如果12-50，可能月频或周频
    if n_obs > 200:
        periods_per_year = 252  # 日频
    elif n_obs > 50:
        periods_per_year = 52   # 周频
    elif n_obs > 20:
        periods_per_year = 12   # 月频
    else:
        periods_per_year = 4    # 季频
    
    # 年化收益率和标准差
    annualized_return = mean_return * periods_per_year
    annualized_std = std_return * np.sqrt(periods_per_year)
    
    # 年化夏普比率
    # 夏普比率 = (年化收益率 - 年化无风险利率) / 年化标准差
    sharpe_annual = (annualized_return - risk_free_rate_annual) / annualized_std
    
    return sharpe_annual

# 主程序
if __name__ == "__main__":
    # 计算夏普比率
    sharpe_ratio = calculate_sharpe_ratio()
    
    # 存入结果字典
    result = {
        'sharpe_annual': round(sharpe_ratio, 6)
    }
    
    print(f"年化夏普比率: {result['sharpe_annual']:.6f}")
    print(f"\n结果字典: {result}")
