import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os

# ==================== 可调参数 ====================
WINDOW = 60                # 滚动窗口长度（交易日）
RISK_FREE_RATE = 0.021     # 年化无风险利率
DATA_FILE = "fund_data.csv"  # 课程数据快照文件路径
FIGURE_FILE = "rolling_sharpe.png"  # 输出图表路径
# =================================================

# ---------- 1. 读取数据 ----------
if not os.path.exists(DATA_FILE):
    raise FileNotFoundError(f"数据文件不存在: {DATA_FILE}。请将课程数据快照放在该路径。")

# 假设 CSV 文件包含 'fund' 列，且数据按时间升序排列
df = pd.read_csv(DATA_FILE)

if 'fund' not in df.columns:
    # 如果列名不是 'fund'，尝试使用第一列
    raise ValueError("数据中缺少 'fund' 列，请检查文件格式。")

# 确保数据为数值类型，并去除缺失值
returns = pd.to_numeric(df['fund'], errors='coerce').dropna()

# ---------- 2. 计算滚动年化夏普比率 ----------
# 日无风险利率（简单利息方式）
rf_daily = RISK_FREE_RATE / 252

# 滚动均值和标准差
rolling_mean = returns.rolling(window=WINDOW).mean()
rolling_std = returns.rolling(window=WINDOW).std()

# 年化夏普比率 = (日超额收益均值 / 日超额收益标准差) * sqrt(252)
rolling_sharpe = (rolling_mean - rf_daily) / rolling_std * np.sqrt(252)

# 删除前 WINDOW-1 个无效值（NaN）
rolling_sharpe = rolling_sharpe.dropna()

# ---------- 3. 绘图并保存 ----------
plt.figure(figsize=(10, 5))
rolling_sharpe.plot(title=f"{WINDOW}-Day Rolling Annualized Sharpe Ratio")
plt.xlabel("Time")
plt.ylabel("Sharpe Ratio")
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.savefig(FIGURE_FILE, dpi=150)
plt.close()

# ---------- 4. 提取最后一个窗口的夏普值 ----------
rolling_sharpe_last = float(rolling_sharpe.iloc[-1])

# ---------- 5. 输出结果字典 ----------
result = {
    'rolling_sharpe_last': rolling_sharpe_last,
    'figure_path': os.path.abspath(FIGURE_FILE)
}

# 可选：打印结果，便于核查
print(result)
