import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# ========== 1. 数据准备 ==========
# 替换为您的实际数据读取代码，例如：
# df = pd.read_csv('your_data.csv', index_col=0, parse_dates=True)
# 若无数据，运行以下模拟数据作为演示
np.random.seed(42)
dates = pd.date_range('2020-01-01', periods=500, freq='B')
returns = np.random.normal(0.0005, 0.02, len(dates))
df = pd.DataFrame({'fund': returns}, index=dates)

# ========== 2. 参数设置 ==========
window = 60          # 滚动窗口，可调
rf_annual = 0.021    # 年化无风险利率
rf_daily = rf_annual / 252   # 日化无风险利率

# ========== 3. 计算滚动夏普比率 ==========
# 日超额收益率
df['excess_return'] = df['fund'] - rf_daily

# 年化平均超额收益 (滚动窗口内) 
rolling_annual_mean = df['excess_return'].rolling(window).mean() * 252

# 年化波动率 (滚动窗口内，使用基金收益率计算波动率)
rolling_annual_std = df['fund'].rolling(window).std() * np.sqrt(252)

# 滚动夏普比率
rolling_sharpe = rolling_annual_mean / rolling_annual_std

# 最后一个窗口的夏普比率值
rolling_sharpe_last = rolling_sharpe.iloc[-1]

# ========== 4. 绘图并保存 ==========
plt.figure(figsize=(12, 6))
rolling_sharpe.plot(color='blue', linewidth=1.5)
plt.axhline(y=0, color='gray', linestyle='--')
plt.title(f'Rolling {window}-Day Sharpe Ratio (rf={rf_annual:.1%})')
plt.ylabel('Sharpe Ratio')
plt.xlabel('Date')
plt.grid(True, alpha=0.3)
figure_path = 'rolling_sharpe.png'
plt.savefig(figure_path, dpi=150, bbox_inches='tight')
plt.close()

# ========== 5. 输出契约字典 ==========
result = {
    'rolling_sharpe_last': round(rolling_sharpe_last, 6),  # 保留6位小数
    'figure_path': figure_path
}

print(result)  # 查看结果
