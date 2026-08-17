import pandas as pd
import numpy as np
import os

# 动态查找当前目录下的课程数据文件（支持 csv, xlsx, xls 格式），确保无占位值
data_file = None
for f in os.listdir('.'):
    if f.endswith(('.csv', '.xlsx', '.xls')):
        data_file = f
        break

if data_file is None:
    # 如果未找到，使用默认值以保证脚本确定性（实际运行时应将数据文件置于同目录下）
    data_file = 'data.csv'

# 读取数据文件
if data_file.endswith('.csv'):
    df = pd.read_csv(data_file)
else:
    df = pd.read_excel(data_file)

# 提取 fund 列并剔除缺失值
fund_nav = df['fund'].dropna()

# 计算日度简单收益率 (假设 fund 列为基金净值)
daily_returns = fund_nav.pct_change().dropna()

# 无风险利率（年化）
rf_annual = 0.021

# 年化参数（假设数据为日度数据，每年 252 个交易日）
# 若为月度数据该值应为 12，周度应为 52。此处按最常见的日度基金净值数据处理
annualization_factor = 252

# 计算日度收益率的均值与样本标准差
mean_daily = daily_returns.mean()
std_daily = daily_returns.std(ddof=1)  # ddof=1 为样本标准差，符合统计惯例

# 年化期望收益率与年化波动率
annual_return = mean_daily * annualization_factor
annual_std = std_daily * np.sqrt(annualization_factor)

# 计算整个样本的年化夏普比率
sharpe_annual = (annual_return - rf_annual) / annual_std

# 按照输出契约存入字典
result = {'sharpe_annual': sharpe_annual}

print(result)
