import numpy as np

# 假设 fund_returns 为基金的日收益率序列（此处用示例数据替代，实际使用时替换为真实数据）
# fund_returns = ...

# 为了演示，生成随机数据作为示例（实际应用中应使用真实数据）
np.random.seed(42)  # 固定随机种子保证可重复，实际使用时删除此行
fund_returns = np.random.normal(0.0005, 0.01, 1000)  # 示例日收益率序列

rf = 0.021  # 年复利报价的无风险利率
rf_cont = np.log(1 + rf)  # 转换为连续复利

mean_daily = np.mean(fund_returns)
std_daily = np.std(fund_returns, ddof=1)

annual_return = mean_daily * 252
annual_vol = std_daily * np.sqrt(252)

sharpe_annual = (annual_return - rf_cont) / annual_vol

result = {'sharpe_annual': sharpe_annual}
