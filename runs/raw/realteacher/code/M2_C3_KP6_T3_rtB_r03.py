import pandas as pd
import numpy as np

# 假设数据文件是常见的Excel或CSV格式，我先尝试读取
# 由于课程数据文件可能在不同位置，请将文件路径替换为实际路径
try:
    # 尝试读取常见的数据文件格式
    df = pd.read_csv('course_data.csv')  # 请替换为实际文件名
except:
    try:
        df = pd.read_excel('course_data.xlsx')  # 请替换为实际文件名
    except:
        # 如果找不到文件，创建一个示例计算框架
        print("请提供实际的课程数据文件路径")
        # 这里用示例数据演示计算过程
        # 假设fund列存在日收益率数据
        np.random.seed(42)
        df = pd.DataFrame({
            'fund': np.random.normal(0.001, 0.02, 252)  # 示例数据
        })

# 计算参数
risk_free_rate = 0.021  # 无风险利率2.1%
trading_days = 252  # 年交易日数

# 提取基金日收益率
fund_daily_returns = df['fund']

# 计算日超额收益
excess_daily_returns = fund_daily_returns - risk_free_rate / trading_days

# 计算年化夏普比率
# 年化超额收益 = 日超额收益的均值 * 252
annual_excess_return = excess_daily_returns.mean() * trading_days

# 年化标准差 = 日收益的标准差 * sqrt(252)，使用样本标准差(ddof=1)
annual_std = fund_daily_returns.std(ddof=1) * np.sqrt(trading_days)

# 夏普比率 = 年化超额收益 / 年化标准差
sharpe_annual = annual_excess_return / annual_std

# 存储结果
result = {
    'sharpe_annual': sharpe_annual
}

print(f"年化夏普比率: {sharpe_annual:.4f}")
print(f"计算结果已存入result字典: {result}")
