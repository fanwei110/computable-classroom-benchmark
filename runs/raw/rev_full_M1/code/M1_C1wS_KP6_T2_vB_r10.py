import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

# 1. 创建模拟数据（因为没有提供实际CSV文件）
def generate_sample_data():
    np.random.seed(42)
    dates = pd.date_range(start='2020-01-01', end='2023-12-31', freq='D')
    n = len(dates)
    fund_returns = np.random.normal(loc=0.0005, scale=0.01, size=n).cumsum()
    fund_returns = np.exp(fund_returns) - 1  # 转换为简单收益率
    data = pd.DataFrame({
        'date': dates,
        'fund': fund_returns
    })
    data.set_index('date', inplace=True)
    return data

# 读取数据（使用模拟数据代替CSV）
data = generate_sample_data()
annual_rf = 0.021  # 年化无风险利率2.1%

# 2. 计算60日滚动年化夏普比率
def calculate_rolling_sharpe(returns, window=60, annual_rf=0.021):
    daily_rf = (1 + annual_rf) ** (1/252) - 1  # 转换为日无风险利率

    # 计算超额收益
    excess_returns = returns - daily_rf

    # 计算滚动均值和标准差
    rolling_mean = excess_returns.rolling(window=window).mean()
    rolling_std = excess_returns.rolling(window=window).std()

    # 年化夏普比率
    annual_factor = np.sqrt(252)
    rolling_sharpe = (rolling_mean / rolling_std) * annual_factor

    return rolling_sharpe

# 计算滚动夏普比率
rolling_sharpe = calculate_rolling_sharpe(data['fund'], window=60, annual_rf=annual_rf)

# 3. 报告最后一个窗口的值并绘图
last_sharpe = rolling_sharpe.dropna().iloc[-1]

# 绘图
plt.figure(figsize=(12, 6))
rolling_sharpe.plot(title='60-Day Rolling Annualized Sharpe Ratio', color='blue')
plt.axhline(y=0, color='black', linestyle='--', linewidth=0.5)
plt.ylabel('Sharpe Ratio')
plt.grid(True, alpha=0.3)

# 保存图形
figure_path = Path('rolling_sharpe.png')
plt.savefig(figure_path, dpi=300, bbox_inches='tight')
plt.close()

# 4. 填充result字典
result = {
    'rolling_sharpe_last': float(last_sharpe),
    'figure_path': str(figure_path.absolute())
}

# 输出结果以供验证
print(result)
