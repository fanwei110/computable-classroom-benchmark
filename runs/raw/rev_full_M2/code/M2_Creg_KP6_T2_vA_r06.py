import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import os

# ---------------------------- 参数（可调） ----------------------------
WINDOW = 60                 # 滚动窗口长度（交易日）
RISK_FREE_RATE = 0.021      # 年化无风险利率
TRADING_DAYS = 252          # 一年交易日数
DATA_FILE = "fund_data.csv" # 数据文件路径
FIGURE_FILE = "rolling_sharpe.png"  # 输出图片路径

# ---------------------------- 1. 读取数据 ----------------------------
if not os.path.exists(DATA_FILE):
    raise FileNotFoundError(f"数据文件未找到: {DATA_FILE}。请确保文件存在且包含 'fund' 列。")

df = pd.read_csv(DATA_FILE, parse_dates=True)
if 'fund' not in df.columns:
    raise ValueError("数据文件必须包含 'fund' 列，代表日收益。")

# 假设 'fund' 列已经是日收益（小数形式，如 0.01 表示 1%）
daily_returns = df['fund'].astype(float)

# 如果数据是百分比形式（绝对值普遍 >1），自动转换为小数
if daily_returns.abs().mean() > 1:
    print("检测到日收益可能为百分比形式，自动除以 100 转换为小数。")
    daily_returns = daily_returns / 100.0

# ---------------------------- 2. 计算滚动年化夏普比率 ----------------------------
# 日度无风险利率（按比例折算）
daily_rf = RISK_FREE_RATE / TRADING_DAYS

# 超额收益
excess_returns = daily_returns - daily_rf

# 滚动均值和标准差
rolling_mean = excess_returns.rolling(window=WINDOW).mean()
rolling_std  = excess_returns.rolling(window=WINDOW).std()

# 年化夏普比率
rolling_sharpe = (rolling_mean / rolling_std) * np.sqrt(TRADING_DAYS)

# 最后一个窗口的夏普值
rolling_sharpe_last = rolling_sharpe.iloc[-1]

# ---------------------------- 3. 绘图并保存 ----------------------------
plt.figure(figsize=(10, 5))
plt.plot(rolling_sharpe, label=f'{WINDOW}-Day Rolling Annualized Sharpe', color='navy')
plt.axhline(y=0, color='gray', linestyle='--', linewidth=0.8)
plt.title('Rolling Annualized Sharpe Ratio')
plt.xlabel('Date')
plt.ylabel('Sharpe Ratio')
plt.legend()
plt.tight_layout()
plt.savefig(FIGURE_FILE, dpi=150)
plt.close()

# ---------------------------- 4. 输出结果 ----------------------------
result = {
    'rolling_sharpe_last': rolling_sharpe_last,
    'figure_path': os.path.abspath(FIGURE_FILE)
}

print("结果字典：")
print(result)
