import numpy as np
import pandas as pd

# 1. 读取CSV文件（假设CSV文件名为'fund_returns.csv'，且包含'fund'列）
# 注意：实际使用时需确保CSV文件路径正确
try:
    df = pd.read_csv('fund_returns.csv')  # 请根据实际文件名调整
    fund_returns = df['fund'].dropna().values  # 提取'fund'列并去除缺失值
except FileNotFoundError:
    raise FileNotFoundError("请确保CSV文件存在且路径正确，文件中包含'fund'列")
except KeyError:
    raise KeyError("CSV文件中未找到'fund'列")

# 2. 设定无风险利率（年化2.1%，需转换为与收益率频率一致）
rf_annual = 0.021
n_periods_per_year = len(fund_returns) / (pd.to_datetime(df['date']).max() - pd.to_datetime(df['date']).min()).days * 365.25 if 'date' in df.columns else 12  # 默认月度数据
rf_period = rf_annual / n_periods_per_year

# 计算超额收益
excess_returns = fund_returns - rf_period

# 计算年化夏普比率
sharpe_ratio = np.mean(excess_returns) / np.std(excess_returns, ddof=1) * np.sqrt(n_periods_per_year)

# 3. 存储结果
result = {
    'sharpe_annual': sharpe_ratio
}

# 输出结果（供教师投屏）
print("年化夏普比率:", result['sharpe_annual'])
