import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# ========================
# 可调参数（教师可按需修改）
# ========================
WINDOW = 60                # 滚动窗口天数
RF_ANNUAL = 0.021          # 年化无风险利率（2.1%）
TRADING_DAYS = 252         # 年交易日数（用于年化）
# ========================

# 1. 读取数据，假设文件名为 snapshot.csv
df = pd.read_csv('snapshot.csv')

# 统一列名为小写便于处理
df.columns = df.columns.str.lower()

# 检查必需列
if 'date' not in df.columns:
    raise KeyError("CSV 文件中缺少 'date' 列")
if 'fund' not in df.columns:
    raise KeyError("CSV 文件中缺少 'fund' 列")

# 解析日期并排序
df['date'] = pd.to_datetime(df['date'])
df.sort_values('date', inplace=True)
df.reset_index(drop=True, inplace=True)

# 如果基金列的数据是百分比形式（例如最大值 > 1），自动转换为小数
if df['fund'].max() > 1.0:
    df['fund'] = df['fund'] / 100.0

# 2. 计算超额收益（日度）
daily_rf = RF_ANNUAL / TRADING_DAYS
df['excess_return'] = df['fund'] - daily_rf

# 3. 计算滚动年化夏普比率
rolling_mean = df['excess_return'].rolling(window=WINDOW).mean()
rolling_std  = df['excess_return'].rolling(window=WINDOW).std()
df['rolling_sharpe'] = (rolling_mean / rolling_std) * np.sqrt(TRADING_DAYS)

# 4. 提取最后一个窗口值（剔除缺失值）
sharpe_dropna = df['rolling_sharpe'].dropna()
rolling_sharpe_last = float(sharpe_dropna.iloc[-1])

# 5. 绘制时间序列图并保存
plt.figure(figsize=(10, 5))
plt.plot(df['date'], df['rolling_sharpe'], color='navy', linewidth=1.2, label=f'{WINDOW}-Day Rolling Sharpe')
plt.axhline(y=0, color='gray', linestyle='--', alpha=0.7)
plt.title(f'{WINDOW}-Day Rolling Annualized Sharpe Ratio (rf={RF_ANNUAL*100:.1f}%)')
plt.xlabel('Date')
plt.ylabel('Sharpe Ratio')
plt.legend()
plt.tight_layout()

figure_path = 'rolling_sharpe.png'
plt.savefig(figure_path, dpi=150)
plt.close()

# 6. 按要求输出字典
result = {
    'rolling_sharpe_last': rolling_sharpe_last,
    'figure_path': figure_path
}

print("结果字典：")
print(result)
