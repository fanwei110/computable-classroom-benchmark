import numpy as np
import pandas as pd
from scipy import stats

# 读取数据
try:
    df = pd.read_csv('data/market_snapshot_v1.csv')
except FileNotFoundError:
    print("数据文件未找到，请检查路径")
    raise

# 检查数据
print(f"数据形状: {df.shape}")
print(f"数据列名: {df.columns.tolist()}")
print(f"fund列前几行:\n{df['fund'].head()}")

# 检查fund列的数据类型和缺失值
print(f"fund列数据类型: {df['fund'].dtype}")
print(f"fund列缺失值数量: {df['fund'].isna().sum()}")

# 计算日收益率（假设fund列是价格数据）
# 如果fund已经是收益率，则直接使用；否则计算价格变动率
fund_data = df['fund'].values

# 判断数据是否为价格序列（通常价格>0且数量级较大）
if np.all(fund_data > 0) and np.mean(fund_data) > 1:
    # 假设是价格数据，计算日收益率
    daily_returns = np.diff(fund_data) / fund_data[:-1]
    print("数据处理：将fund列视为价格数据，计算日收益率")
else:
    # 假设已经是收益率数据
    daily_returns = fund_data[1:]
    print("数据处理：将fund列视为收益率数据")

# 检查收益率数据
print(f"日收益率样本数: {len(daily_returns)}")
print(f"日收益率描述性统计:\n{pd.Series(daily_returns).describe()}")

# 设定无风险利率
rf_annual = 0.021  # 2.1%年化无风险利率

# 假设一年有252个交易日
trading_days_per_year = 252

# 计算日化无风险利率
rf_daily = rf_annual / trading_days_per_year

# 计算超额收益率（日度）
excess_daily_returns = daily_returns - rf_daily

# 计算日度超额收益的均值和标准差
mean_excess_daily = np.mean(excess_daily_returns)
std_excess_daily = np.std(excess_daily_returns, ddof=1)  # 使用样本标准差

# 年化处理
# 年化超额收益 = 日度超额收益均值 * 252
mean_excess_annual = mean_excess_daily * trading_days_per_year
# 年化标准差 = 日度标准差 * sqrt(252)
std_excess_annual = std_excess_daily * np.sqrt(trading_days_per_year)

# 计算年化夏普比率
sharpe_annual = mean_excess_annual / std_excess_annual

print(f"\n=== 夏普比率计算 ===")
print(f"日度超额收益均值: {mean_excess_daily:.8f}")
print(f"日度超额收益标准差: {std_excess_daily:.8f}")
print(f"年化超额收益: {mean_excess_annual:.6f}")
print(f"年化标准差: {std_excess_annual:.6f}")
print(f"年化夏普比率: {sharpe_annual:.4f}")

# 计算信息比率（可选，用于验证的额外指标）
ir = mean_excess_annual / std_excess_annual
print(f"信息比率（验证）: {ir:.4f}")

# 存储结果
result = {
    'sharpe_annual': float(sharpe_annual)
}

print(f"\n结果字典: {result}")
print("计算完成！")
