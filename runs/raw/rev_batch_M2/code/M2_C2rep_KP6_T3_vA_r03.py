import pandas as pd
import numpy as np

# ----------------------------------------------------------------------
# 1. 读取数据
# ----------------------------------------------------------------------
df = pd.read_csv("data/market_snapshot_v1.csv")

if "fund" not in df.columns:
    raise ValueError("数据中缺少 'fund' 列，请检查文件。")

fund = df["fund"].dropna()

# ----------------------------------------------------------------------
# 2. 判断 fund 列是价格还是收益率，并计算日收益率
#    假设：若序列中位数 > 1，视为价格（净值）；否则视为小数收益率。
# ----------------------------------------------------------------------
if fund.median() > 1:
    # 价格序列 → 计算日简单收益率
    daily_returns = fund.pct_change().dropna()
else:
    # 假设已经是小数形式的日收益率
    daily_returns = fund.copy()
    # 若数值过大（例如百分比形式），则除以100转换为小数
    if daily_returns.abs().max() > 0.5:  # 经验阈值
        daily_returns = daily_returns / 100.0

# ----------------------------------------------------------------------
# 3. 参数设定
# ----------------------------------------------------------------------
rf_annual = 0.021          # 年化无风险利率
trading_days = 252         # 一年交易日数
rf_daily = rf_annual / trading_days

# ----------------------------------------------------------------------
# 4. 计算年化夏普比率
# ----------------------------------------------------------------------
excess_returns = daily_returns - rf_daily
mean_excess = excess_returns.mean()
std_excess = excess_returns.std()

sharpe_annual = np.sqrt(trading_days) * (mean_excess / std_excess)

# ----------------------------------------------------------------------
# 5. 输出结果
# ----------------------------------------------------------------------
result = {"sharpe_annual": sharpe_annual}

if __name__ == "__main__":
    print(result)
