import numpy as np
import pandas as pd

# 假设 df 为包含基金数据的 DataFrame，'fund' 列为基金净值（全样本）
# df = pd.read_csv(...) 或其他方式导入

# 1. 计算日收益率
daily_returns = df['fund'].pct_change().dropna()

# 2. 计算日收益率均值与样本标准差（ddof=1）
mean_daily = daily_returns.mean()
std_daily = daily_returns.std(ddof=1)

# 3. 年化处理（每年 252 个交易日）
annual_return = mean_daily * 252
annual_std = std_daily * np.sqrt(252)

# 4. 无风险利率与年化夏普比率计算
# 题目给定 rf = 2.1%，按约定用小数表示为 0.021
rf = 0.021

sharpe_annual = (annual_return - rf) / annual_std

# 5. 按输出契约存入字典
result = {
    'sharpe_annual': sharpe_annual
}

# 打印结果查看
print(result)
