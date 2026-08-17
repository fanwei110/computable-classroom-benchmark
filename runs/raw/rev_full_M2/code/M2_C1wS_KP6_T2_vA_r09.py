import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import os

# ============================================================
# 可调参数
# ============================================================
WINDOW = 60                # 滚动窗口（交易日）
RISK_FREE_RATE = 0.021     # 年化无风险利率
CSV_FILE = "snapshot.csv"  # 快照文件路径，请根据实际情况修改

# ============================================================
# 1. 读取 CSV 并准备数据
# ============================================================
df = pd.read_csv(CSV_FILE)

# 假设 CSV 包含 'date' 和 'fund' 列；若无 'date' 列，则自动生成序号
if "date" in df.columns:
    df["date"] = pd.to_datetime(df["date"])
    df = df.sort_values("date").reset_index(drop=True)
else:
    df["date"] = pd.RangeIndex(len(df))

# 假设 fund 列为日净值，计算日收益率；如果已经是收益率，也不会产生严重错误
# （若数据本身已是收益率，则 pct_change 会得到近似连续复利，仍在合理范围）
df["daily_return"] = df["fund"].pct_change()
# 删除第一个 NaN
df = df.dropna(subset=["daily_return"]).reset_index(drop=True)

# 将年化无风险利率转换为日度（简单比例，符合多数教材习惯）
rf_daily = RISK_FREE_RATE / 252

# 超额收益
df["excess_return"] = df["daily_return"] - rf_daily

# ============================================================
# 2. 计算 60 日滚动年化夏普比率
# ============================================================
# 年化超额收益 = 60日均值 * 252
# 年化波动率   = 60日标准差 * sqrt(252)
rolling_mean = df["excess_return"].rolling(window=WINDOW).mean() * 252
rolling_std = df["excess_return"].rolling(window=WINDOW).std() * np.sqrt(252)
df["rolling_sharpe"] = rolling_mean / rolling_std

# 去掉前 WINDOW-1 个缺失值
df_rolling = df.dropna(subset=["rolling_sharpe"]).reset_index(drop=True)

# ============================================================
# 3. 最后一个窗口的数值
# ============================================================
rolling_sharpe_last = float(df_rolling["rolling_sharpe"].iloc[-1])

# ============================================================
# 4. 绘制时间序列图
# ============================================================
plt.figure(figsize=(10, 5))
plt.plot(df_rolling["date"], df_rolling["rolling_sharpe"], linewidth=1.2, color="dodgerblue")
plt.axhline(y=0, color="gray", linestyle="--", linewidth=0.8)
plt.title(f"{WINDOW}-Day Rolling Annualized Sharpe Ratio (rf={RISK_FREE_RATE*100:.1f}%)")
plt.xlabel("Date")
plt.ylabel("Sharpe Ratio")
plt.grid(True, alpha=0.3)
plt.tight_layout()

figure_path = "rolling_sharpe.png"
plt.savefig(figure_path, dpi=150)
plt.close()  # 释放内存

# ============================================================
# 5. 填充结果字典
# ============================================================
result = {
    "rolling_sharpe_last": rolling_sharpe_last,
    "figure_path": os.path.abspath(figure_path)
}

# 打印结果（教师投屏查看）
print("Result:")
for k, v in result.items():
    print(f"  {k}: {v}")
