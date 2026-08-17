import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import os

# ==================== 可调参数 ====================
WINDOW = 60              # 滚动窗口（交易日）
RF_ANNUAL = 0.021        # 年化无风险利率
ANNUALIZE = 252          # 年化交易日数
CSV_FILE = 'snapshot.csv' # 数据文件
FIG_NAME = 'rolling_sharpe.png'
# =================================================

# 1. 读取快照CSV -----------------------------------------------------------------
df = pd.read_csv(CSV_FILE)
# 尝试将date列解析为时间索引
if 'date' in df.columns:
    df['date'] = pd.to_datetime(df['date'])
    df.set_index('date', inplace=True)
# 确保fund列存在并转为数值
df['fund'] = pd.to_numeric(df['fund'], errors='coerce')
df.dropna(subset=['fund'], inplace=True)

# 2. 计算日超额收益 --------------------------------------------------------------
rf_daily = RF_ANNUAL / ANNUALIZE
excess_return = df['fund'] - rf_daily

# 3. 计算60日滚动年化夏普比率 -----------------------------------------------------
roll_mean = excess_return.rolling(window=WINDOW, min_periods=WINDOW).mean()
roll_std  = excess_return.rolling(window=WINDOW, min_periods=WINDOW).std()
rolling_sharpe = np.sqrt(ANNUALIZE) * roll_mean / roll_std

# 4. 获取最后一个窗口的值 ---------------------------------------------------------
rolling_sharpe_valid = rolling_sharpe.dropna()
if len(rolling_sharpe_valid) == 0:
    raise ValueError("数据不足以计算窗口为 %d 的滚动夏普比率" % WINDOW)
rolling_sharpe_last = float(rolling_sharpe_valid.iloc[-1])

# 5. 画图并保存 ------------------------------------------------------------------
plt.figure(figsize=(10, 5))
plt.plot(rolling_sharpe.index, rolling_sharpe.values, linewidth=1.0, color='#1f77b4')
plt.title('60-Day Rolling Annualized Sharpe Ratio')
plt.xlabel('Date' if isinstance(rolling_sharpe.index, pd.DatetimeIndex) else 'Period')
plt.ylabel('Sharpe Ratio')
plt.grid(True, linestyle='--', alpha=0.6)
plt.tight_layout()
plt.savefig(FIG_NAME, dpi=150)
plt.close()

# 6. 填充结果字典 ----------------------------------------------------------------
result = {
    'rolling_sharpe_last': rolling_sharpe_last,
    'figure_path': os.path.abspath(FIG_NAME)
}

# 输出至控制台（教师可投屏查看）
print("最终窗口年化夏普比率：", result['rolling_sharpe_last'])
print("图形保存位置：", result['figure_path'])
