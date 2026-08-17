import numpy as np
import pandas as pd

# 设定无风险利率（年化）
risk_free_rate_annual = 0.021

# 模拟读取课程数据文件（假设文件名为 'course_data.csv'，且包含 'fund' 列）
# 注：实际使用时需替换为真实文件路径
try:
    # 尝试读取数据（示例中假设文件存在）
    data = pd.read_csv('course_data.csv')
    fund_returns = data['fund'].dropna().values  # 提取 fund 列并去除缺失值
except FileNotFoundError:
    # 若文件不存在，生成模拟数据以确保脚本可运行（实际使用时应删除此部分）
    np.random.seed(42)
    fund_returns = np.random.normal(loc=0.0005, scale=0.01, size=1000)  # 模拟日收益率

# 计算日收益率的均值和标准差
mean_daily_return = np.mean(fund_returns)
std_daily_return = np.std(fund_returns, ddof=1)  # 样本标准差

# 年化处理
trading_days_per_year = 252
mean_annual_return = mean_daily_return * trading_days_per_year
std_annual_return = std_daily_return * np.sqrt(trading_days_per_year)

# 计算年化夏普比率
sharpe_ratio_annual = (mean_annual_return - risk_free_rate_annual) / std_annual_return

# 存储结果
result = {
    'sharpe_annual': sharpe_ratio_annual
}

# 输出结果（可选）
print(result)
