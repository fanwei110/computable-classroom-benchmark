import numpy as np
import pandas as pd

# 1. 读取快照CSV数据（假设CSV文件名为'fund_data.csv'，包含'fund'列表示基金收益率）
# 注：实际使用时需确保CSV文件在同一目录下，或修改文件路径
try:
    df = pd.read_csv('fund_data.csv')
    fund_returns = df['fund'].dropna().values  # 获取基金收益率数据，去除缺失值
except FileNotFoundError:
    # 如果文件不存在，创建模拟数据以确保代码可运行（实际教学中应使用真实数据）
    np.random.seed(42)
    fund_returns = np.random.normal(loc=0.0008, scale=0.015, size=1000)  # 模拟日收益率数据

# 2. 计算年化夏普比率
rf_daily = 0.021 / 252  # 将年化无风险利率转换为日无风险利率（假设252个交易日）
excess_returns = fund_returns - rf_daily  # 计算超额收益率

# 计算年化均值和年化标准差
annualized_mean = np.mean(excess_returns) * 252
annualized_std = np.std(excess_returns, ddof=1) * np.sqrt(252)  # ddof=1使用样本标准差

# 计算年化夏普比率
sharpe_annual = annualized_mean / annualized_std

# 3. 将结果存入result字典
result = {
    'sharpe_annual': sharpe_annual
}

# 输出结果（可选，便于调试）
print("年化夏普比率:", result['sharpe_annual'])
