import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter

# 1. 读取快照CSV数据（模拟数据，实际使用时请替换为真实CSV读取）
# 假设CSV有日期和fund收益率列
np.random.seed(42)  # 确保可复现
dates = pd.date_range(start='2020-01-01', periods=200, freq='D')
fund_returns = np.random.normal(loc=0.0005, scale=0.01, size=200)  # 模拟日收益率
data = pd.DataFrame({'date': dates, 'fund': fund_returns})
data.set_index('date', inplace=True)

# 无风险利率（年化2.1%，转换为日利率）
annual_rf = 0.021
daily_rf = (1 + annual_rf) ** (1/252) - 1

# 2. 计算60日滚动年化夏普比率
window = 60
rolling_excess_returns = data['fund'].rolling(window=window).apply(
    lambda x: (x - daily_rf).mean() * 252 / (x.std() * np.sqrt(252)), raw=True
)

# 3. 报告最后一个窗口的值
last_sharpe = rolling_excess_returns.iloc[-1]

# 绘制时间序列图
plt.figure(figsize=(10, 6))
rolling_excess_returns.plot(label=f'{window}-day Rolling Sharpe Ratio', color='royalblue')
plt.axhline(y=0, color='black', linestyle='--', linewidth=0.5)
plt.title(f'{window}-Day Rolling Annualized Sharpe Ratio (RF={annual_rf*100:.1f}%)')
plt.xlabel('Date')
plt.ylabel('Sharpe Ratio')
plt.grid(True, alpha=0.3)
plt.legend()

# 格式化y轴显示
plt.gca().yaxis.set_major_formatter(FuncFormatter(lambda y, _: f'{y:.2f}'))

# 保存图形
figure_path = 'rolling_sharpe_ratio.png'
plt.savefig(figure_path, dpi=300, bbox_inches='tight')
plt.close()

# 4. 填充result字典
result = {
    'rolling_sharpe_last': float(last_sharpe),
    'figure_path': figure_path
}

# 输出结果以供验证
print(result)
