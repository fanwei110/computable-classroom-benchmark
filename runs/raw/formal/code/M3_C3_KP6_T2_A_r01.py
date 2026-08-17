import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os

# 尝试获取已存在的 df，若不存在则尝试从常见文件读取
if 'df' not in locals() and 'df' not in globals():
    if os.path.exists('data.csv'):
        df = pd.read_csv('data.csv')
    elif os.path.exists('data.xlsx'):
        df = pd.read_excel('data.xlsx')

# 窗口大小可调，默认为60
window = 60
# 无风险利率用小数表示
rf = 0.021
# 每年252个交易日
annual_factor = 252

# 计算日收益率
returns = df['fund'].pct_change()

# 滚动计算均值和标准差（ddof=1 为样本标准差）
rolling_mean = returns.rolling(window=window).mean()
rolling_std = returns.rolling(window=window).std(ddof=1)

# 年化收益率与年化波动率（按252日年化）
rolling_annual_return = rolling_mean * annual_factor
rolling_annual_std = rolling_std * np.sqrt(annual_factor)

# 计算60日滚动年化夏普比率
rolling_sharpe = (rolling_annual_return - rf) / rolling_annual_std

# 获取最后一个有效窗口的数值
rolling_sharpe_last = rolling_sharpe.dropna().iloc[-1]

# 绘制曲线图
plt.figure(figsize=(12, 6))
plt.plot(rolling_sharpe.dropna())
plt.title(f'{window}-Day Rolling Annualized Sharpe Ratio (rf={rf*100}%)')
plt.xlabel('Time')
plt.ylabel('Sharpe Ratio')
plt.grid(True)

# 保存图片
figure_path = 'rolling_sharpe.png'
plt.savefig(figure_path)
plt.close()

# 将结果存入指定字典
result = {
    'rolling_sharpe_last': rolling_sharpe_last,
    'figure_path': figure_path
}
