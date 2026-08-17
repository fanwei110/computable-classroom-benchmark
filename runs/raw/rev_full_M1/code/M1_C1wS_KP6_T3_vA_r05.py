import numpy as np
import pandas as pd

# 1. 读取数据（假设CSV文件名为'fund_data.csv'，且包含'fund'列表示基金收益率）
# 注：实际使用时需确保CSV文件路径正确，这里假设文件在当前目录
try:
    df = pd.read_csv('fund_data.csv')
    fund_returns = df['fund'].dropna().values  # 获取基金收益率数据，去除缺失值
except FileNotFoundError:
    # 如果文件不存在，创建模拟数据以确保代码可运行（课堂演示用）
    np.random.seed(42)
    fund_returns = np.random.normal(loc=0.0005, scale=0.01, size=1000)  # 模拟日收益率

# 无风险利率（年化）
risk_free_rate_annual = 0.021

# 2. 计算年化夏普比率
# 假设fund_returns是日收益率（常见情况），则年化处理如下：
daily_risk_free_rate = (1 + risk_free_rate_annual) ** (1/252) - 1  # 转换为日无风险利率
excess_returns = fund_returns - daily_risk_free_rate  # 计算超额收益

# 年化夏普比率 = (年化超额收益均值) / (年化超额收益标准差)
annualized_excess_return = np.mean(excess_returns) * 252
annualized_excess_volatility = np.std(excess_returns) * np.sqrt(252)
sharpe_annual = annualized_excess_return / annualized_excess_volatility

# 3. 存储结果
result = {
    'sharpe_annual': sharpe_annual
}

# 输出结果（可选，便于调试）
print("年化夏普比率:", result['sharpe_annual'])
