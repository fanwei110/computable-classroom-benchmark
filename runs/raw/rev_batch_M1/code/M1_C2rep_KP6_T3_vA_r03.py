import numpy as np
import pandas as pd

# 1. 读取数据并设定无风险利率
file_path = 'data/market_snapshot_v1.csv'
data = pd.read_csv(file_path)
risk_free_rate = 0.021  # 年化无风险利率2.1%

# 提取fund列的收益率数据
fund_returns = data['fund'].dropna()

# 2. 计算年化夏普比率
# 日度收益率转年化收益率
annualized_return = np.mean(fund_returns) * 252
# 日度收益率转年化波动率
annualized_volatility = np.std(fund_returns) * np.sqrt(252)
# 计算夏普比率
sharpe_ratio_annual = (annualized_return - risk_free_rate) / annualized_volatility

# 3. 存储结果
result = {
    'sharpe_annual': sharpe_ratio_annual
}

# 输出结果以供验证（可选，实际使用时可删除）
print(result)
