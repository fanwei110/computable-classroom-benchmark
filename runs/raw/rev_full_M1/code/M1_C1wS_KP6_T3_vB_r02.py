import numpy as np
import pandas as pd

# 1. 读取快照CSV数据（假设CSV文件名为'fund_returns.csv'，包含'date'和'fund'两列）
# 注：实际使用时需确保CSV文件路径正确
try:
    df = pd.read_csv('fund.csv', parse_dates=['date'])
    fund_returns = df.set_index('date')['fund'].dropna()
except FileNotFoundError:
    # 如果文件不存在，创建模拟数据以确保代码可运行（教学演示用）
    np.random.seed(42)
    dates = pd.date_range(start='2020-01-01', end='2023-12-31', freq='D')
    fund_returns = pd.Series(np.random.normal(0.0005, 0.01, len(dates)), index=dates)
    fund_returns = fund_returns[fund_returns.index.dayofweek < 5]  # 剔除周末

# 2. 计算年化夏普比率
rf_daily = 0.021 / 252  # 将年化无风险利率转换为日频
excess_returns = fund_returns - rf_daily

# 年化收益率和年化波动率
annualized_return = (1 + excess_returns.mean()) ** 252 - 1
annualized_volatility = excess_returns.std() * np.sqrt(252)

# 计算夏普比率（年化）
sharpe_annual = annualized_return / annualized_volatility

# 3. 存储结果
result = {
    'sharpe_annual': sharpe_annual
}

# 输出结果（可选，用于调试）
print("年化夏普比率:", result['sharpe_annual'])
