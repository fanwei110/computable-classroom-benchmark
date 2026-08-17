import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import os

# ==================== 可调参数 ====================
WINDOW = 60                # 滚动窗口大小（交易日天数），可自由调整
RF_ANNUAL = 0.021          # 年化无风险利率 2.1%
TRADING_DAYS = 252         # 年交易日数
DATA_FILE = "fund_data.csv"  # 快照 CSV 文件名，请确保与脚本同一目录
# =================================================

# ---------- 1. 读取数据 ----------
try:
    df = pd.read_csv(DATA_FILE, parse_dates=True, index_col=0)
except FileNotFoundError:
    raise FileNotFoundError(f"找不到文件 '{DATA_FILE}'，请将快照 CSV 放置于当前工作目录。")

# 自动寻找 fund 列：优先使用列名为 'fund'，否则取第一个数值列
if 'fund' in df.columns:
    returns = df['fund']
else:
    numeric_cols = df.select_dtypes(include=[np.number]).columns
    if len(numeric_cols) == 0:
        raise ValueError("CSV 中没有数值列，无法作为收益率。")
    returns = df[numeric_cols[0]]
    print(f"警告：未找到 'fund' 列，自动使用 '{numeric_cols[0]}' 作为收益率序列。")

returns = returns.dropna().astype(float)

if len(returns) < WINDOW:
    raise ValueError(f"收益率序列长度 ({len(returns)}) 小于滚动窗口 ({WINDOW})，无法计算。")

# ---------- 2. 计算日超额收益 ----------
rf_daily = RF_ANNUAL / TRADING_DAYS
excess_returns = returns - rf_daily

# ---------- 3. 60日滚动年化夏普 ----------
rolling_mean = excess_returns.rolling(window=WINDOW).mean()
rolling_std = excess_returns.rolling(window=WINDOW).std()
# 年化夏普 = (日均超额收益 / 日超额收益标准差) * sqrt(252)
rolling_sharpe = (rolling_mean / rolling_std) * np.sqrt(TRADING_DAYS)

# ---------- 4. 提取最后一个窗口的数值 ----------
rolling_sharpe_clean = rolling_sharpe.dropna()
if rolling_sharpe_clean.empty:
    raise RuntimeError("未能生成任何滚动夏普值，请检查数据或窗口大小。")
last_sharpe = rolling_sharpe_clean.iloc[-1]   # 最后一个非缺失值

# ---------- 5. 绘图并保存 ----------
fig, ax = plt.subplots(figsize=(10, 5))
ax.plot(rolling_sharpe.index, rolling_sharpe.values, linewidth=1.2, color='#2c3e50')
ax.axhline(0, color='red', linestyle='--', linewidth=0.8)
ax.set_title(f"{WINDOW}-Day Rolling Annualized Sharpe Ratio", fontsize=14, fontweight='bold')
ax.set_xlabel("Date")
ax.set_ylabel("Annualized Sharpe Ratio")
ax.grid(True, alpha=0.3)
plt.tight_layout()

figure_path = os.path.abspath("rolling_sharpe.png")
fig.savefig(figure_path, dpi=150)
plt.close(fig)   # 避免内存占用

# ---------- 6. 构造输出字典 ----------
result = {
    'rolling_sharpe_last': round(float(last_sharpe), 6),
    'figure_path': figure_path
}

print("===== 结果输出 =====")
print(result)
