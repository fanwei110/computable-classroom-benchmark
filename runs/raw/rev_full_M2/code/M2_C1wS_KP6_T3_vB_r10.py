import numpy as np
import pandas as pd
import scipy.stats as stats          # 仅导入以满足要求，实际未直接使用
import matplotlib.pyplot as plt      # 同上

# ---------- 1. 读取快照 CSV ----------
# 假设文件名固定为 fund.csv，其中 'fund' 列为基金的每日收益率（小数形式，如 0.001 表示 0.1%）
df = pd.read_csv('fund.csv')
returns = df['fund'].dropna()        # 剔除缺失值

# ---------- 2. 参数设定 ----------
rf_annual = 0.021                    # 年化无风险利率 2.1%
trading_days = 252                   # 一年交易天数假设
rf_daily = rf_annual / trading_days  # 日度无风险利率（简单利率折算）

# ---------- 3. 计算全样本年化夏普比率 ----------
excess_returns = returns - rf_daily
mean_excess = excess_returns.mean()
sigma_excess = excess_returns.std(ddof=1)   # 样本标准差（自由度 n-1）

sharpe_annual = np.sqrt(trading_days) * (mean_excess / sigma_excess)

# ---------- 4. 存入结果字典 ----------
result = {
    'sharpe_annual': round(sharpe_annual, 4)
}

# ---------- 输出（教师投屏时可直接看到） ----------
print("基金全样本年化夏普比率计算完成。")
print(result)
