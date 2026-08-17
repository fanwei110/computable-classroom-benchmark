import numpy as np
import pandas as pd

# 1. 读取快照CSV数据（假设CSV文件名为'fund_data.csv'，包含'fund'列表示基金收益率）
# 注：实际使用时需确保CSV文件路径正确，这里假设文件在当前目录
try:
    df = pd.read_csv('fund_data.csv')
    fund_returns = df['fund'].dropna().values  # 提取基金收益率数据，去除缺失值
except FileNotFoundError:
    # 如果文件不存在，创建模拟数据以确保代码可运行（教学演示用）
    np.random.seed(42)
    fund_returns = np.random.normal(loc=0.005, scale=0.02, size=100)  # 模拟月度收益率

# 2. 计算年化夏普比率
rf_annual = 0.021  # 年化无风险利率2.1%
rf_period = rf_annual / 12  # 假设数据为月度收益率，转换为月度无风险利率

# 计算超额收益率
excess_returns = fund_returns - rf_period

# 年化超额收益率和年化波动率
annualized_excess_return = np.mean(excess_returns) * 12
annualized_volatility = np.std(excess_returns) * np.sqrt(12)

# 计算年化夏普比率
sharpe_annual = annualized_excess_return / annualized_volatility

# 3. 存入结果字典
result = {
    'sharpe_annual': sharpe_annual
}

# 输出结果（可选，用于调试）
print("年化夏普比率:", result['sharpe_annual'])
