import numpy as np
import pandas as pd

# 1. 读取数据并设定无风险利率
# 假设CSV文件名为'fund_data.csv'，且包含'fund'列（基金的月度收益率）
# 如果文件名或列名不同，请根据实际情况调整
data = pd.read_csv('fund_data.csv')  # 请确保文件在当前工作目录
fund_returns = data['fund'].dropna()  # 获取基金收益率数据，去除缺失值

risk_free_rate = 0.021  # 年化无风险利率2.1%

# 2. 计算年化夏普比率
# 将月度收益率转换为年化收益率和年化波动率
monthly_excess_returns = fund_returns - (risk_free_rate / 12)  # 月度超额收益
annualized_return = np.mean(monthly_excess_returns) * 12
annualized_volatility = np.std(monthly_excess_returns) * np.sqrt(12)
sharpe_annual = annualized_return / annualized_volatility

# 3. 存储结果
result = {
    'sharpe_annual': sharpe_annual
}

# 输出结果（可选，用于验证）
print("年化夏普比率:", result['sharpe_annual'])
